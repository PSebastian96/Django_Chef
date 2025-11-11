from django.contrib import admin
from .models import CustomUser, Category, IngreadientMeasure

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'joined_at']
    search_fields = ('username', 'email')
    ordering = ['joined_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id']
    ordering = ['name']
    list_editable = ['name']
    search_fields = ['name']

@admin.register(IngreadientMeasure)
class IngredientMeasureAdmin(admin.ModelAdmin):
    list_display = ['id', 'measure']
    list_display_links = ['id']
    ordering = ['id']
    list_editable = ['measure']
    search_fields = ['measure']