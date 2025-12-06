import tkinter as tk
from tkinter import messagebox, scrolledtext
from owlready2 import *
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import threading

# Check and create ontology if it doesn't exist
if not os.path.exists("movies_ontology.owl"):
    # Create a new ontology
    onto = get_ontology("http://example.org/movies_ontology.owl")

    with onto:
        # Define classes
        class Movie(Thing):
            pass
        
        class Person(Thing):
            pass
        
        class Actor(Person):
            pass
        
        class Director(Person):
            pass
        
        class Genre(Thing):
            pass
        
        # Define properties
        class hasTitle(Movie >> str, FunctionalProperty):
            pass
        
        class hasReleaseYear(Movie >> int, FunctionalProperty):
            pass
        
        class hasGenre(Movie >> Genre):
            pass
        
        class hasDirector(Movie >> Director):
            pass
        
        class hasActor(Movie >> Actor):
            pass
        
        class actedIn(Actor >> Movie):
            inverse = hasActor
        
        class directed(Director >> Movie):
            inverse = hasDirector

    # Add sample data (optional but recommended for testing)
    with onto:
        action = Genre("Action")
        sci_fi = Genre("SciFi")
        christopher_nolan = Director("ChristopherNolan")
        leonardo_dicaprio = Actor("LeonardoDiCaprio")
        inception = Movie("Inception")
        inception.hasTitle = "Inception"
        inception.hasReleaseYear = 2010
        inception.hasGenre = [action, sci_fi]
        inception.hasDirector = [christopher_nolan]
        inception.hasActor = [leonardo_dicaprio]
        leonardo_dicaprio.actedIn.append(inception)

    # Run reasoning and save
    sync_reasoner()
    onto.save(file="movies_ontology.owl", format="rdfxml")
    print("Ontology file created and saved!")

# Load the ontology
onto = get_ontology("movies_ontology.owl").load()

# Function to query DBpedia and integrate (simplified)
def fetch_from_dbpedia(movie_name):
    if not movie_name:
        return "Please enter a movie name."
    
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    dbpedia_resource = movie_name.replace(' ', '_')
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
        return f"Error querying DBpedia: {str(e)}"
    
    # Integrate into ontology
    with onto:
        movie_iri = movie_name.replace(' ', '_')
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
        sync_reasoner()
        onto.save(file="movies_ontology.owl", format="rdfxml")
        return f"Data for '{movie_name}' fetched from DBpedia and integrated into the ontology!"
    else:
        return f"No data found for '{movie_name}' on DBpedia."

# Function to run custom SPARQL query
def run_custom_sparql(sparql_query):
    if not sparql_query:
        return "Please enter a SPARQL query."
    
    try:
        # Ensure prefix is included if not in query
        if "PREFIX :" not in sparql_query:
            sparql_query = "PREFIX : <http://example.org/movies_ontology.owl#>\n" + sparql_query
        results = list(onto.world.sparql(sparql_query))
        output = ""
        if results:
            for result in results:
                output += str(result) + "\n"
        else:
            output = "No results found."
        return output
    except Exception as e:
        return f"Error running SPARQL query: {str(e)}"

# Tkinter GUI
def main():
    root = tk.Tk()
    root.title("Movies Ontology App")
    root.geometry("600x400")

    # Movie Name Input for Fetch
    tk.Label(root, text="Movie Name (e.g., Inception):").pack(pady=5)
    movie_entry = tk.Entry(root, width=50)
    movie_entry.pack()

    # SPARQL Query Input
    tk.Label(root, text="SPARQL Query (e.g., SELECT ?actor WHERE { :Inception :hasActor ?actor }):").pack(pady=5)
    query_entry = tk.Text(root, width=50, height=5)
    query_entry.pack()

    # Output Area
    output_text = scrolledtext.ScrolledText(root, width=70, height=15)
    output_text.pack(pady=10)

    # Buttons
    def fetch_movie():
        movie_name = movie_entry.get().strip()
        result = fetch_from_dbpedia(movie_name)
        output_text.insert(tk.END, f"Fetch Result:\n{result}\n\n")

    def run_query():
        sparql_query = query_entry.get("1.0", tk.END).strip()
        result = run_custom_sparql(sparql_query)
        output_text.insert(tk.END, f"Query Result:\n{result}\n\n")

    tk.Button(root, text="Fetch from DBpedia", command=fetch_movie).pack(side=tk.LEFT, padx=20)
    tk.Button(root, text="Run SPARQL Query", command=run_query).pack(side=tk.RIGHT, padx=20)

    root.mainloop()

if __name__ == "__main__":
    main()