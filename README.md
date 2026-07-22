# Semantic Movie Ontology

Educational **knowledge graph / semantic web** project: define a movie OWL ontology, populate sample data, optionally enrich from **DBpedia**, reason, and query with **SPARQL**. Includes a small **Tkinter** UI.

## Concepts demonstrated

- OWL classes & properties (`Movie`, `Actor`, `Director`, `Genre`, …)  
- Inverse properties (`hasActor` ↔ `actedIn`)  
- Local ontology file: `movies_ontology.owl`  
- Linked data fetch via DBpedia (SPARQLWrapper)  
- SPARQL queries over local graph  

## Stack

- Python 3.8+  
- [owlready2](https://owlready2.readthedocs.io/)  
- rdflib, SPARQLWrapper  
- Tkinter (stdlib UI)  
- Java runtime recommended for HermiT reasoner (owlready2)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Scripts

| Script | Purpose |
|--------|---------|
| `movies_ontology.py` | Create schema + sample individuals → `movies_ontology.owl` |
| `add_movies_fixed.py` | Add / fix movie individuals |
| `integrate_dbpedia.py` | Pull movie facts from DBpedia |
| `query_ontology.py` | Example SPARQL queries |
| `app_tkinter.py` | Minimal desktop UI |

```bash
python movies_ontology.py
python integrate_dbpedia.py   # needs network
python query_ontology.py
python app_tkinter.py
```

## What I built

- Hands-on knowledge graph modeling for a domain (movies)  
- Bridge between local OWL data and open linked data (DBpedia)  
- Query + UI path for non-CLI demos  

## Limitations

- Small sample graph — not a production recommendation engine  
- DBpedia availability / schema drift can break fetches  
- UI is intentionally minimal  

## License

Educational / portfolio use.
