from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Truncates django_migrations table")
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE 'django_migrations'")
