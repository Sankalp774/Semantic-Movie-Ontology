from owlready2 import *

# Load the ontology (assumes movies_ontology.owl exists in the same directory)
onto = get_ontology("movies_ontology.owl").load()

# Example local SPARQL query: Find movies released after 2000
results = list(onto.world.sparql("""
    PREFIX : <http://example.org/movies_ontology.owl#>
    SELECT ?movie ?title ?year WHERE {
        ?movie a :Movie .
        ?movie :hasTitle ?title .
        ?movie :hasReleaseYear ?year .
        FILTER (?year > 2000)
    }
"""))

# Print the results
print("Query Results:")
if results:
    for result in results:
        print(f"Movie IRI: {result[0]},\nTitle: {result[1]},\nYear: {result[2]}")
else:
    print("No results found.")

# Optional: Add more queries here
# For example, find actors in a specific movie
movie_name = "Inception"  # Change as needed
results_actors = list(onto.world.sparql(f"""
    PREFIX : <http://example.org/movies_ontology.owl#>
    SELECT ?actor WHERE {{
        :{movie_name} :hasActor ?actor .
    }}
"""))

print(f"\nActors in {movie_name}:")
if results_actors:
    for result in results_actors:
        print(f"Actor IRI: {result[0]}")
else:
    print("No actors found.")

# Federated query example (local + DBpedia)
# Uncomment and run if needed (requires internet)
# results_fed = list(onto.world.sparql("""
#     PREFIX : <http://example.org/movies_ontology.owl#>
#     SELECT ?movie ?director ?wikiAbstract WHERE {
#         ?movie a :Movie .
#         ?movie :hasDirector ?director .
#         SERVICE <http://dbpedia.org/sparql> {
#             ?director dbo:abstract ?wikiAbstract .
#             FILTER (lang(?wikiAbstract) = 'en')
#         }
#     }
# """))
# 
# print("\nFederated Query Results:")
# for result in results_fed:
#     print(f"Movie: {result[0]}, Director: {result[1]}, Abstract: {result[2]}")