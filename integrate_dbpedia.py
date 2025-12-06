from owlready2 import *
from SPARQLWrapper import SPARQLWrapper, JSON

# Load the existing ontology
onto = get_ontology("movies_ontology.owl").load()

# List of 10 movies to add (replace underscores with spaces for display, but use underscores for DBpedia resources)
movies = [
    "The_Dark_Knight",
    "Oppenheimer",
    "The_Matrix",
    "Interstellar",
    "Dune_(2021_film)",  # Specify year to avoid ambiguity
    "Avatar_(2009_film)",
    "Titanic_(1997_film)",
    "Joker_(2019_film)",
    "Tenet_(film)",
    "Batman_Begins"
]

# Set up DBpedia SPARQL endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

for dbpedia_resource in movies:
    # Query for movie details
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    SELECT ?title ?releaseDate ?director ?actor ?genre WHERE {{
        dbr:{dbpedia_resource} dbo:abstract ?abstract .
        OPTIONAL {{ dbr:{dbpedia_resource} rdfs:label ?title FILTER (lang(?title) = 'en') }}
        OPTIONAL {{ dbr:{dbpedia_resource} dbo:releaseDate ?releaseDate }}
        OPTIONAL {{ dbr:{dbpedia_resource} dbo:director ?director }}
        OPTIONAL {{ dbr:{dbpedia_resource} dbo:starring ?actor }}
        OPTIONAL {{ dbr:{dbpedia_resource} dbo:genre ?genre }}
    }}
    """
    sparql.setQuery(query)
    try:
        results = sparql.query().convert()
    except Exception as e:
        print(f"Error querying DBpedia for {dbpedia_resource}: {str(e)}")
        continue
    
    # Integrate into ontology
    with onto:
        movie_iri = dbpedia_resource.replace('_', '')  # Clean IRI for local ontology (no underscores)
        movie = onto.Movie(movie_iri)
        integrated = False
        for result in results["results"]["bindings"]:
            integrated = True
            title = result.get("title", {}).get("value", "Unknown")
            year_str = result.get("releaseDate", {}).get("value", "Unknown")
            year = int(year_str[:4]) if year_str != "Unknown" and year_str else None
            director_uri = result.get("director", {}).get("value")
            actor_uri = result.get("actor", {}).get("value")
            genre_uri = result.get("genre", {}).get("value")
            
            if title != "Unknown":
                movie.hasTitle = title
            if year is not None:
                movie.hasReleaseYear = year
            if director_uri:
                director = onto.Director(IRI(director_uri))
                movie.hasDirector.append(director)
            if actor_uri:
                actor = onto.Actor(IRI(actor_uri))
                movie.hasActor.append(actor)
            if genre_uri:
                genre = onto.Genre(IRI(genre_uri))
                movie.hasGenre.append(genre)
    
    if integrated:
        print(f"Data for '{dbpedia_resource.replace('_', ' ')}' integrated!")
    else:
        print(f"No data found for '{dbpedia_resource.replace('_', ' ')}' on DBpedia.")

# Run reasoning and save updates
sync_reasoner()
onto.save(file="movies_ontology.owl", format="rdfxml")
print("All movies processed and ontology saved!")