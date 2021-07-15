from django.core.management.base import BaseCommand
from work_db.services import WorkWithBanks


class Command(BaseCommand):
    help = 'Adding banks to the database'

    def handle(self, *args, **options):
        WorkWithBanks.load_and_save_infoBank()
