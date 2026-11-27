"""
universal_hierarchy_parser.py

Herramienta STANDALONE (fuera del pipeline knowledge-scraper) para extraer
listas jerárquicas de texto (término + descripción, con categorías y
sub-ítems anidados) de CUALQUIER web, usando anclas de XPath ID reales
en vez de heurísticas de texto frágiles.

Usa lxml.html directamente (no BeautifulSoup) porque BeautifulSoup NO
expone XPath real sobre sus Tag — solo lxml.html sí.

--------------------------------------------------------------------
IDEA DE DISEÑO (la tuya, formalizada):
--------------------------------------------------------------------
  Nodo 0        -> root_xpath_id       (p.ej. "mwAeM"  == "Geographical")
  Nodo 1A..1X   -> category_xpath_ids  (p.ej. ["mwAeQ", "mwAjU", "mwA2o"])
  Nodo 2AY..2AX -> se detectan solos recorriendo <ul>/<li> hermanos dentro
                   de cada nodo de categoría (no hace falta dar su ID,
                   basta con dar el ID del PRIMER <ul> anidado, el resto
                   se recorre automáticamente por hermandad de nodos).
  Nodo 3A       -> se detecta solo: es el <dl> hermano inmediato del <ul>
                   del ítem (perfil UL_THEN_DL) — no hace falta su ID.

Es decir: dando el ID del nodo raíz + los IDs de cada categoría (o ni
siquiera eso, si usas heading_text en vez de xpath_id), el parser
recorre el resto de la jerarquía solo, siguiendo el NestingProfile
indicado. Esto cumple tu restricción: "que nada más poniendo el primer
ID de cada nodo anidado el script funcione".
--------------------------------------------------------------------
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import pandas as pd
from lxml import html as lxml_html


# ======================================================================
# MODELOS ESTÁNDAR DE ANIDACIÓN (los más comunes en la práctica)
# ======================================================================

class NestingProfile(str, Enum):
    """
    UL_THEN_DL
        <ul><li><b>Término</b></li></ul>
        <dl><dd>Descripción</dd></dl>
        Estilo Wikipedia moderna (MediaWiki "definition-style" tras lista).

    LI_INLINE
        <li><b>Término</b>: descripción en el mismo <li></li>
        El patrón más común en blogs, docs técnicas, FAQs.

    DT_DD
        <dl><dt>Término</dt><dd>Descripción</dd></dl>
        Lista de definición clásica en HTML (glosarios, diccionarios).

    HEADING_PARAGRAPH
        <h4>Término</h4><p>Descripción</p>
        Común en páginas de producto/documentación con sub-secciones.

    AUTO
        Prueba los perfiles anteriores en orden y se queda con el
        primero que produzca filas no vacías. Útil cuando no conoces
        de antemano el patrón exacto de la web objetivo.
    """
    UL_THEN_DL = "ul_then_dl"
    LI_INLINE = "li_inline"
    DT_DD = "dt_dd"
    HEADING_PARAGRAPH = "heading_par"
    AUTO = "auto"


@dataclass
class HierarchyNode:
    """Representa un 'Nodo' tal como los describiste: una etiqueta de
    texto asociada a un elemento localizable por XPath ID o por texto
    de heading."""
    label: str
    xpath_id: Optional[str] = None
    heading_text: Optional[str] = None


# ======================================================================
# LOCALIZACIÓN DE NODOS
# ======================================================================

def _get_by_id(tree, xpath_id: str):
    try:
        return tree.get_element_by_id(xpath_id)
    except KeyError:
        return None


def _find_heading_element(tree, heading_text: str):
    for level in range(2, 7):
        for h in tree.xpath(f"//h{level}"):
            text = " ".join(h.itertext()).strip()
            if heading_text.strip().lower() in text.lower():
                return h
    return None


def _resolve_node_container(tree, node: HierarchyNode):
    """Devuelve el elemento contenedor (idealmente un <section>, o si no
    existe, el padre directo del heading) para el nodo dado."""
    element = None

    if node.xpath_id:
        element = _get_by_id(tree, node.xpath_id)

    if element is None and node.heading_text:
        element = _find_heading_element(tree, node.heading_text)

    if element is None:
        return None

    # Si el propio elemento ya es un contenedor de sección, úsalo.
    if element.tag == "section":
        return element

    # Si es un heading (h2..h6) o su wrapper div.mw-heading, sube al
    # <section> ancestro; si no hay <section>, usa el padre directo.
    ancestor_section = element.xpath("ancestor::section[1]")
    if ancestor_section:
        return ancestor_section[0]

    return element.getparent() if element.getparent() is not None else element


# ======================================================================
# EXTRACCIÓN POR PERFIL DE ANIDACIÓN
# ======================================================================

def _text(el) -> str:
    return " ".join(el.itertext()).strip() if el is not None else ""


def _extract_ul_then_dl(container, section_label, category_label):
    """Perfil UL_THEN_DL: pares secuenciales <ul>/<dl> hermanos."""
    records = []
    children = [c for c in container if isinstance(c.tag, str)]

    i = 0
    while i < len(children):
        node = children[i]

        if node.tag == "ul":
            items = _walk_ul_items(node)

            next_el = children[i + 1] if i + 1 < len(children) else None
            dd_texts = []
            consumed_dl = False
            if next_el is not None and next_el.tag == "dl":
                dds = next_el.findall("dd")
                dd_texts = [_text(dd) for dd in dds]
                consumed_dl = True

            dd_cursor = 0
            for item_title, inline_desc, parent_item in items:
                if parent_item is None and dd_cursor < len(dd_texts):
                    description = dd_texts[dd_cursor]
                    dd_cursor += 1
                else:
                    description = inline_desc

                records.append({
                    "Section": section_label,
                    "Category": category_label,
                    "Item": item_title,
                    "Description": description,
                    "Parent_item": parent_item,
                })

            if consumed_dl:
                i += 1

        i += 1

    return records


def _walk_ul_items(ul):
    """Extrae (título, descripción_inline, padre) de los <li> directos
    de un <ul>, recursando en sub-<ul> anidados."""
    results = []
    for li in ul.findall("li"):
        nested_uls = li.findall("ul")

        bold = li.find(".//b")
        if bold is None:
            bold = li.find(".//strong")

        if bold is not None:
            item_title = _text(bold)
            li_text = _text(li)
            inline_description = (
                li_text[len(item_title):].strip(" :.-")
                if li_text.startswith(item_title) else ""
            )
        else:
            full_text = _text(li)
            for nested in nested_uls:
                nested_text = _text(nested)
                if nested_text:
                    full_text = full_text.replace(nested_text, "")
            parts = re.split(r"[:—–-]", full_text, maxsplit=1)
            item_title = parts[0].strip()
            inline_description = parts[1].strip() if len(parts) > 1 else ""

        for nested in nested_uls:
            nested_text = _text(nested)
            if nested_text and nested_text in inline_description:
                inline_description = inline_description.replace(nested_text, "").strip()

        results.append((item_title, inline_description, None))

        for nested in nested_uls:
            for (sub_t, sub_d, _) in _walk_ul_items(nested):
                results.append((sub_t, sub_d, item_title))

    return results


def _extract_li_inline(container, section_label, category_label):
    records = []
    for ul in container.findall(".//ul"):
        for item_title, inline_desc, parent_item in _walk_ul_items(ul):
            records.append({
                "Section": section_label,
                "Category": category_label,
                "Item": item_title,
                "Description": inline_desc,
                "Parent_item": parent_item,
            })
    return records


def _extract_dt_dd(container, section_label, category_label):
    records = []
    for dl in container.findall(".//dl"):
        dts = dl.findall("dt")
        dds = dl.findall("dd")
        for dt, dd in zip(dts, dds):
            records.append({
                "Section": section_label,
                "Category": category_label,
                "Item": _text(dt),
                "Description": _text(dd),
                "Parent_item": None,
            })
    return records


def _extract_heading_paragraph(container, section_label, category_label):
    records = []
    children = [c for c in container if isinstance(c.tag, str)]
    for i, node in enumerate(children):
        if node.tag in ("h3", "h4", "h5", "h6"):
            item_title = _text(node)
            desc = ""
            if i + 1 < len(children) and children[i + 1].tag == "p":
                desc = _text(children[i + 1])
            records.append({
                "Section": section_label,
                "Category": category_label,
                "Item": item_title,
                "Description": desc,
                "Parent_item": None,
            })
    return records


_PROFILE_EXTRACTORS = {
    NestingProfile.UL_THEN_DL: _extract_ul_then_dl,
    NestingProfile.LI_INLINE: _extract_li_inline,
    NestingProfile.DT_DD: _extract_dt_dd,
    NestingProfile.HEADING_PARAGRAPH: _extract_heading_paragraph,
}


# ======================================================================
# API PÚBLICA
# ======================================================================

def parse_hierarchy(
    html: str,
    root: HierarchyNode,
    categories: list[HierarchyNode],
    profile: NestingProfile = NestingProfile.AUTO,
) -> pd.DataFrame:
    """
    Parsea una jerarquía de texto a partir de un nodo raíz (Section) y
    una lista de nodos de categoría, cada uno localizado por su
    xpath_id o heading_text.

    Ejemplo (equivalente a tu Nodo 0 / Nodo 1A / Nodo 1X):

        root = HierarchyNode(label="Geographical", xpath_id="mwAeM")
        categories = [
            HierarchyNode(label="Peninsulas", xpath_id="mwAeQ"),
            HierarchyNode(label="Regional",   xpath_id="mwAjU"),
            HierarchyNode(label="Other groupings", heading_text="Other groupings"),
        ]
        df = parse_hierarchy(html, root, categories, profile=NestingProfile.UL_THEN_DL)
    """
    tree = lxml_html.fromstring(html)

    all_records = []

    for cat_node in categories:
        container = _resolve_node_container(tree, cat_node)
        if container is None:
            print(f'⚠️  Categoría "{cat_node.label}" no encontrada (xpath_id={cat_node.xpath_id}, heading_text={cat_node.heading_text}), se omite.')
            continue

        if profile == NestingProfile.AUTO:
            records = []
            for candidate_profile, extractor in _PROFILE_EXTRACTORS.items():
                records = extractor(container, root.label, cat_node.label)
                if records:
                    break
        else:
            extractor = _PROFILE_EXTRACTORS[profile]
            records = extractor(container, root.label, cat_node.label)

        all_records.extend(records)

    df = pd.DataFrame(all_records)

    if df.empty:
        raise ValueError("No hierarchical items parsed for any category.")

    return df


# ======================================================================
# EJEMPLO DE USO
# ======================================================================

if __name__ == "__main__":
    with open("fixture_regions_v3.html", encoding="utf-8") as f:
        html_source = f.read()

    root = HierarchyNode(label="Geographical", heading_text="Geographical")
    categories = [
        HierarchyNode(label="Peninsulas", heading_text="Peninsulas"),
        HierarchyNode(label="Regional", heading_text="Regional"),
    ]

    df = parse_hierarchy(
        html_source, root, categories, profile=NestingProfile.UL_THEN_DL
    )

    pd.set_option("display.max_colwidth", 60)
    print(df.to_string())
