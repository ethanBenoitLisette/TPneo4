from py2neo import Graph

# Connexion à Neo4j (remplace "password" par ton mot de passe)
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
