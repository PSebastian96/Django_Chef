from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify


# django chef user model (user db)
class CustomUser(AbstractUser):
    # these are default in Django
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

# category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name

# recipe model
class Recipe(models.Model):
    TIME_UNITS = [
        ('min', 'Minutes'),
        ('hr', 'Hours'),
        ('day', 'Days'),
        ('wk', 'Weeks'),
        ('mo', 'Months'),
    ]

    SPICE_LEVELS = [(i, str(i)) for i in range(6)]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    prep_time = models.PositiveIntegerField()
    prep_time_unit = models.CharField(max_length=5, choices=TIME_UNITS, default='min')
    cook_time = models.PositiveIntegerField()
    cook_time_unit = models.CharField(max_length=5, choices=TIME_UNITS, default='min')
    spice_level = models.PositiveSmallIntegerField(choices=SPICE_LEVELS, default=0)
    category = models.ForeignKey(Category, null=True, blank=False, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    
    def pluralize_unit(self, count, unit_code):
        unit_name = dict(self.TIME_UNITS).get(unit_code, "")
        if count == 1:
            return unit_name
        return f"{unit_name}s" 
    
    def get_prep_display(self):
        """Return human-readable prep time, e.g., '2 Hours'."""
        return f"{self.prep_time} {dict(self.TIME_UNITS).get(self.prep_time_unit)}"

    def get_cook_display(self):
        """Return human-readable cook time, e.g., '45 Minutes'."""
        return f"{self.cook_time} {dict(self.TIME_UNITS).get(self.cook_time_unit)}"

# ingredient measure model
class IngreadientMeasure(models.Model):
    measure = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.measure

# ingredient model
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    measure = models.ForeignKey(IngreadientMeasure, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} - {self.quantity or ''} - {self.measure}"

# recipe step model
class Step(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    step = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.step_number}. { self.step }"
    
# favorite recipe model
class FavoriteRecipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique_user_recipe')
        ]
    
    def __str__(self):
        return f"{self.user.username}\s favorite recipe: {self.recipe.name}"
