import os
import urllib.request
from urllib.error import URLError

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

from housing_data.models import ProjectIndex


def refresh_tile_index():
    """ Signal tile server to register new view """
    try:
        urllib.request.urlopen(f"http://{settings.MARTIN_HOST}/index.json")
    except URLError:
        pass


def as_geometry_query(query: 'Query'):
    """
    Removes casting of geometries to byte arrays as necessary for what django does
     but not useful as a raw postgis query
    :param query: QuerySet Query object to modify
    """
    return str(query).replace('::bytea', '')


def as_tile_server_query(query: 'Query'):
    import re
    query_str = as_geometry_query(query)
    return re.sub(r',\s*\"geo_adminregion\".\"mini_geom\"\s*,', ',',
                  re.sub(r',\s*\"geo_adminregion\".\"geom\"\s*,', ',', query_str))


class Command(BaseCommand):
    help = "Handles scripting that needs to be done to initialize public housing data."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # create map view for use in tile server
        print('Adding map view of all public housing projects.')
        view_name = f'maps.{settings.PUBLIC_HOUSING_PROJECT_LAYER_VIEW}'
        source_table = ProjectIndex._meta.db_table

        view_query = as_tile_server_query(f"""
            SELECT *
            FROM (
                SELECT 
                id, property_id, hud_property_name, property_street_address, municipality_name, city,
                zip_code, units, scattered_sites, latitude, longitude, census_tract, crowdsourced_id, house_cat_id, status, 
                funding_category, max_units,
                ST_Transform(ST_SetSRID(ST_Point(longitude::numeric, latitude::numeric), 4326), 3857)::geometry(point,3857) as geom_webmercator
                --- ST_SetSRID(ST_Point(longitude::numeric, latitude::numeric), 4326)::geometry(point,4326) as geom
                
                FROM "datastore"."{source_table}" 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            ) source_table
        """.lstrip())

        with connection.cursor() as cursor:
            print(f"""CREATE SCHEMA IF NOT EXISTS maps""")
            print(f"""DROP MATERIALIZED VIEW IF EXISTS {view_name}""")
            print(f"""CREATE MATERIALIZED VIEW {view_name} AS {view_query}""")
            print(f"""GRANT SELECT ON {view_name} TO {os.environ.get('MAPS_DB_USER')};""")

            cursor.execute(f"""CREATE SCHEMA IF NOT EXISTS maps""")
            cursor.execute(f"""DROP MATERIALIZED VIEW IF EXISTS {view_name}""")
            cursor.execute(f"""CREATE MATERIALIZED VIEW {view_name} AS {view_query}""")
            cursor.execute(f"""GRANT SELECT ON {view_name} TO {os.environ.get('MAPS_DB_USER')};""")

        print('Projects map view added!')
        refresh_tile_index()
