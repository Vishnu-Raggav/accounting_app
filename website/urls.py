from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('invoices/', views.invoice, name='invoices'),
    path('entries/', views.entries, name='entries'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
]
