from django.core.management.base import BaseCommand
from work_db.services import WorkWiBanks


class Command(BaseCommand):
    help = 'Adding banks to the database'

    def handle(self, *args, **options):
        WorkWiBanks.load_and_save_infoBank()
