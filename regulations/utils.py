from django.db import connection


def get_formated_string(value: str, delimiter: str) -> str:
    query = f" {delimiter} ".join([f"'{word}'" for word in value.split()])
    return f"({query})"


def set_postgres_search_config() -> None:
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
