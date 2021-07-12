import zipfile
from django.core.management.base import BaseCommand
from work_db import services
from work_db.models import Bank


class Command(BaseCommand):
    help = 'Adding banks to the database'

    def handle(self, *args, **options):
        f = services.load()
        with zipfile.ZipFile(f.file_field.name) as zf:
            zf.extract('bnkseek.txt', 'media/')
        with open('media/bnkseek.txt') as file:
            for line in file:
                _, city, _, name, _, bik, account = line.split('\t')  # 5 - bik
                account = account.split('\n')
                Bank.objects.get_or_create(
                    city=city,
                    name=name,
                    bik=bik,
                    account=account[0],
                )
