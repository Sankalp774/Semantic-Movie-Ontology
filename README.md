# Semantic Movie Ontology — Knowledge Graphs for AI Systems

OWL + SPARQL project demonstrating **symbolic AI / knowledge graphs** — a differentiator next to pure neural projects.

```text
OWL schema (Movie, Actor, Director, Genre)
  → sample individuals
  → optional DBpedia enrichment
  → HermiT-style reasoning (owlready2)
  → SPARQL suite → metrics/sparql_report.json
  → Tkinter explorer
```

## Why this matters for AI/ML hiring

Modern Applied AI stacks combine:

- **neural** retrieval/generation  
- **symbolic** structure (ontologies, constraints, tool schemas)

This repo proves you understand RDF/OWL/SPARQL — rare for freshers.

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python movies_ontology.py          # create/populate OWL
python query_ontology.py           # classic demos
python -m kg.query_suite           # JSON metrics report
python app_tkinter.py              # UI
# optional network:
python integrate_dbpedia.py
```

## Core artifacts

| File | Role |
|------|------|
| `movies_ontology.py` | Schema + sample graph |
| `movies_ontology.owl` | Serialized ontology |
| `integrate_dbpedia.py` | Linked data import |
| `kg/query_suite.py` | Evaluatable SPARQL suite |
| `app_tkinter.py` | Lightweight explorer |

## Interview prompts you can answer

- Difference between RDF triple and property graph  
- Why inverse properties matter (`hasActor` ↔ `actedIn`)  
- When to use SPARQL vs vector search  
- How a KG can ground an LLM agent (tool: `query_movies`)  

## Limitations

- Educational scale graph  
- DBpedia availability varies  
- Not a neural recommender (see Mood-Movie-Recs-AI for that)  

## Author

Sankalp Sahu
