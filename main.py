from database import create_db, execute_sql_queries
from openai_connection import ask_gpt
from search import SemanticSearcher

if __name__ == "__main__":
    create_db()
    searcher = SemanticSearcher()
    while True:
        print("Please enter your question to book database ")
        print("Type 'quit' to finish the program): ")
        user_input = input()
        if user_input.lower() == 'quit':
            print("Exiting the program.")
            break
        sql_examples = searcher.search(user_input)
        query_to_execute = ask_gpt(user_input, sql_examples)
        execute_sql_queries(query_to_execute)