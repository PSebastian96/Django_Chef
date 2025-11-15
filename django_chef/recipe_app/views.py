from formtools.wizard.views import SessionWizardView
from django.views.generic import (CreateView, DetailView, UpdateView, ListView, TemplateView, DeleteView, View)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from .forms import (RecipeForm, IngredientsForm, StepsForm, CustomUserCreation, CustomLoginForm)
from .models import (Recipe, Ingredient, Step, IngreadientMeasure, CustomUser, Category, IngreadientMeasure, FavoriteRecipe)
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

""" 
Home page view
"""
class HomePageView(TemplateView):
    template_name = 'home.html'

"""
User CRUD Section
"""
# user register view
class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreation
    template_name = 'recipe_app/users/register_user.html'
    success_url = reverse_lazy('recipe_list')

# user login view
class UserLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'recipe_app/users/login.html'
    redirect_authenticated_user = True
    """"Django has a built in next page, which is profile, to direct to a custom page
    override the get_success_url() function."""
    def get_success_url(self):
        return reverse_lazy('recipe_list')

# user logout view
class UserLogOutView(LogoutView):
    next_page = 'login'

# user profile
class CustomUserDetails(LoginRequiredMixin, TemplateView):
    template_name = 'recipe_app/users/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
# user update
class CustomUserDetailUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'recipe_app/users/update_account.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic']
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        # Ensure users can only update *their own* account
        return self.request.user

# user delete
class DelUserView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'recipe_app/users/delete_account.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        # only allow deleting your own account
        return self.request.user

"""
Recipe CRUD Section
"""
# create recip - multi step
class WizForm(LoginRequiredMixin, SessionWizardView):
    form_list = [
    ("recipe", RecipeForm),
    ("ingredients", IngredientsForm),
    ("steps", StepsForm),
    ]

    TEMPLATES = {
    "recipe": "recipe_app/recipe_forms/rec_form.html",
    "ingredients": "recipe_app/recipe_forms/ing_form.html",
    "steps": "recipe_app/recipe_forms/instruction_form.html",
    }
    
    file_storage = FileSystemStorage(
         location=os.path.join(settings.MEDIA_ROOT, 'wizard_temp')
    )
    
    def get_template_names(self):
        """Return the correct template for the current step."""
        return [self.TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        """Save data after all steps are complete."""
        # Step 1 — Recipe
        recipe_form = form_list[0]
        recipe = recipe_form.save(commit=False)
        recipe.slug = slugify(recipe.title)
        recipe.owner = self.request.user
        recipe.save()

        # Step 2 — Ingredient
        ingredient_form = form_list[1].cleaned_data
        Ingredient.objects.create(
            recipe=recipe,
            name=ingredient_form['name'],
            quantity=ingredient_form.get('quantity'),
            measure=IngreadientMeasure.objects.filter(measure=ingredient_form.get('measure')).first(),
        )

        # Step 3 — Step
        step_form = form_list[2].cleaned_data
        Step.objects.create(
            recipe=recipe,
            step_number=step_form['step_number'],
            step=step_form['step']
        )

        return redirect('read_recipe', pk=recipe.pk, slug=recipe.slug)

# list all recipe
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'
    queryset = Recipe.objects.all()
    template_name = 'recipe_app/recipe/list_recipe.html'
    ordering = ['title']
    
    def get_queryset(self):
        # Get only the recipes created by the logged-in user
        queryset = Recipe.objects.filter(owner=self.request.user).order_by('title')

        # Get all favorited recipe IDs for this user
        favorites = set(
            FavoriteRecipe.objects.filter(user=self.request.user)
            .values_list('recipe_id', flat=True)
        )

        # Add a dynamic "is_fav" attribute to each recipe
        for recipe in queryset:
            recipe.is_fav = recipe.id in favorites

        return queryset

# read recipe
class ReadRecipe(LoginRequiredMixin, DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipe_app/recipe/read_recipe.html'

    def get_object(self, queryset=None):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('pk'),  slug=self.kwargs.get('slug'), owner=self.request.user)

        #
        recipe.is_fav = FavoriteRecipe.objects.filter(
            user=self.request.user,
            recipe=recipe
        ).exists()

        return recipe
    
# update recipe
class UpdateRecipe(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = 'recipe_app/recipe/update_recipe.html'
    form_class = RecipeForm
    http_method_names = ['get', 'post']

    def get_success_url(self):
        return reverse('read_recipe', kwargs={'pk': self.object.pk, 'slug': self.object.slug})
    
    def get_object(self, queryset=None):
        return get_object_or_404(
            Recipe,
            pk=self.kwargs.get('pk'),
            slug=self.kwargs.get('slug')
        )
    
    def get_queryset(self):
        return Recipe.objects.filter(owner=self.request.user)


#delete recipe
class DelRecipe(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipe_app/recipe/delete_recipe.html'
    success_url = reverse_lazy('recipe_list')
    context_object_name = 'recipe'

    def get_context_object_name(self, obj):
        recipe = super().get_context_object_name(obj)
        return messages.info(self.request,f'{recipe.title} has been deleted!')
    
    def get_object(self, queryset=None):
        # Ensure only existing recipes are deleted
        return get_object_or_404(Recipe, pk=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
        
    def get_queryset(self):
        return Recipe.objects.filter(owner=self.request.user)

"""
Ingredient CRUD Section
"""
# create ingredients
class CreateIngredient(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = 'recipe_app/ingredients/create_ingredients.html'
    fields = ['name', 'quantity', 'measure']
    
    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        context['recipe'] = recipe
        return context

    def get_success_url(self):
        return reverse_lazy('read_recipe', kwargs={'pk': self.object.recipe.pk, 'slug': self.object.recipe.slug})

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'], slug=self.kwargs['slug'])

# update ingredient
class UpdateIngredient(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = 'recipe_app/ingredients/update_ingredients.html'
    fields = ['name', 'quantity', 'measure']

    def get_success_url(self):
        return reverse_lazy('read_recipe', kwargs={'pk': self.object.recipe.pk, 'slug': self.object.recipe.slug})

# delete ingredient
class DelIngredient(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'recipe_app/ingredients/delete_ingredient.html'

    def get_success_url(self):
        return reverse_lazy('read_recipe', kwargs={'pk': self.object.recipe.pk, 'slug': self.object.recipe.slug})

"""
Step CRUD Section
"""
# create step
class CreateInstruction(LoginRequiredMixin, CreateView):
    model = Step
    template_name = 'recipe_app/instructions/create_instruction.html'
    fields = ['step_number', 'step']
    
    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        context['recipe'] = recipe
        return context

    def get_success_url(self):
        return reverse_lazy('read_recipe', kwargs={'pk': self.object.recipe.pk, 'slug': self.object.recipe.slug})

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'], slug=self.kwargs['slug'])

# update step
class Updateinstruction(LoginRequiredMixin, UpdateView):
    model = Step
    template_name = 'recipe_app/instructions/update_instruction.html'
    fields = ['step_number', 'step']

    def get_success_url(self):
        return reverse_lazy('read_recipe', kwargs={'pk': self.object.recipe.pk, 'slug': self.object.recipe.slug})

# delete step
class DelInstruction(LoginRequiredMixin, DeleteView):
    model = Step
    template_name = 'recipe_app/instructions/delete_instruction.html'

    def get_success_url(self):
        return reverse_lazy('read_recipe', kwargs={'pk': self.object.recipe.pk, 'slug': self.object.recipe.slug})

"""
Category CRUD Section
"""

# create category
class CreateCategory(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'recipe_app/category/create_category.html'
    fields = ['name']
    success_url = reverse_lazy('list_category')
    http_method_names = ['get', 'post']

# list categories
class ListCategories(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'recipe_app/category/list_category.html'
    context_object_name = 'categories'
    http_method_names = ['get']
    ordering = ['name']

# update category
class UpdateCategories(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'recipe_app/category/update_category.html'
    success_url = reverse_lazy('list_category')
    fields = ['name']
    http_method_names = ['get', 'post']

# delete category
class DelCategory(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('list_category')
    template_name = 'recipe_app/category/delete_category.html'

    # Ensure both pk and slug are used
    def get_object(self, queryset=None):
        return get_object_or_404(
            Category,
            pk=self.kwargs['pk'],
            slug=self.kwargs['slug']
        )

"""
Measurement CRUD Section
"""

# create measurement
class CreateMeasurement(LoginRequiredMixin, CreateView):
    model = IngreadientMeasure
    template_name = 'recipe_app/measurements/create_measurement.html'
    fields = ['measure']
    success_url = reverse_lazy('list_measurement')
    http_method_names = ['get', 'post']

# list measurement
class ListMeasurement(LoginRequiredMixin, ListView):
    model = IngreadientMeasure
    template_name = 'recipe_app/measurements/list_measurement.html'
    context_object_name = 'measurements'
    http_method_names = ['get']
    ordering = ['measure']

# update measurement
class UpdateMeasurement(LoginRequiredMixin, UpdateView):
    model = IngreadientMeasure
    template_name = 'recipe_app/measurements/update_measurement.html'
    success_url = reverse_lazy('list_measurement')
    fields = ['measure']
    http_method_names = ['get', 'post']

# delete measurement
class DelMeasurement(LoginRequiredMixin, DeleteView):
    model = IngreadientMeasure
    success_url = reverse_lazy('list_measurement')
    template_name = 'recipe_app/measurements/delete_measurement.html'
    # Ensure both pk and slug are used
    def get_object(self, queryset=None):
        return get_object_or_404(
            IngreadientMeasure,
            pk=self.kwargs['pk'],
        )
    
""" 
Favorite Recipe Add, Delete, List
"""

class ToggleFavoriteView(LoginRequiredMixin, View):
    """Add or remove a recipe from favorites."""
    def post(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])

        favorite, created = FavoriteRecipe.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )

        if created:
            messages.success(request, f"Added <strong class='text-decoration-underline'>{recipe.title}</strong> to favorites.")
        else:
            favorite.delete()
            messages.info(request, f"Removed <strong class='text-decoration-underline'>{recipe.title}</strong> from favorites.")

        # return user back to where they came from
        next_url = request.META.get("HTTP_REFERER", reverse("recipe_list"))
        return redirect(next_url)

class FavoriteListView(LoginRequiredMixin, ListView):
    model = FavoriteRecipe
    template_name = 'recipe_app/recipe/favorites_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return FavoriteRecipe.objects.filter(user=self.request.user).select_related('recipe')