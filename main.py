from database import create_db, execute_sql_queries, DatabaseExecuteError
from openai_connection import ask_for_query, correct_query
from search import SemanticSearcher

if __name__ == "__main__":
    create_db()
    searcher = SemanticSearcher()
    while True:
        print("Please enter your question to book database ")
        print("Type 'quit' to finish the program): ")
        user_input =""
        while not user_input:  user_input = input()
        if user_input.lower() == 'quit':
            print("Exiting the program.")
            break
        sql_examples = searcher.search(user_input)
        query_to_execute = ask_for_query(user_input, sql_examples)
        error_messages = []
        while True:
            try:
                execute_sql_queries(query_to_execute)
                break
            except DatabaseExecuteError as e:
                error_messages.append(str(e))
                if len(error_messages)>10:
                    print(f"Sorry I can not find answer to the question {user_input}")
                query_to_execute = correct_query(user_input, sql_examples, error_messages)