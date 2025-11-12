from django.contrib import admin
from .models import CustomUser, Category, IngreadientMeasure, Recipe

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

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title','category','owner']
    search_fields = ['title','category__name']
    ordering = ['title']
    fields = ['title', 'category', 'owner']

    def save_model(self, request, obj, form, change):
        # Only auto-assign owner if it's blank (admin can still choose manually)
        if not change or not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)