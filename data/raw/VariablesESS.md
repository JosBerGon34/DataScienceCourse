# Datos Principales

**Variable target:** `lrscale` — Escala de 0 a 10. Siendo 0 extrema izquierda a 10 extrema derecha.

**Variables predictoras:**

Todas las escalas de estas variables son discontinuas, con pasos de 1. Y otras son categóricas factorizadas. Habrá variables cualitativas y otras serán más de referencia para distinguir las clases gracias a la comparación que haremos con variables económicas generales por país.

---

## Variables

### `-cntry` — País

Países de la zona euro. Este estudio solo trabajará con datos de 3 grandes bloques.

**Unique values:** Austria, Belgium, Bulgaria, Croatia, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Israel, Italy, Netherlands, Norway, Poland, Portugal, Serbia, Slovakia, Slovenia, Spain, Sweden, Switzerland, United Kingdom.

---

### `-netusoft` — Internet use, how often

**Question:** People can use the internet on different devices such as computers, tablets and smartphones. How often do you use the internet on these or any other devices, whether for work or personal use?

**ESS rounds:** ESS8, ESS9, ESS10, ESS10SC, ESS11

| Value | Category |
|-------|----------|
| 1 | Never |
| 2 | Only occasionally |
| 3 | A few times a week |
| 4 | Most days |
| 5 | Every day |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-ppltrst` — Most people can be trusted or you can't be too careful

**Question:** Using this card, generally speaking, would you say that most people can be trusted, or that you can't be too careful in dealing with people? Please tell me on a score of 0 to 10, where 0 means you can't be too careful and 10 means that most people can be trusted.

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 0 | You can't be too careful |
| 1–9 | (escala 0–10) |
| 10 | Most people can be trusted |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-clsprty` — Feel closer to a particular party than all other parties

**Question:** Is there a particular political party you feel closer to than all the other parties?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Yes |
| 2 | No |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-gincdif` — Government should reduce differences in income levels

**Question:** Using this card, please say to what extent you agree or disagree with each of the following statements. The government should take measures to reduce differences in income levels.

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Agree strongly |
| 2 | Agree |
| 3 | Neither agree nor disagree |
| 4 | Disagree |
| 5 | Disagree strongly |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-lawobey` — The law should always be obeyed

**Question:** Using this card, please say to what extent you agree or disagree with each of the following statements. Whatever the circumstances, the law should always be obeyed.

**ESS rounds:** ESS1

| Value | Category |
|-------|----------|
| 1 | Agree strongly |
| 2 | Agree |
| 3 | Neither agree nor disagree |
| 4 | Disagree |
| 5 | Disagree strongly |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-lrscale` — Placement on left-right scale ⭐ *(target)*

**Question:** In politics people sometimes talk of 'left' and 'right'. Using this card, where would you place yourself on this scale, where 0 means the left and 10 means the right?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 0 | Left |
| 1–9 | (escala 0–10) |
| 10 | Right |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-mmbprty` — Member of political party

**Question:** Are you a member of any political party?

**ESS rounds:** ESS1–ESS5

| Value | Category |
|-------|----------|
| 1 | Yes |
| 2 | No |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-needtru` — Employees need strong trade unions to protect work conditions/wages

**Question:** Using this card, please say to what extent you agree or disagree with each of the following statements. Employees need strong trade unions to protect their working conditions and wages.

**ESS rounds:** ESS1

| Value | Category |
|-------|----------|
| 1 | Agree strongly |
| 2 | Agree |
| 3 | Neither agree nor disagree |
| 4 | Disagree |
| 5 | Disagree strongly |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-trstlgl` — Trust in the legal system

**Question:** Using this card, please tell me on a score of 0–10 how much you personally trust each of the institutions I read out. 0 means you do not trust an institution at all, and 10 means you have complete trust. ...the legal system?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 0 | No trust at all |
| 1–9 | (escala 0–10) |
| 10 | Complete trust |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-trstprl` — Trust in country's parliament

**Question:** Using this card, please tell me on a score of 0–10 how much you personally trust each of the institutions I read out. 0 means you do not trust an institution at all, and 10 means you have complete trust. ...[country]'s parliament?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 0 | No trust at all |
| 1–9 | (escala 0–10) |
| 10 | Complete trust |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-trstun` — Trust in the United Nations

**Question:** Using this card, please tell me on a score of 0–10 how much you personally trust each of the institutions I read out. 0 means you do not trust an institution at all, and 10 means you have complete trust. ...the United Nations?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 0 | No trust at all |
| 1–9 | (escala 0–10) |
| 10 | Complete trust |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-imbgeco` — Immigration bad or good for country's economy

**Question:** Would you say it is generally bad or good for [country]'s economy that people come to live here from other countries?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 0 | Bad for the economy |
| 1–9 | (escala 0–10) |
| 10 | Good for the economy |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-atchctr` — How emotionally attached to [country]

**Question:** How emotionally attached do you feel to [country]? Please choose a number from 0 to 10, where 0 means not at all emotionally attached and 10 means very emotionally attached.

**ESS rounds:** ESS8, ESS9, ESS10, ESS10SC, ESS11

| Value | Category |
|-------|----------|
| 0 | Not at all emotionally attached |
| 1–9 | (escala 0–10) |
| 10 | Very emotionally attached |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-atcherp` — How emotionally attached to Europe

**Question:** And how emotionally attached do you feel to Europe?

**ESS rounds:** ESS8, ESS9, ESS10, ESS10SC, ESS11

| Value | Category |
|-------|----------|
| 0 | Not at all emotionally attached |
| 1–9 | (escala 0–10) |
| 10 | Very emotionally attached |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-brncntr` — Born in country

**Question:** Were you born in [country]?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Yes |
| 2 | No |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-ctzcntr` — Citizen of country

**Question:** Are you a citizen of [country]?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Yes |
| 2 | No |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-rlgdgr` — How religious are you

**Question:** Regardless of whether you belong to a particular religion, how religious would you say you are?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 0 | Not at all religious |
| 1–9 | (escala 0–10) |
| 10 | Very religious |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-rlgdnm` — Religion or denomination belonging to at present

**Question:** Which one?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Roman Catholic |
| 2 | Protestant |
| 3 | Eastern Orthodox |
| 4 | Other Christian denomination |
| 5 | Jewish |
| 6 | Islam |
| 7 | Eastern religions |
| 8 | Other Non-Christian religions |
| 66 | Not applicable* |
| 77 | Refusal* |
| 99 | No answer* |

\* Missing Value

---

### `-hhmmb` — Number of people living regularly as member of household

**Question:** Including yourself, how many people - including children - live here regularly as members of this household?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-gndr` — Gender

**Question:** CODE SEX, respondent

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Male |
| 2 | Female |
| 9 | No answer* |

\* Missing Value

---

### `-agea` — Age of respondent, calculated

**Question:** Age of respondent, calculated

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 999 | Not available* |

\* Missing Value

---

### `-ablret` — Worried not being able to retire at the age you would like to

**Question:** Using this card, can you tell me how worried, if at all, you are that you will not be able to retire at the age you would like to?

**ESS rounds:** ESS3

| Value | Category |
|-------|----------|
| 0 | Not worried at all |
| 1–9 | (escala 0–10) |
| 10 | Extremely worried |
| 66 | Not applicable* |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-chldhm` — Children living at home or not

**Question:** INTERVIEWER REFER TO HOUSEHOLD GRID AND CODE:

**ESS rounds:** ESS1–ESS8

| Value | Category |
|-------|----------|
| 1 | Respondent lives with children at household grid |
| 2 | Does not |
| 9 | Not available* |

\* Missing Value

---

### `-domicil` — Domicile, respondent's description

**Question:** Which phrase on this card best describes the area where you live?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | A big city |
| 2 | Suburbs or outskirts of big city |
| 3 | Town or small city |
| 4 | Country village |
| 5 | Farm or home in countryside |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-edulvlb` — Highest level of education

**Question:** What is the highest level of education you have successfully completed?

**ESS rounds:** ESS5–ESS11

| Value | Category |
|-------|----------|
| 0 | Not completed ISCED level 1 |
| 113 | ISCED 1, completed primary education |
| 129 | Vocational ISCED 2C < 2 years, no access ISCED 3 |
| 212 | General/pre-vocational ISCED 2A/2B, access ISCED 3 vocational |
| 213 | General ISCED 2A, access ISCED 3A general/all 3 |
| 221 | Vocational ISCED 2C >= 2 years, no access ISCED 3 |
| 222 | Vocational ISCED 2A/2B, access ISCED 3 vocational |
| 223 | Vocational ISCED 2, access ISCED 3 general/all |
| 229 | Vocational ISCED 3C < 2 years, no access ISCED 5 |
| 311 | General ISCED 3 >=2 years, no access ISCED 5 |
| 312 | General ISCED 3A/3B, access ISCED 5B/lower tier 5A |
| 313 | General ISCED 3A, access upper tier ISCED 5A/all 5 |
| 321 | Vocational ISCED 3C >= 2 years, no access ISCED 5 |
| 322 | Vocational ISCED 3A, access ISCED 5B/lower tier 5A |
| 323 | Vocational ISCED 3A, access upper tier ISCED 5A/all 5 |
| 412 | General ISCED 4A/4B, access ISCED 5B/lower tier 5A |
| 413 | General ISCED 4A, access upper tier ISCED 5A/all 5 |
| 421 | ISCED 4 programmes without access ISCED 5 |
| 422 | Vocational ISCED 4A/4B, access ISCED 5B/lower tier 5A |
| 423 | Vocational ISCED 4A, access upper tier ISCED 5A/all 5 |
| 510 | ISCED 5A short, intermediate/academic/general tertiary below bachelor |
| 520 | ISCED 5B short, advanced vocational qualifications |
| 610 | ISCED 5A medium, bachelor/equivalent from lower tier tertiary |
| 620 | ISCED 5A medium, bachelor/equivalent from upper/single tier tertiary |
| 710 | ISCED 5A long, master/equivalent from lower tier tertiary |
| 720 | ISCED 5A long, master/equivalent from upper/single tier tertiary |
| 800 | ISCED 6, doctoral degree |
| 5555 | Other |
| 7777 | Refusal* |
| 8888 | Don't know* |
| 9999 | No answer* |

\* Missing Value

---

### `-emplno` — Number of employees respondent has/had

**Question:** How many employees (if any) do/did you have?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 66666 | Not applicable* |
| 77777 | Refusal* |
| 88888 | Don't know* |
| 99999 | No answer* |

\* Missing Value

---

### `-emplrel` — Employment relation

**Question:** In your main job are/were you...

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Employee |
| 2 | Self-employed |
| 3 | Working for own family business |
| 6 | Not applicable* |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

### `-mnactic` — Main activity, last 7 days. All respondents. Post coded

**Question:** POST CODE: MAIN ACTIVITY

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Paid work |
| 2 | Education |
| 3 | Unemployed, looking for job |
| 4 | Unemployed, not looking for job |
| 5 | Permanently sick or disabled |
| 6 | Retired |
| 7 | Community or military service |
| 8 | Housework, looking after children, others |
| 9 | Other |
| 66 | Not applicable* |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-tporgwk` — What type of organisation work/worked for

**Question:** Which of the types of organisation on this card do/did you work for?

**ESS rounds:** ESS4–ESS11

| Value | Category |
|-------|----------|
| 1 | Central or local government |
| 2 | Other public sector (such as education and health) |
| 3 | A state owned enterprise |
| 4 | A private firm |
| 5 | Self employed |
| 6 | Other |
| 66 | Not applicable* |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-wkhtot` — Total hours normally worked per week in main job overtime included

**Question:** Regardless of your basic or contracted hours, how many hours do/did you normally work a week (in your main job), including any paid or unpaid overtime.

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 666 | Not applicable* |
| 777 | Refusal* |
| 888 | Don't know* |
| 999 | No answer* |

\* Missing Value

---

### `-impfreea` — Important to make own decisions and be free

**Question:** Now I will briefly describe some people. Please listen to each description and tell me how much each person is or is not like you. It is important to her/him to make her/his own decisions about what she/he does. She/he likes to be free and not depend on others.

**ESS rounds:** ESS11

| Value | Category |
|-------|----------|
| 1 | Very much like me |
| 2 | Like me |
| 3 | Somewhat like me |
| 4 | A little like me |
| 5 | Not like me |
| 6 | Not like me at all |
| 66 | Not applicable* |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-impricha` — Important to be rich, have money and expensive things

**Question:** Now I will briefly describe some people. Please listen to each description and tell me how much each person is or is not like you. It is important to her/him to be rich. She/he wants to have a lot of money and expensive things.

**ESS rounds:** ESS11

| Value | Category |
|-------|----------|
| 1 | Very much like me |
| 2 | Like me |
| 3 | Somewhat like me |
| 4 | A little like me |
| 5 | Not like me |
| 6 | Not like me at all |
| 66 | Not applicable* |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-imptrada` — Important to follow traditions and customs

**Question:** Now I will briefly describe some people. Please listen to each description and tell me how much each person is or is not like you. Tradition is important to her/him. She/he tries to follow the customs handed down by her/his religion or her/his family.

**ESS rounds:** ESS11

| Value | Category |
|-------|----------|
| 1 | Very much like me |
| 2 | Like me |
| 3 | Somewhat like me |
| 4 | A little like me |
| 5 | Not like me |
| 6 | Not like me at all |
| 66 | Not applicable* |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-iphlppla` — Important to help people and care for others well-being

**Question:** Now I will briefly describe some people. Please listen to each description and tell me how much each person is or is not like you. It's very important to her/him to help the people around her/him. She/he wants to care for their well-being.

**ESS rounds:** ESS11

| Value | Category |
|-------|----------|
| 1 | Very much like me |
| 2 | Like me |
| 3 | Somewhat like me |
| 4 | A little like me |
| 5 | Not like me |
| 6 | Not like me at all |
| 66 | Not applicable* |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-happy` — How happy are you

**Question:** Taking all things together, how happy would you say you are?

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 0 | Extremely unhappy |
| 1–9 | (escala 0–10) |
| 10 | Extremely happy |
| 77 | Refusal* |
| 88 | Don't know* |
| 99 | No answer* |

\* Missing Value

---

### `-health` — Subjective general health

**Question:** How is your health in general? Would you say it is...

**ESS rounds:** ESS1–ESS11

| Value | Category |
|-------|----------|
| 1 | Very good |
| 2 | Good |
| 3 | Fair |
| 4 | Bad |
| 5 | Very bad |
| 7 | Refusal* |
| 8 | Don't know* |
| 9 | No answer* |

\* Missing Value

---

## Protocol de Missing Data (ESS Portal)

### C. Principles of variable definitions — C1. Missing values

Analysis of item non-response is an important part of quality control of survey items, and consistent use of missing values in the questionnaire and other documentation ensures uniform coding of skips in the interview. The aim is that the ESS data files will contain detailed information on item non-response.

The missing values in the data files are defined in the following way:

| Code | Type | Description |
|------|------|-------------|
| 6, 66, 666… | **Not applicable** | The respondent has been routed away from the question. This missing value might be coded in the national data files before deposit, but the coding will be overwritten by standardised procedures at NSD. |
| 7, 77, 777… | **Refusals** | The respondent has explicitly refused. These codes are almost always available. They can be included in the list of answering options presented to the interviewers, or placed in administrative columns, menus etc. |
| 8, 88, 888… | **Don't know** | These codes are almost always available. They can be included in the list of answering options presented to the interviewers, or placed in administrative columns, menus etc. |
| 9, 99, 999… | **No answer** | Codes for missing data not elsewhere explained, for example respondent/interviewer errors and production/system errors. In administrative variables, 9, 99, 999 etc. are labelled "Not available". |

> **Important notice:** In most filters, "Refusals" (7, 77, 777 etc) are routed the same way as "Don't knows" (8, 88, 888 etc). The exceptions being filter variables C20 (CTZCNTR), F53 (EMPRF14) and F57 (EMPRM14).   