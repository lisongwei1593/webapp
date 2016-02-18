from oscar.apps.address.admin import *  # noqa

from webapp.apps.address.models import (Province, City, District)


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug_name')
    search_fields = ('name', 'slug_name')


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug_name', 'province', 'lng', 'lat')
    search_fields = ('name', 'slug_name', 'province')


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug_name', 'city')
    search_fields = ('name', 'slug_name', 'city')


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.unregister(get_model('address', 'useraddress'))
admin.site.unregister(get_model('address', 'Country'))
