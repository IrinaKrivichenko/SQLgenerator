# SQLgenerator

## Introduction

SQLgenerator is a versatile console-based tool that simplifies user access to database.
SQLgenerator empowers users to perform various database operations with ease, regardless of their language proficiency or SQL expertise. Whether you need to insert, select, delete, or update data, SQLgenerator simplifies the process and enhances the accessibility of database management tasks. Results are conveniently displayed in the console for immediate review.

Key Features:
- **Multilingual Support**: SQLgenerator supports interactions in 15 different languages, allowing users to input questions and queries in their preferred language.
- **Query Types**: SQLgenerator supports a wide range of SQL query types, including INSERT, SELECT, DELETE, and UPDATE queries.
- **Query Generation**: Based on user input, SQLgenerator generates the corresponding SQL query, making it accessible to users who may not be familiar with SQL syntax.
- **Query Execution**: SQLgenerator executes the generated SQL query on its own database and provides the query's execution results directly in the console.

## Installation

### Prerequisites

Before you begin, please ensure that your system meets the following resource requirements:

- CPU: At least 1 core.
- RAM: At least 2GB of RAM.
- Docker: Make sure you have Docker installed on your system.

### Follow these steps to set up and run SQLgenerator using Docker

1. Create a `.env` file in the project directory.
2. Add your OpenAI API key as an environment variable in the `.env` file using the following format:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```
3. Open your terminal and navigate to the directory containing the project files, including the Dockerfile:
   ```bash
   cd /path/to/sqlgenerator-project
   ```
4. Build the Docker image using the following command:
   ```bash
   docker build -t sqlgenerator:1.0 -f Dockerfile .
   ```
5. Use the following command to run the SQLgenerator container:

   ```bash
   docker run -it sqlgenerator:1.0
   ```
6. Now you can enter messages via your keyboard in the console application.
     
## Technical details

SQLgenerator leverages the RAG (Retrieval-Augmented Generation) technique in conjunction with the power of OpenAI's GPT-4 language model for effective database interaction.

### The RAG (Retrieval-Augmented Generation)

The RAG technique enhances natural language understanding and interaction with databases through a series of coordinated steps:

1. **User Query**: The process begins when a user submits a natural language query or question to SQLgenerator.
2. **Encoding**: SQLgenerator employs an encoder, specifically the Sentence Transformers library with the `distiluse-base-multilingual-cased-v1` model. This encoder transforms the user's text-based query into a high-dimensional vector representation.
3. **Database Retrieval**: The encoded user query is used to search the database of pre-existing SQL queries. SQLgenerator retrieves SQL queries from its database that are semantically similar to the user's input. Vector search assesses the relevance of the retrieved SQL queries to the user's query. It selects the most suitable queries based on semantic similarity and context.
4. **Query Generation**: In cases where the retrieved queries are not sufficiently refined or when the user's question demands it, SQLgenerator generates new SQL queries. This generation step leverages OpenAI's GPT-4 language model to create SQL queries that align precisely with the user's intent and context.
5. **SQL Execution**: The generated SQL queries are executed on SQLgenerator's own SQLite database. The system interacts with the database, retrieves data, and performs the specified operations.
6. **User Interaction**: SQLgenerator provides the user with the relevant generated SQL queries, , along with the results of SQL execution. The user can review the results in the console and interact further with the database if needed.

By following these steps, SQLgenerator ensures that users receive accurate, contextually relevant SQL queries in response to their natural language queries. The RAG technique simplifies the process of interacting with the database, making it accessible even to users without prior SQL knowledge.

### Database Schema

SQLgenerator is designed to work seamlessly with a predefined SQLite database schema consisting of 6 tables filled with test data, which it creates itself.
![Database Schema](https://github.com/IrinaKrivichenko/SQLgenerator/blob/master/img/db_scheme.png?raw=true)

### Folder Structure

Here's an overview of the project's folder structure:

- .gitignore              # Ignore files and folders for version control
- database.py             # Database creation and SQL query execution
- Dockerfile              # Docker configuration for containerization
- main.py                 # Main program for user interaction
- openai_connection.py    # OpenAI GPT-4 integration for generating SQL queries
- requirements.txt        # List of Python dependencies
- search.py               # Semantic search module for SQL queries
- data/                   # Folder containing SQL query files
- img/                    # Folder for project images
- README.md               # Project documentation (you are here)

- ## Alternative Approaches Considered

During the initial project planning, several alternative approaches were considered to address user queries and database interactions. These approaches were evaluated based on the complexity of the underlying language needs.

### Approach 1: Lightweight Word2Vec Encoding

**Key Features:**
- Language: English-only queries.
- Query Types: Limited to database selection (only SELECT queries).

**Solution:**
- Utilized a lightweight Word2Vec encoding model.
- The Word2Vec model was trained on database table and field names for query generation.

**Solution Pros:**
- Lightweight and efficient model.

**Solution Cons:**
- Hard restriction to the questions users can ask.

### Approach 2 (Chosen One): Advanced Multilingual Model

**Key Features:**
- Language: Supported multiple languages, including languages with variable word forms (e.g., Russian).
- Query Types: Handling synonyms and various query types (e.g., "add" and "insert," "select," "return," and "retrieve").

**Solution:**
- Leveraged the pretrained distiluse-base-multilingual-cased-v1 model, which supports 15 languages ([source](https://www.sbert.net/docs/pretrained_models.html)).

**Solution Pros:**
- Multilingual support.
- Robust handling of synonyms.
- Versatile query generation capabilities.

**Solution Cons:**
- The model consumes more memory and computational resources.

### Approach 3: Solving Advanced Language Needs with a Hybrid Solution

**Solution:**
- A hybrid solution combining the lightweight Word2Vec encoding model with GPT-4 chat interactions.
- Focused on maintaining the lightweight nature of the encoding model while enhancing query generation.
- Utilized GPT-4 to expand and rephrase user queries based on a specified vocabulary.

**Solution Pros:**
- Maintains a lightweight model while benefiting from advanced query generation.
- Provides flexibility in query generation and handling of specific vocabulary.

**Solution Cons:**
- Requires additional requests to GPT-4.

These alternative approaches were carefully evaluated, considering factors like language support, synonym handling, and model complexity. Ultimately, the project adopted the second approach, leveraging the distiluse-base-multilingual-cased-v1 model for its ability to handle a wide range of languages and query types effectively.
