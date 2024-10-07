from django.contrib import admin
from .models import Category, Article,Rating,Review, BreakingNews

admin.site.register(Article)
admin.site.register(Rating)
admin.site.register(Review)

admin.site.register(BreakingNews)

    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    
    