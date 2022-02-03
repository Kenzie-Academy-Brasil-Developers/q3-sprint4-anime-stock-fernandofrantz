from os import getenv
import psycopg2

configs = {
    'host': getenv('DB_HOST'),
    'database': getenv('DB_DATABASE'),
    'user': getenv('DB_USER'),
    'password': getenv('DB_PASSWORD')
}
conn = psycopg2.connect(**configs)
