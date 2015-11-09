from django.contrib import admin
from models import Proxy

class ProxyAdmin(admin.ModelAdmin):
    fields = ['ip','port','type','country','create_time']
    list_display = ['ip','port','type','create_time','was_published_recently']
    list_filter = ['create_time']
    search_fields = ['ip','port','type','create_time']

# Register your models here.
admin.site.register(Proxy,ProxyAdmin)