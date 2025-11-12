from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (CustomUserDetails, CustomUserDetailUpdateView, DelUserView, UserRegisterView, UserLoginView, 
                    UserLogOutView, RecipeListView ,WizForm, HomePageView) # RecipeWizard
from .views import (CreateCategory, ListCategories, UpdateCategories, DelCategory,
                    CreateMeasurement, ListMeasurement, UpdateMeasurement, DelMeasurement,
                    ReadRecipe, UpdateRecipe, DelRecipe, CreateIngredient, UpdateIngredient, DelIngredient,
                    CreateInstruction, Updateinstruction, DelInstruction, AddFavorite, RemoveFavorite, ListFavorite)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register_to_django_chef/', UserRegisterView.as_view(), name='register'),
    path('create_recipe/', WizForm.as_view(), name='create_recipe'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('my_account/', CustomUserDetails.as_view(), name='account'),
    path('update_account/', CustomUserDetailUpdateView.as_view(), name='update_account'),
    path('delete_account/', DelUserView.as_view(), name='delete_account'),
    path('logout/', UserLogOutView.as_view(), name='logout'),
    path('create_category/', CreateCategory.as_view(), name='create_category'),
    path('list_category/', ListCategories.as_view(), name='list_category'),
    path('update_category/<int:pk>/', UpdateCategories.as_view(), name='update_category'),
    path('delete_category/<int:pk>/', DelCategory.as_view(), name='delete_category'),
    path('create_measurement/', CreateMeasurement.as_view(), name='create_measurement'),
    path('list_measurement/', ListMeasurement.as_view(), name='list_measurement'),
    path('update_measurement/<int:pk>/', UpdateMeasurement.as_view(), name='update_measurement'),
    path('delete_measurement/<int:pk>/', DelMeasurement.as_view(), name='delete_measurement'),
    path('recipe_list/', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/id_<int:pk>/<slug:slug>/read/', ReadRecipe.as_view(), name='read_recipe'),
    path('update_recipe/id_<int:pk>/<slug:slug>/', UpdateRecipe.as_view(), name='update_recipe'),
    path('recipe/id_<int:pk>/<slug:slug>/delete/', DelRecipe.as_view(), name='delete_recipe'),
    path('add_ingredient/id_<int:pk>/<slug:slug>/', CreateIngredient.as_view(), name='add_ingredient'),
    path('update_ingredient/id_<int:pk>/<slug:slug>/update/', UpdateIngredient.as_view(), name='update_ingredient'),
    path('ingredient/id_<int:pk>/<slug:slug>/delete/', DelIngredient.as_view(), name='delete_ingredient'),
    path('add_instruction/id_<int:pk>/<slug:slug>/', CreateInstruction.as_view(), name='add_instruction'),
    path('update_instruction/id_<int:pk>/<slug:slug>/', Updateinstruction.as_view(), name='update_instruction'),
    path('delete_instruction/id_<int:pk>/<slug:slug>/', DelInstruction.as_view(), name='delete_instruction'),
    # path('add_favorite/id_<int:pk>/<slug:slug>/', AddFavorite.as_view(), name='add_fav'),
    # path('remove_favorite/id_<int:pk>/<slug:slug>/', RemoveFavorite.as_view(), name='remove_fav'),
    # path('fav_recipe_list/', ListFavorite.as_view(), name='list_fav'),
    # path('create_recipe/', RecipeWizard.as_view([RecipeForm, IngredientsForm, StepsForm]), name='create_recipe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)