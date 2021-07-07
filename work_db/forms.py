from django import forms
from . import models


class BankForm(forms.ModelForm):
    class Meta:
        model = models.Bank
        fields = ['name', 'bik', 'city', 'account']
        labels = {
            'name': 'Наименование',
            'bik': 'БИК',
            'city': 'Город',
            'account': 'Счет',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BankReviews(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['username', 'review', ]
        labels = {
            'username': 'Username',
            'review': 'Отзыв',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control'}),
        }

    # def __init__(self, *args, **kwargs):
    #     self.bank = kwargs.pop('bank')
    #     super().__init__(*args, **kwargs)
    #
    # def save(self, commit=True):
    #     review = super().save(commit=False)
    #     review.bank = self.bank
    #     review.save()
    #     return review
