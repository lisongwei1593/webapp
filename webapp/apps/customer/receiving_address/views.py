# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse

from webapp.apps.address.models import Province, City, District


def get_location(request):

    province_id = request.GET.get('province_id', '')
    city_id = request.GET.get('city_id', '')
    result = {}
    if province_id:
        try:
            current_province = Province.objects.get(id=province_id)

            citys = current_province.city_set.all()
            citys_data = list(citys.values('id', 'name'))

            districts = District.objects.filter(city__province=current_province)
            districts_data = list(districts.values('id', 'name'))

            result = {'citys': citys_data, 'districts': districts_data}
        except:
            result = {'citys': [], 'districts': []}
    if city_id:
        try:
            current_city = City.objects.get(id=city_id)

            districts = current_city.district_set.all()
            districts_data = list(districts.values('id', 'name'))

            result = {'districts': districts_data}
        except:
            result = {'districts': []}
    return HttpResponse(json.dumps(result), content_type='application/json', status=200)




