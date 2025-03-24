from django.contrib import admin
from .models import GDLETNewsModel
# Register your models here.

@admin.register(GDLETNewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','url','socialimage']