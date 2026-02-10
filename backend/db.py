import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="lab_archive",
        user="postgres",
        password="VRinstitute",
        port=5432
    )
