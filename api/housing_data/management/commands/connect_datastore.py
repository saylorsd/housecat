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

            maps_user = os.environ.get("MAPS_DB_USER")
            maps_password = os.environ.get("MAPS_DB_PASSWORD")

            # cur.execute(f"""
            # DROP SERVER IF EXISTS datastore CASCADE;
            # """)
            #
            # cur.execute(f"""
            # DROP SCHEMA IF EXISTS datastore;
            # """)

            cur.execute(f'''
                DO
                $do$
                BEGIN
                   IF EXISTS (
                      SELECT FROM pg_catalog.pg_roles
                      WHERE  rolname = '{maps_user}') THEN
                
                      RAISE NOTICE 'Role "{maps_user}" already exists. Skipping.';
                   ELSE
                      CREATE ROLE {maps_user} LOGIN PASSWORD '{maps_password}';
                   END IF;
                END
                $do$;
            ''')

            cur.execute(f'GRANT CONNECT ON DATABASE {os.environ.get("DJANGO_DB_NAME")} TO {os.environ.get("MAPS_DB_USER")}')
            cur.execute(f"""CREATE SCHEMA IF NOT EXISTS maps""")
            cur.execute(f'GRANT USAGE ON SCHEMA maps TO {os.environ.get("MAPS_DB_USER")}')

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
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'nested') THEN
                        CREATE TYPE public.nested AS
                        (
                            json  json,
                            extra text
                        );
                    END IF;
                END$$;
            """
            print(query)
            cur.execute(query)

            query = f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'datastore') THEN
                         -- import (or refresh) the datastore's public shema into a local one
                        DROP SCHEMA IF EXISTS datastore CASCADE;
                        CREATE SCHEMA IF NOT EXISTS datastore; -- the local one
                        IMPORT FOREIGN SCHEMA public
                            LIMIT TO (
                            "1885161c-65f3-4cb2-98aa-4402487ae888",
                            "ba6b156f-82fe-41b0-83b9-c17540836598",
                            "25c0e399-0ad8-42cf-8899-e6f35faf1187",
                            "64449027-404c-48fb-a9a4-75e9e8d14188",
                            "e5b27187-b134-4050-8101-db4e19ffdb30",
                            "f71eb9f3-c413-47a3-8592-af447fe93020",
                            "6234dd27-79f4-43d3-b098-19f12692ce55",
                            "6803b4c9-df5d-4ef0-8c33-43e9feaff0a2",
                            "931d45da-f791-46c4-998b-60bafa904b36",
                            "b3ff057c-1518-4a34-a004-39d3d49a5ad7",
                            "d5275180-13f1-460b-b933-aab6afc2966e",
                            "ad49ed19-1122-4f9d-a3c2-491f36a293f4",
                            "a768bb6b-9d1e-463f-9711-651fedf971fb",
                            "7cc60ad7-b209-46f2-bdda-9755d8a42461",
                            "6269354d-bac6-4c2e-ad07-2dd7e2ab252e",
                            "7eeabaa5-bd27-4df0-9459-d56acd826451",
                            "127d12cd-9718-4b44-9cc1-2673a1a50dba",
                            "438a732d-c86f-4a06-bff8-61eb6ebe7328",
                            "c099b5b9-df5d-4380-9cb3-6c45b03ac8b4",
                            "7d4ad5ee-7229-4aa6-b3a2-69779fe5c52a",
                            "f6a77bc1-e3c1-403a-86bc-40b906124af6",
                            "fcb7cd5d-71f6-4f38-bb78-a3002be47ed6",
                            "a6b93b7b-e04e-42c9-96f9-ee788e4f0978",
                            "afba564f-cc68-42f0-b37b-fc8d70e8ef47",
                            "ecdbf89a-bbe7-4e82-b902-d6b774758d3a",
                            "0b6a109e-b1f1-4064-8f42-eeb5355dc9df",
                            "e82411f8-623d-4336-b714-ecdded80703d"
                            )
                            FROM SERVER datastore INTO datastore;

                        
                        -- give the django db user privileges to the linked schema
                        GRANT USAGE ON FOREIGN SERVER datastore TO {os.environ.get('DJANGO_DB_USER')};
                        GRANT USAGE ON SCHEMA datastore TO {os.environ.get('DJANGO_DB_USER')};
                        GRANT ALL ON ALL TABLES IN SCHEMA datastore TO {os.environ.get('DJANGO_DB_USER')};
                    END IF;
                END$$;
            """
            print(query)
            cur.execute(query)
