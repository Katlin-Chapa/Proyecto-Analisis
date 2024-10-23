import django_filters
from .models import Stock, Categoria  # Asegúrate de importar Categoria

class StockFilter(django_filters.FilterSet):
    # Filtro por nombre
    nombre = django_filters.CharFilter(lookup_expr='icontains', label='Nombre')  # Cambié 'name' a 'nombre' para reflejar el nombre en español

    # Filtro por categoría
    categoria = django_filters.ModelChoiceFilter(queryset=Categoria.objects.all(), label='Categoría', empty_label='Seleccione una categoría')

    class Meta:
        model = Stock
        fields = ['nombre', 'categoria']  # Agrega 'categoria' a los campos
