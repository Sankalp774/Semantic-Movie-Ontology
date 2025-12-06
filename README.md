The Movies Ontology Project is a semantic web application built in Python that creates, populates, and queries an OWL ontology focused on movies. It demonstrates key semantic web concepts such as RDF triples, OWL classes/properties, reasoning, SPARQL querying, and linked data integration with external sources like DBpedia (a knowledge graph extracted from Wikipedia).
This project allows users to:

Define a movie ontology schema (classes like Movie, Actor, Director; properties like hasTitle, hasReleaseYear).
Populate it with sample data or fetch real movie details from DBpedia (e.g., for films like Inception, The Dark Knight).
Perform local and federated SPARQL queries to retrieve insights (e.g., movies released after 2000).
Interact via a simple UI (Tkinter-based app for fetching data and running queries).

It's ideal for educational purposes, semantic web coursework, or as a foundation for movie recommendation systems, knowledge graphs, or AI-driven film analysis.
Features

Ontology Creation: Define classes, subclasses, object/data properties, and axioms using OWLReady2.
Data Population: Add manual samples or automate bulk imports from DBpedia (supports 10+ movies like Oppenheimer, Interstellar).
Reasoning: Use HermiT reasoner to infer relationships (e.g., inverses like actedIn ↔ hasActor).
Querying: Execute SPARQL queries locally or federated with DBpedia for enriched results.
UI Integration: Basic Tkinter app for user input (movie names for fetching, custom SPARQL for querying).
Extensibility: Easily add more movies, properties, or integrate other RDF sources.
Cross-Platform: Runs on Windows/macOS/Linux with Python 3.8+.

Installation
Prerequisites

Python 3.8 or higher (download from python.org).
Java (for OWLReady2 reasoning; download from oracle.com or adoptium.net).

Steps

Clone the repository:textgit clone https://github.com/Sankalp774/Semantic-movies-ontology-project.git
cd movies-ontology-project
Install dependencies:textpip install owlready2 rdflib SPARQLWrapper(For UI: Tkinter is built-in with Python; no extra install needed.)
(Optional) Install Protégé for ontology visualization: Download from protege.stanford.edu.

Usage
1. Create and Populate Ontology
Run movies_ontology.py to define classes/properties and add sample data (e.g., Inception).
textpython movies_ontology.py
This generates movies_ontology.owl.
2. Integrate DBpedia Data
Run integrate_dbpedia.py or add_movies_dbpedia.py to fetch details for specific movies (e.g., The Dark Knight, Oppenheimer).
textpython add_movies_dbpedia.py
Updates the OWL file with linked data.
3. Query the Ontology
Run query_ontology.py for example SPARQL queries (e.g., movies after 2000).
textpython query_ontology.py
4. Run the UI App
Launch the Tkinter app for interactive fetching and querying:
textpython app_tkinter.py

Enter a movie name (e.g., "Interstellar") and click "Fetch from DBpedia" to integrate data.
Input a SPARQL query (e.g., SELECT ?actor WHERE { :Inception :hasActor ?actor }) and click "Run SPARQL Query" for results.

Example SPARQL Query
textPREFIX : <http://example.org/movies_ontology.owl#>
SELECT ?movie ?title ?year WHERE {
    ?movie a :Movie .
    ?movie :hasTitle ?title .
    ?movie :hasReleaseYear ?year .
    FILTER (?year > 2000)
}
Project Structure
textmovies-ontology-project/
├── movies_ontology.py          # Ontology creation and sample data
├── integrate_dbpedia.py       # Single movie DBpedia integration
├── add_movies_dbpedia.py      # Bulk movie integration (10+ movies)
├── query_ontology.py          # SPARQL query examples
├── app_tkinter.py             # Tkinter UI for interaction
├── movies_ontology.owl        # Generated OWL file (git-ignored by default)
├── README.md                  # This file
└── requirements.txt           # Dependencies list
Contributing
Contributions are welcome! To contribute:

Fork the repo.
Create a feature branch (git checkout -b feature/new-feature).
Commit changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature/new-feature).
Open a Pull Request.

Please ensure code follows PEP8 style and includes tests/comments.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

Inspired by semantic web tutorials and DBpedia resources.
Thanks to xAI for guidance in project development.
Libraries: OWLReady2, RDFLib, SPARQLWrapper.

For issues or suggestions, open a GitHub issue. Happy semantic querying! 🎥
