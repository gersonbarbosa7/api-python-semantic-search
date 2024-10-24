# API Magazine Hybrid Search Application

## Overview

This application provides a robust hybrid search functionality using FastAPI, enabling users to search through a database of magazines by keywords or semantic vectors. The architecture is designed for scalability and performance, making it suitable for handling large datasets efficiently.

## Architecture

The architecture of this application is built around a microservices approach, allowing independent scaling and deployment of components. Here are the key components:

- **FastAPI**: The web framework used for building the API, providing high performance and easy integration with async operations.
- **PostgreSQL**: The relational database that stores magazine information and content. It includes a vector extension for semantic search.
- **Sentence Transformers**: Used to generate vector representations of the content for enhanced semantic search capabilities.
- **Redis**: Implemented for caching responses, improving the application's response time for frequent queries.
- **Docker**: Containerization of the application for easy deployment and management.

## Flows

### 1. User Queries

Users can perform searches by sending a POST request to the `/search` endpoint with the following JSON payload:

```json
{
  "query": "Mary",
  "search_type": "keywords"
}
```

or

```json
{
  "query": "Tell me about USA",
  "search_type": "semantic"
}
```

or

```json
{
  "query": "When Neymar back to field?",
  "search_type": "hybrid"
}
```

## Search Logic
- **Keyword Search**: The application performs a keyword search across the title, author, and content fields.
- **Semantic Search**: The application uses vector representations to perform semantic searches, returning results based on vector similarity.

## Installation Instructions

### Prerequisites
Python 3.9 or higher
PostgreSQL 12 or higher
Redis
Docker

### First of all
1 - Clone this repository to your local machine.

2 - Install the required dependencies using the following command:

If using Mac/Linux
````
python -m venv .venv
source .venv/bin/activate
````

after for all OS

```
pip install -r requirements.txt
```

3 - Run the following command to set up the database and redis (you have Docker installed, right?)
```
docker-compose up -d
```

4 - Creating your .env file using the sample:
```
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=0.0.0.0
DB_PORT=5432
```

5 - Run the script example-data/import.py to create tables and insert some data into the database:

if you using mac or linux:
```
python3 example-data/import.py
```

if using windows
```
python example-data/import.py
```

This import will insert around of 500 rows. If you want to do a hard test, please download the file:
[Complete sample json data](https://drive.google.com/file/d/1pNsb7rV61O_LkVlrp7OR8w2PP889wHD4/view?usp=share_link)

6 - Finally, Run the follow code:
```
uvicorn app.main:app --reload   
```

### USAGE: POST request to `/search` endpoint

To search the database using the `/search` endpoint, you can use the following `POST` request format. This example uses the `semantic` search type. You alse can use `keywords` or `hybrid` passing it in attribute `search_type` to see differents results.

#### Request:

**POST** `http://127.0.0.1:8000/search`

```json
{
  "query": "Is Neymar good player?",
  "search_type": "semantic"
}
```

## Endpoint details
To see details and to test, go tho the URL:
[http://12.0.0.1:8000/docs](http://12.0.0.1:8000/docs)

## Others ways
You can use [Insominio](https://insomnia.rest/download) or [Postman](https://www.postman.com) to consume the api

```
http://12.0.0.1:8000/search
```

Enjoy it!