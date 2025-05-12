from py2neo import Graph

# Connexion à Neo4j (remplace "ui" par ton mot de passe)
graph = Graph("bolt://localhost:9001", auth=("neo4j", "ui"))
