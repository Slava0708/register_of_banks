from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', blank=False)
    bik = models.CharField(max_length=9, verbose_name='Бик', blank=False)
    city = models.CharField(max_length=50, verbose_name='Город', blank=True)
    account = models.CharField(max_length=20, verbose_name='Счет', blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        ordering = ['name']


class Review(models.Model):
    username = models.CharField(max_length=20, verbose_name='Пользователь', blank=False)
    review = models.TextField(verbose_name='Отзыв о банке', blank=False)
    bank = models.ForeignKey('Bank', unique=False, on_delete=models.CASCADE, blank=False)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class Files(models.Model):
    file_field = models.FileField(upload_to='media/')

