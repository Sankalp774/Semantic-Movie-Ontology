"""
Runnable SPARQL suite with machine-readable results for the movies ontology.

  python -m kg.query_suite
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from owlready2 import get_ontology


QUERIES = {
    "movies_after_2000": """
        PREFIX : <http://example.org/movies_ontology.owl#>
        SELECT ?title ?year WHERE {
            ?m a :Movie .
            ?m :hasTitle ?title .
            ?m :hasReleaseYear ?year .
            FILTER (?year > 2000)
        }
    """,
    "movies_with_actors": """
        PREFIX : <http://example.org/movies_ontology.owl#>
        SELECT ?title ?actor WHERE {
            ?m a :Movie .
            ?m :hasTitle ?title .
            ?m :hasActor ?actor .
        }
    """,
}


def main() -> None:
    owl = ROOT / "movies_ontology.owl"
    if not owl.exists():
        # bootstrap
        import movies_ontology  # noqa: F401

    onto = get_ontology(str(owl)).load()
    report = {"ontology": str(owl.name), "queries": {}}
    for name, sparql in QUERIES.items():
        rows = list(onto.world.sparql(sparql))
        report["queries"][name] = {
            "row_count": len(rows),
            "sample": [[str(c) for c in row] for row in rows[:10]],
        }

    out = ROOT / "metrics" / "sparql_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
