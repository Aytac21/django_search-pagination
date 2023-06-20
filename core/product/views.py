from django.shortcuts import render
from django.db.models import F, FloatField
from django.db.models.functions import Coalesce
from .models import Product
from django.core.paginator import Paginator

def list_view(request):
    products = Product.objects.annotate(
        discount=Coalesce("discount_price", 0, output_field=FloatField()),
        total_price=F("price") - F("discount")
    )

    name = request.GET.get("name", None)

    if name:
        products = products.filter(name__icontains=name)
        
    
    paginator=Paginator(products,3)
    page_num=request.GET.get('page',1)
    products=paginator.page(page_num)

    context = {'products': products}
    return render(request,'list.html',context)