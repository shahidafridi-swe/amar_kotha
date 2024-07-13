from django.contrib import admin
from .models import Category, Article,Rating

admin.site.register(Article)
admin.site.register(Rating)

    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    