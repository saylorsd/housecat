import os

from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Connects CKAN datastore with postgres FDW"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with connection.cursor() as cur:
            cur.execute('CREATE EXTENSION IF NOT EXISTS postgres_fdw;')

            cur.execute(f'''
                CREATE USER {os.environ.get("MAPS_DB_USER")} 
                WITH PASSWORD '{os.environ.get("MAPS_DB_PASSWORD")}' 
            ''')

            cur.execute(f'GRANT CONNECT ON DATABASE {os.environ.get("DJANGO_DB_NAME")} TO {os.environ.get("MAPS_DB_USER")}')
            cur.execute(f'GRANT USAGE ON SCHEMA public TO {os.environ.get("MAPS_DB_USER")}')

            # use FDW to connect to remote CKAN datastore
            query = f"""
                CREATE SERVER IF NOT EXISTS datastore
                FOREIGN DATA WRAPPER postgres_fdw
                OPTIONS (
                    host '{os.environ.get('DATASTORE_HOST')}', 
                    dbname '{os.environ.get('DATASTORE_NAME')}', 
                    port '{os.environ.get('DATASTORE_PORT')}'
                );
            """
            print(query)
            cur.execute(query)

            # map our user to the read-only account on CKAN
            query = f"""
                CREATE USER MAPPING IF NOT EXISTS FOR {os.environ.get('DJANGO_DB_USER')}
                SERVER datastore
                OPTIONS (user '{os.environ.get('DATASTORE_USER')}', password '{os.environ.get('DATASTORE_PASSWORD')}');
            """
            print(query)
            cur.execute(query)

            query = """
                CREATE TYPE public.nested AS
                (
                    json  json,
                    extra text
                );
            """
            print(query)
            cur.execute(query)

            query = f"""
                 -- import (or refresh) the datastore's public shema into a local one
                DROP SCHEMA IF EXISTS datastore CASCADE;
                CREATE SCHEMA IF NOT EXISTS datastore; -- the local one
                IMPORT FOREIGN SCHEMA public
                FROM SERVER datastore INTO datastore;
                
                -- give the django db user privileges to the linked schema
                GRANT USAGE ON FOREIGN SERVER datastore TO {os.environ.get('DJANGO_DB_USER')};
                GRANT USAGE ON SCHEMA datastore TO {os.environ.get('DJANGO_DB_USER')};
                GRANT ALL ON ALL TABLES IN SCHEMA datastore TO {os.environ.get('DJANGO_DB_USER')};
            """
            print(query)
            cur.execute(query)
