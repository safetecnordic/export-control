from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TEXT SEARCH DICTIONARY english_stem_nostop (
            Template = snowball
            , Language = english
            );
            """
        )
        cursor.execute(
            """
            CREATE TEXT SEARCH CONFIGURATION public.english_nostop ( COPY = pg_catalog.english );
            """
        )
        cursor.execute(
            """
            ALTER TEXT SEARCH CONFIGURATION public.english_nostop
            ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, hword, hword_part, word WITH english_stem_nostop;
            """
        )
