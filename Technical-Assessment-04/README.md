# Technical Assessment 04

**Student:** Haruka Gabrielle Ito

**Course and section:** CS0065 AN43

**Submission:** Individual

This outdoor-weather advisory demonstrates Knowledge Representation (KR),
Rule-Based Reasoning (RBR), and Case-Based Reasoning (CBR) on the same facts.
The measurements and past cases are illustrative classroom data.

## Run

Python 3 is required; there are no external packages. From this folder:

```text
python kr_rbr_cbr.py --demo
```

To type a revised CBR solution, or press Enter to keep the retrieved solution:

```text
python kr_rbr_cbr.py
```

The six input facts are in `KNOWLEDGE_BASE`. The default case base starts with
three past cases when `cases.json` is absent and retains new cases in that file.
Later runs reload it and avoid saving identical problem-and-solution pairs.
To use a fresh case file without changing the default one:

```text
python kr_rbr_cbr.py --demo --case-file fresh_demo.json
```

## Laboratory tasks

- **KR:** Six facts in three dictionary categories: environment, weather,
  and context.
- **RBR:** Four IF-THEN functions and an inference loop that checks every rule
  and returns all matching actions. The demo fires the heat, rain, and
  humidity rules.
- **CBR:** Three past cases, ranked feature similarity, reuse of C002 at
  95.42%, a demonstrated manual revision, and retention as C004.
- **Learning:** The updated base contains four cases, and the same problem
  retrieves C004 at 100%. Interactive revision can replace the solution or
  leave it unchanged.

Numeric similarities are normalized and averaged with Boolean matches.
The normalization scales are comparison parameters, not weather alert limits.
The complete source, executed output, RBR and CBR screenshots, knowledge-base
description, and comparative reflection are in the separate assessment document.
