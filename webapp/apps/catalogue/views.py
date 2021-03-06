#coding=utf-8
'''
'''
import json
import traceback
import datetime
from django.contrib import messages
from django.core.paginator import InvalidPage
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from oscar.apps.customer.history import extract
from oscar.core.loading import get_class,get_model

from webapp.apps.catalogue.models import Category

from django.http.response import HttpResponse

SimpleProductSearchHandler = get_class(
    'catalogue.searchproduct_handlers', 'SimpleProductSearchHandler')
Product = get_model('catalogue', 'product')
ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
Province = get_model('address', 'Province')
City = get_model('address', 'City')

class CustomProductDetailView(CoreProductDetailView):
    template_name = "catalogue/customdetail.html"
    enforce_paths = False
    enforce_parent = False
    ##不显示下架商品
    queryset = Product.objects.filter(is_on_shelves = True,opening_date__lte=datetime.datetime.now().date())

    def get_history_products(self):
        ids = extract(self.request)
        history_products = Product.objects.filter(id__in = ids,opening_date__lte=datetime.datetime.now().date()).order_by('-browse_num')[:7]
        return history_products

    def get_context_data(self, **kwargs):
        ctx = super(CustomProductDetailView, self).get_context_data(**kwargs)
        provinces = Province.objects.all()
        ctx['provinces']=provinces
        ctx['history_products'] = self.get_history_products()
        ctx['recommended_products'] = self.get_object().recommended_products.filter(opening_date__lte=datetime.datetime.now().date()).order_by('-browse_num')[:7]
        #查找categorylist
        category_list = Category.objects.filter(depth=1).order_by('path')[:10]
        ctx['category_list'] = category_list
        product = self.get_object()
        ctx['max_num'] = 1989
        return ctx

    ###浏览量+1
    def get(self,request,*args,**kwargs):
        #=======================================================================
        # pk_id = request.path.split('_')[1].split(r'/')[0]
        # print pk_id
        # product = Product.objects.get(pk=pk_id)
        # product.browse_num +=1
        # product.save()
        #=======================================================================
        product = self.get_object()
        product.browse_num +=1
        product.save(update_fields=['browse_num',])

        return super(CustomProductDetailView,self).get(request,*args,**kwargs)


class AllSearchProductView(TemplateView):
    """
    Browse all products in the catalogue
    分页展示所有商品
    """
    context_object_name = "products"
    template_name = 'catalogue/product-list.html'

    def get(self, request, *args, **kwargs):
        try:
            self.search_handler = self.get_search_handler(
                self.request.GET, request.get_full_path(), [])
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _('The given page number was invalid.'))
            return redirect('catalogue:allproducts')
        return super(AllSearchProductView, self).get(request, *args, **kwargs)

    def get_search_handler(self, *args, **kwargs):
        return SimpleProductSearchHandler(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {}
        ctx['summary'] = _("All products")
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name)
        ctx.update(search_context)

        ctx['hotproduct'] = []

        ctx['history_products'] = []

        category_list = Category.objects.filter(depth=1).order_by('path')[:10]
        ctx['category_list'] =category_list


        return ctx


def get_province_citys(request,pid):
    province = Province.objects.get(id=pid)
    cities = City.objects.filter(province=province)
    all_city_info = []
    for city in cities:
        city_info = [city.id,city.name]
        all_city_info.append(city_info)
    return HttpResponse(json.dumps(all_city_info),content_type = "application/json")

def city_has_product(request):
    pid = request.POST.get('pid')
    cid = request.POST.get('cid')
    product = Product.objects.get(id=pid)
    city = City.objects.get(id=cid)
    all_city = []
    all_pickup_addr = product.stock_config_product.distribution_pickup_addr.all()
    for pickup_addr in all_pickup_addr:
        all_city.append(pickup_addr.city)
    return HttpResponse(city in all_city)











