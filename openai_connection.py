import openai
from dotenv import load_dotenv
import os

def ask_gpt(user_question, sql_examples):
    system_content = """
                I would like you to create SQL queries based on user questions.
                If you have multiple questions, please separate them with semicolons.
                If it is an INSERT query, and you don't know the value for a field, you can omit it from the query
                """
    system_content = "Here is relevant queries to the same database: ".join([system_content, sql_examples])
    # Load environment variables from .env file
    load_dotenv()
    # Get API key from environment variable
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(
        model="gpt-4",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_question}
        ]
    )
    return response.choices[0].message['content']