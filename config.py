from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('PSQL_USER')
password = os.getenv('PSQL_PASSWORD')
host = os.getenv('PSQL_HOST')
db = os.getenv('PSQL_NAME')
port = os.getenv('PSQL_PORT')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_db = os.getenv('REDIS_DB')
api_key = os.getenv('API_KEY')