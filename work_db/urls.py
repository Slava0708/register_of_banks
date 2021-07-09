from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BanksArticleListView.as_view(), name="index"),
    path('banks/<int:id>/edit/', BankUpdatesView.as_view(), name="update"),
    path('banks/add/', BankCreateViews.as_view(), name="adding banks"),
    path('banks/<int:id>/', DetailBank.as_view(), name="bank"),
    path('banks/<int:id>/delete/', DeleteBank.as_view(), name="delete"),
    path('banks/<int:id>/reviews/', CreateReviews.as_view(), name="reviews"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)