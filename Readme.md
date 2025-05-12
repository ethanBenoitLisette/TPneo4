# 🧪 API REST avec Flask & Neo4j

Je suis encore débutant, donc tout n’est pas parfait, mais ça fonctionne normalement et ça m’aide à comprendre comment tout ça marche. 😄

---

## 🚀 Installation

### 1. Installer les dépendances Python

D’abord, il faut installer les modules nécessaires (ils sont listés dans `requirements.txt`) :

```bash
pip install -r requirements.txt
```

### 2. Lancer Neo4j avec Docker

Ensuite, j’ai utilisé Docker pour lancer Neo4j (comme ça pas besoin d’installer Neo4j sur mon ordi directement) :

```bash
docker run --name neo4j -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/ui neo4j
```

➡️ L’interface web de Neo4j est accessible ici : [http://localhost:7474](http://localhost:7474)
🧠 Identifiants par défaut : `neo4j / ui` (je les ai gardés simples pour tester)

### 3. Lancer le serveur Flask

Enfin, pour lancer l’API :

```bash
python app.py
```

➡️ L’API tourne ici : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔌 Arrêter tout proprement

### Arrêter Neo4j

```bash
docker stop neo4j
```

### Arrêter Flask

Utiliser `Ctrl + C` dans le terminal où Flask tourne.

---

## 🧪 Tester les fonctionnalités de l’API

J’ai testé tout ça avec **Postman**, mais tu peux aussi utiliser curl ou un autre outil.

---

### 1. Créer un utilisateur

**Requête :** `POST /users`

```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

**Réponse attendue :**

```json
{
  "message": "User created",
  "user": {
    "id": "...",
    "name": "Alice",
    "email": "alice@example.com",
    "created_at": "..."
  }
}
```

**Vérification dans Neo4j :**

```cypher
MATCH (u:User) RETURN u;
```

---

### 2. Créer un post pour un utilisateur

**Requête :** `POST /users/<user_id>/posts`

```json
{
  "title": "Mon premier post",
  "content": "Ceci est un test"
}
```

**Réponse attendue :**

```json
{
  "message": "Post created",
  "post": {
    "id": "...",
    "title": "Mon premier post",
    "content": "Ceci est un test",
    "created_at": "..."
  }
}
```

**Dans Neo4j :**

```cypher
MATCH (p:Post) RETURN p;
```

---

### 3. Ajouter un commentaire à un post

**Requête :** `POST /posts/<post_id>/comments`

```json
{
  "user_id": "<id_utilisateur>",
  "content": "Super post !"
}
```

**Réponse :**

```json
{
  "message": "Comment added",
  "comment": {
    "id": "...",
    "content": "Super post !",
    "created_at": "..."
  }
}
```

**Dans Neo4j :**

```cypher
MATCH (c:Comment) RETURN c;
```

---

### 4. Supprimer un utilisateur

**Requête :** `DELETE /users/<user_id>`
**Réponse :**

```json
{
  "message": "User deleted"
}
```

**Dans Neo4j :**

```cypher
MATCH (u:User {id: "<id>"}) RETURN u;
```

👉 Si rien ne s'affiche, ça veut dire qu’il est bien supprimé !

---

### 5. Supprimer un post

**Requête :** `DELETE /posts/<post_id>`
**Réponse :**

```json
{
  "message": "Post deleted"
}
```

**Dans Neo4j :**

```cypher
MATCH (p:Post {id: "<id>"}) RETURN p;
```

---

### 6. Supprimer un commentaire

**Requête :** `DELETE /comments/<comment_id>`
**Réponse :**

```json
{
  "message": "Comment deleted"
}
```

**Dans Neo4j :**

```cypher
MATCH (c:Comment {id: "<id>"}) RETURN c;
```

---

## 🧰 Comment j’ai utilisé Postman pour tester

1. J’ai installé Postman depuis [ce lien](https://www.postman.com/downloads/).
2. J’ai créé une nouvelle requête en choisissant `POST` ou `DELETE`, selon le cas.
3. Dans "Body", j’ai mis le JSON (en choisissant bien "raw" et "JSON").
4. J’ai cliqué sur "Send".
5. Ensuite, j’ai vérifié dans Neo4j si mes données étaient bien ajoutées ou supprimées.

---

## ✅ Récapitulatif rapide des routes

| Action                   | Méthode | URL                         | Vérification Cypher                        |
| ------------------------ | ------- | --------------------------- | ------------------------------------------ |
| Créer un utilisateur     | POST    | `/users`                    | `MATCH (u:User) RETURN u;`                 |
| Créer un post            | POST    | `/users/<user_id>/posts`    | `MATCH (p:Post) RETURN p;`                 |
| Ajouter un commentaire   | POST    | `/posts/<post_id>/comments` | `MATCH (c:Comment) RETURN c;`              |
| Supprimer un utilisateur | DELETE  | `/users/<user_id>`          | `MATCH (u:User {id: "<id>"}) RETURN u;`    |
| Supprimer un post        | DELETE  | `/posts/<post_id>`          | `MATCH (p:Post {id: "<id>"}) RETURN p;`    |
| Supprimer un commentaire | DELETE  | `/comments/<comment_id>`    | `MATCH (c:Comment {id: "<id>"}) RETURN c;` |

---

> Voilà ! Si jamais tu débutes comme moi, j’espère que ce README t’aidera. N’hésite pas à améliorer ce projet ou à le personnaliser ✌️
