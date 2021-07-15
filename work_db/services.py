import io
import zipfile

import requests

from django.conf import settings
from django.core.management.base import CommandError
from work_db.models import Bank


class WorkWithBanks:

    @staticmethod
    def get_Content():
        response = requests.get(settings.URL)
        if response.status_code != requests.codes.ok:
            raise CommandError('Cannot download file')
        return response.content

    @staticmethod
    def read_zip_bytes(content):
        b_bytes = io.BytesIO(content)
        with zipfile.ZipFile(b_bytes) as zf:
            with zf.open('bnkseek.txt') as file:
                byte = file.read()
                text = byte.decode('windows-1251')
        return text

    @staticmethod
    def save_InfoBanks(text):
        text = text.split('\n')
        text.pop(-1)  # delete because last line text = ['']
        for line in text:
            line = line.split('\t')
            _, city, _, name, _, bik, account = line
            Bank.objects.get_or_create(
                city=city,
                name=name,
                bik=bik,
                account=account,
            )

    @staticmethod
    def load_and_save_infoBank():
        content = WorkWithBanks.get_Content()
        text = WorkWithBanks.read_zip_bytes(content)
        WorkWithBanks.save_InfoBanks(text)
