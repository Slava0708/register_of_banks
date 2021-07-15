import io

import responses

from django.conf import settings
from django.db import connections
from django.test import TestCase

from work_db import forms
from work_db import models
from work_db.services import WorkWithBanks


class ModelBankTest(TestCase):

    @classmethod
    def setUpClass(cls):
        models.Bank.objects.create(name="Альфа Банк", bik='408934430')

    def test_bik_label(self):
        bank = models.Bank.objects.get(name="Альфа Банк")
        field_label = bank._meta.get_field('bik').verbose_name
        self.assertEqual(field_label, 'Бик')

    def test_city_label(self):
        bank = models.Bank.objects.get(id=1)
        field_label = bank._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'Город')

    def test_name_label(self):
        bank = models.Bank.objects.get(id=1)
        field_label = bank._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')

    def test_length_bik(self):
        bank = models.Bank.objects.get(id=1)
        field_label = bank._meta.get_field('bik').max_length
        self.assertEquals(field_label, 9)

    def test_blank_name(self):
        bank = models.Bank.objects.get(id=1)
        field_label = bank._meta.get_field('name').blank
        self.assertEquals(field_label, False)

    def test_blank_account(self):
        bank = models.Bank.objects.get(id=1)
        field_label = bank._meta.get_field('account').blank
        self.assertEquals(field_label, True)

    @classmethod
    def tearDownClass(cls):
        connections.close_all()


class ModelReviewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        bank1 = models.Bank.objects.create(name="Альфа Банк", bik='408934430')
        models.Review.objects.create(username="Вячеслав", review='Cool!', bank=bank1)

    def test_username_label(self):
        review = models.Review.objects.get(username="Вячеслав")
        field_label = review._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'Пользователь')

    def test_review_label(self):
        review = models.Review.objects.get(username="Вячеслав")
        field_label = review._meta.get_field('review').verbose_name
        self.assertEquals(field_label, 'Отзыв о банке')

    def test_blank_created_at(self):
        review = models.Review.objects.get(id=1)
        field_label = review._meta.get_field('created_at').blank
        self.assertEquals(field_label, True)

    def test_blank_username(self):
        review = models.Review.objects.get(id=1)
        field_label = review._meta.get_field('username').blank
        self.assertEquals(field_label, False)

    def test_max_length_username(self):
        review = models.Review.objects.get(id=1)
        field_label = review._meta.get_field('username').max_length
        self.assertEquals(field_label, 20)

    @classmethod
    def tearDownClass(cls):
        connections.close_all()


class TestForm(TestCase):

    def test_BankForm_name_label(self):
        form = forms.BankForm()
        self.assertEqual(form.fields['name'].label, "Наименование")

    def test_BankForm_bik_label(self):
        form = forms.BankForm()
        self.assertEqual(form.fields['bik'].label, "БИК")

    def test_BankForm_city_label(self):
        form = forms.BankForm()
        self.assertEqual(form.fields['city'].label, "Город")

    def test_BankForm_account_label(self):
        form = forms.BankForm()
        self.assertEqual(form.fields['account'].label, "Счет")


class ViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        for i in range(21):
            k = models.Bank.objects.create(name=str(i), bik=i)
            models.Review.objects.create(username=str(i), review=str(i + 10), bank=k)

    def test_view_url_banks_add(self):
        resp = self.client.get('/banks/add/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_bank_id(self):
        resp = self.client.get(('/banks/1/'))
        self.assertEqual(resp.status_code, 200)

    def test_view_url_bank_id_edit(self):
        resp = self.client.get('/banks/2/edit/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_bank_id_delete(self):
        resp = self.client.get('/banks/3/delete/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_bank_create(self):
        resp = self.client.get('/banks/6/reviews/')
        self.assertEqual(resp.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        connections.close_all()


class WorkWiBanksTestCase(TestCase):
    path = settings.ARCHIVE
    file = io.FileIO(path)
    URL = settings.URL

    @responses.activate
    def test_get_content(self):
        byte = self.file.read()
        responses.add(responses.GET, self.URL, byte)
        self.assertEqual(models.Bank.objects.count(), 0)
        WorkWithBanks.load_and_save_infoBank()
        self.assertTrue(responses.calls[0].request.url == self.URL)
        counts_banks_for_end = models.Bank.objects.all().count()
        self.assertEqual(counts_banks_for_end, 4)
