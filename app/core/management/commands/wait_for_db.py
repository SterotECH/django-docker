"""
Django Command to wait for Database to e available
"""

import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django Command to wait for database."""

    def handle(self, *args, **options):
        """Entry Point for command"""
        self.stdout.write(self.style.WARNING("Waiting for database..."))
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])  # type: ignore
                db_up = True
            except (OperationalError, Psycopg2Error):
                self.stderr.write(
                    self.style.ERROR(
                        "Database unavailable, waiting 1 second...",
                    )
                )
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database Available"))
