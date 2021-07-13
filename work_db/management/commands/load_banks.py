from django.core.management.base import BaseCommand
from work_db.services import Work_with_Banks


class Command(BaseCommand):
    help = 'Adding banks to the database'

    def handle(self, *args, **options):
        Work_with_Banks.load_and_save_arcive_of_banks(self)
