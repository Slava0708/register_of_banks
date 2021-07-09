from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import *
from django.views.generic.detail import DetailView
from . import models, forms
from django.shortcuts import redirect
from .models import Bank


class BanksArticleListView(ListView):
    paginate_by = 20
    model = models.Bank
    template_name = 'index.html'
    extra_context = {'title': 'Главная страница'}


class BankCreateViews(CreateView):
    template_name = "adding banks.html"
    form_class = forms.BankForm
    success_url = reverse_lazy('index')


class BankUpdatesView(UpdateView):
    model = models.Bank
    form_class = forms.BankForm
    template_name = 'update banks.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('index')
    context_object_name = 'Bank'


class DetailBank(DetailView):
    model = models.Bank
    template_name = 'bank.html'
    context_object_name = 'Bank'
    pk_url_kwarg = 'id'

    def post(self, request, id):
        url = reverse('reviews', kwargs={
            'id': id,
        })
        return redirect(url)


class CreateReviews(CreateView):
    template_name = "banks reviews.html"
    form_class = forms.BankReviews
    model = models.Review

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({
    #         'bank': Bank.objects.get(id=self.kwargs['id']),
    #     })
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.bank = Bank.objects.get(id=self.kwargs['id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('bank', kwargs={
            'id': self.kwargs['id']
        })


class DeleteBank(DeleteView):
    model = models.Bank
    template_name = 'delete bank.html'
    context_object_name = 'Bank'
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'


