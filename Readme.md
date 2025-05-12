
# API RESTful avec Flask et Neo4j

## Introduction

Ce projet consiste à créer une API RESTful en Python utilisant Flask et Neo4j pour gérer des utilisateurs, des posts, des commentaires et des relations d'amitié entre utilisateurs. L'API permet de créer, lire, mettre à jour et supprimer des utilisateurs, posts, commentaires et gérer les relations d'amitié.

## Prérequis

Avant de démarrer, vous devez avoir installé les outils suivants :
- Python 3.8+ (ou une version plus récente)
- Docker
- Neo4j (via Docker ou installation locale)
- pip pour installer les dépendances

## Installation

### 1. Créer un environnement virtuel

Créez un environnement virtuel Python pour installer les dépendances.

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Linux/MacOS
venv\Scripts\activate  # Sur Windows
```

### 2. Installer les dépendances

Installez les bibliothèques Python nécessaires à l'aide de `pip`.

```bash
pip install -r requirements.txt
```

### 4. Lancer Neo4j avec Docker

Si vous n'avez pas installé Neo4j, vous pouvez le faire en utilisant Docker. Exécutez la commande suivante pour démarrer un conteneur Neo4j.

```bash
docker run --name neo4j -d \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j
```

Cela va lancer un serveur Neo4j accessible à `http://localhost:7474` avec les identifiants par défaut `neo4j` et `password`.

### 5. Lancer l'application Flask

Assurez-vous que le serveur Neo4j est en cours d'exécution, puis lancez l'application Flask avec la commande suivante.

```bash
python app.py
```

Cela démarrera le serveur Flask, généralement accessible à `http://localhost:5000`.

## Utilisation de l'API

Voici un résumé des principales routes disponibles dans l'API :

### Utilisateurs

* **GET /users** : Récupérer la liste des utilisateurs.
* **POST /users** : Créer un nouvel utilisateur.
* **GET /users/\:id** : Récupérer un utilisateur par son ID.
* **PUT /users/\:id** : Mettre à jour un utilisateur.
* **DELETE /users/\:id** : Supprimer un utilisateur.
* **GET /users/\:id/friends** : Récupérer la liste des amis d'un utilisateur.
* **POST /users/\:id/friends** : Ajouter un ami à un utilisateur.
* **DELETE /users/\:id/friends/\:friendId** : Supprimer un ami.
* **GET /users/\:id/friends/\:friendId** : Vérifier si deux utilisateurs sont amis.
* **GET /users/\:id/mutual-friends/\:otherId** : Récupérer les amis en commun.

### Posts

* **GET /posts** : Récupérer tous les posts.
* **GET /posts/\:id** : Récupérer un post par son ID.
* **GET /users/\:id/posts** : Récupérer les posts d'un utilisateur.
* **POST /users/\:id/posts** : Créer un post pour un utilisateur.
* **PUT /posts/\:id** : Mettre à jour un post.
* **DELETE /posts/\:id** : Supprimer un post.
* **POST /posts/\:id/like** : Ajouter un like à un post.
* **DELETE /posts/\:id/like** : Retirer un like d'un post.

### Commentaires

* **GET /posts/\:id/comments** : Récupérer les commentaires d'un post.
* **POST /posts/\:id/comments** : Ajouter un commentaire à un post.
* **DELETE /posts/\:postId/comments/\:commentId** : Supprimer un commentaire.
* **GET /comments/\:id** : Récupérer un commentaire par son ID.
* **PUT /comments/\:id** : Mettre à jour un commentaire.
* **POST /comments/\:id/like** : Ajouter un like à un commentaire.
* **DELETE /comments/\:id/like** : Retirer un like d'un commentaire.

## Test de l'API avec Postman ou curl

Voici quelques exemples pour tester l'API avec **Postman** ou **curl**.

### Créer un utilisateur

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

### Récupérer la liste des utilisateurs

```bash
curl http://localhost:5000/users
```

### Créer un post

```bash
curl -X POST http://localhost:5000/users/1/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Mon premier post", "content": "Contenu du post"}'
```

### Ajouter un like à un post

```bash
curl -X POST http://localhost:5000/posts/1/like \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

## Documentation supplémentaire

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Py2neo Documentation](https://py2neo.org/)
* [Neo4j Documentation](https://neo4j.com/docs/)

## Conclusion

Ce projet montre comment créer une API RESTful avec Flask et Neo4j pour gérer des utilisateurs, des posts, des commentaires, et des relations sociales. Vous pouvez étendre cette API pour ajouter d'autres fonctionnalités comme des notifications ou des fils d'actualités.

