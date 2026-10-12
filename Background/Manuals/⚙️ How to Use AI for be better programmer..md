**3 Symptoms we need to detect, in order to know if we are being dependant of AI, and at the same time if we are are not learning afterall, delegating all our experience
just asking to AI to make all the work for us:

Symptom 1: Blank sheet symptom: They give you a problem to solve and you don't know how to start in front of a code editor
Symptom 2: You can read code, but you cant write it.
Symptom 3:  You dont know to debugg code, always delegate the solution to AI copy-pasting mostly.


### 1) Always you first, AI later:

Try to present your logic pipeline, and syntax estructure to AI before get the first usable
programm. Always getting reference of your lack of methodology and programming.
Always try to get a feedback about your solution at first instance.

### 2) AI only explanes, You write:

When you don't know about to do something in programming, ask to AI for explanations
rather to copy the code blocks.
-So AI reviews, you refactor.
### 3) Every generated code, one questionary:

If in a real project, AI makes entirely code blocks, don't integrate it directly to production. Untill you can respond the next 3 questions:

A) What does every block of code, explaining main syntax instructions.
B) Why the codeblock is done like this especificly.
C) What would happen if arrives an unexpected data.

### 4) Train your programming skills, at least one time per week:

-Example: Im a bit rusty about transform tuples, lists in to dataframe columns, also cleaning data or producing new columns using maths or categorical manipulation.
Make a prompt for an AI, asking for simple exercises and start coding. Use AI as 
professor.
-Every program, script or pipeline, try to make it reusable.

### 5) Conlusions:

The thing that differs and make valuable between devs and programmer is:
-The capability of Understanding the problem we need to solve with the programm
-The code build decision, which part its important and which is not.
-Detect when the solution is not good or just is not what we needed.
-Ensure we are concious about our own code, take responsability of the code we put
on production.


***METODOLOGY SOLUTION:

# Software Development Workflow with AI

Using AI efficiently is not about asking it to write code.
It is about integrating AI into a structured software engineering workflow.

The development process should be divided into three complementary architectures:

```text
                    PROBLEM
                       │
                       ▼
        ┌──────────────────────────────┐
        │ 1. SOFTWARE ARCHITECTURE      │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │ 2. CODE DEVELOPMENT           │
        └──────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │ 3. DEBUG ARCHITECTURE         │
        └──────────────────────────────┘
                       │
                       ▼
                  REFACTOR
                       │
                       ▼
               REUSABLE MODULE
                       │
                       ▼
              KNOWLEDGE LIBRARY
```

---

# 1. Software Architecture

The first step is **never writing code**.

The objective is understanding the problem and transforming it into a logical model.

Questions to answer:

- What problem am I solving?
- What are the inputs?
- What are the outputs?
- Which entities interact?
- Which modules are required?
- Which parts can be reused?

Deliverables:

- Logical pipeline
- GRAFCET / Flow diagram
- Entity relationships
- Function responsibilities
- Project architecture

### AI Role

AI acts as an **architectural reviewer**.

It validates the logical design and suggests improvements, but the architecture always belongs to the developer.

---

# 2. Code Development

Once the architecture is clear, implementation begins.

The objective is translating the logical model into clean, modular and reusable code.

Recommended workflow:

Problem

↓

Pseudo-code

↓

Functions

↓

Implementation

↓

Testing

↓

Refactoring

The developer always writes and understands the code.

### AI Role

AI acts as a **development assistant**.

Typical tasks:

- Explain libraries
- Suggest better implementations
- Detect duplicated code
- Improve readability
- Propose refactoring

AI should **never replace the developer's understanding**.

---

# 3. Debug Architecture

Debugging is not fixing code.

Debugging is understanding why reality differs from our expectations.

When something fails:

Do NOT modify the code immediately.

Instead:

Observe

↓

Inspect variables

↓

Inspect data types

↓

Inspect program state

↓

Locate the exact failure

↓

Understand the cause

↓

Apply the fix

↓

Run regression tests

Most bugs are discovered by understanding the execution state rather than rewriting functions.

### AI Role

AI acts as a **mentor**.

Instead of asking:

"Fix this code."

Prefer asking:

"What should I inspect first?"

or

"Which variable is most likely causing this behaviour?"

---

# Continuous Improvement

Every solved problem should improve your personal engineering framework.

Think

↓

Model

↓

Develop

↓

Debug

↓

Generalize

↓

Reuse

If a solution is useful once, keep it.

If it is useful twice, turn it into a function.

If it is useful many times, turn it into a reusable module.

Over time your projects become your own software engineering library instead of isolated scripts.

---

# Human vs AI Responsibilities

| Phase | Human | AI |
|--------|-------|----|
| Software Architecture | Architect | Reviewer |
| Code Development | Developer | Assistant |
| Debug Architecture | Investigator | Mentor |
| Refactoring | Decision Maker | Advisor |

The human always owns the architecture, decisions and final responsibility.

AI accelerates learning and implementation, but never replaces engineering judgement.
