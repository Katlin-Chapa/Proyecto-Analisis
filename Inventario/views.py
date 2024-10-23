from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView, 
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Stock
from .forms import StockForm
from django_filters.views import FilterView
from .filters import StockFilter


class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(es_eliminado=False)
    template_name = 'inventario.html'