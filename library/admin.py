from django.contrib import admin

# Register your models here.
from .models import Data

from .forms  import createData

class createDataadmin(admin.ModelAdmin):
    list_display=['song','artist','year','rating','genre']
    form=createData
    list_filter=['artist','year','genre']
    search_fields=['song','artist','genre']
    

admin.site.register(Data,createDataadmin)