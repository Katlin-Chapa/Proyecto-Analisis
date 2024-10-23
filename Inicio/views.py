from django.shortcuts import render
from django.views.generic import View, TemplateView
#from inventory.models import Stock
#from transactions.models import SaleBill, PurchaseBill

class InicioVista(View):
    template_name = "inicio.html"
    def get(self, request):
        # Aquí podrías obtener datos, si es necesario
        return render(request, self.template_name)
    '''def get(self, request):        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'sales'     : sales,
            'purchases' : purchases
        }
        return render(request, self.template_name, context)
'''
class AcercaVista(TemplateView):
    template_name = "acerca.html"