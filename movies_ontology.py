from owlready2 import *

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

# Add sample data
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
print("Ontology created, populated, and saved!")

