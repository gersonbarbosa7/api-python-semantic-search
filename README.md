# API Magazine Hybrid Search Application

## Overview

This application provides a robust hybrid search functionality using FastAPI, enabling users to search through a database of magazines by keywords or semantic vectors. The architecture is designed for scalability and performance, making it suitable for handling large datasets efficiently.

## Architecture

The architecture of this application is built around a microservices approach, allowing independent scaling and deployment of components. Here are the key components:

- **FastAPI**: The web framework used for building the API, providing high performance and easy integration with async operations.
- **PostgreSQL**: The relational database that stores magazine information and content. It includes a vector extension for semantic search.
- **Sentence Transformers**: Used to generate vector representations of the content for enhanced semantic search capabilities.
- **Redis (optional)**: Implemented for caching responses, improving the application's response time for frequent queries.
- **Docker (optional)**: Containerization of the application for easy deployment and management.

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
Python 3.8 or higher
PostgreSQL 12 or higher
Redis (optional, for caching)

##
<tab><tab>code/text here
