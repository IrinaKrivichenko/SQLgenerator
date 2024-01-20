from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

class SemanticSearcher:
    # based on this article it is more efficient to search for chunks with create and select queries separately
    # https://github.com/vanna-ai/vanna/blob/main/papers/ai-sql-accuracy-2023-08-17.md#setting-up-architecture-of-the-test
    QUERY_CATEGORIES = {
        "create": {"k": 4},
        "select": {"k": 9},
        "insert": {"k": 1},
        "update": {"k": 1}
    }

    def __init__(self, datafolder='./data/'):
        self.model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
        self.sql_queries = {category: self.prepare_sql_category(category, datafolder)
                            for category in SemanticSearcher.QUERY_CATEGORIES}

    def prepare_sql_category(self, category_name, datafolder):
        files_in_folder = os.listdir(datafolder)
        target_file = next((f for f in files_in_folder if (category_name in f) and f.endswith(".txt")), None)
        target_file = os.path.join(datafolder, target_file)
        # Reading SQL queries from a file
        with open(target_file, 'r', encoding='utf-8') as file:
            sql_queries = file.readlines()
        # Generate embeddings for the queries
        embeddings = self.model.encode(sql_queries, show_progress_bar=True)
        # Create a Faiss index
        index = faiss.IndexFlatL2(embeddings.shape[1])
        # Convert embeddings to a NumPy array and add them to the index
        embeddings_np = np.array(embeddings, dtype=np.float32)
        index.add(embeddings_np)
        sql_category = {"sql_queries": sql_queries, "index": index}
        return sql_category

    def search(self, question):
        # Generate an embedding for the question
        question_embedding = self.model.encode(question, show_progress_bar=False)
        query_embedding_np = np.array([question_embedding], dtype=np.float32)
        result = ""
        # Perform a vector search in all the categories separately:
        for category in self.sql_queries:
            k = SemanticSearcher.QUERY_CATEGORIES[category]['k']  # Number of nearest neighbors to retrieve
            index = self.sql_queries[category]['index']
            # Search for the nearest neighbors
            distances, rows = index.search(query_embedding_np, k)
            # Print the nearest neighbors
            # print(f"category: {category}")
            for distance, r in zip(distances[0], rows[0]):
                text = self.sql_queries[category]['sql_queries'][r]
                # print(f"Distance={distance}, Text={text}")
                # Use the str.join() method to concatenate the strings with ";"
                result = ";".join([result, text])
        return result

if __name__ == "__main__":
    searcher = SemanticSearcher()
    searcher.search("FREQUENCY")