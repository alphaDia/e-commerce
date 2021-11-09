from django.db import models
from category.models import Category

class Product(models.Model):
    name            = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to="photos/product")
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    variations      = models.ManyToManyField('Variation') 
    created_at      = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_detail', args=[self.category.slug, self.slug])
    

class VariationManager(models.Manager):
    def colors(self):
        return self.filter(variation_category="color", is_active=True)

    def sizes(self):
        return self.filter(variation_category="size", is_active=True)

class Variation(models.Model):
    variation_choices = (
        ('color', 'color'),
        ('size', 'size'),
    )
    variation_category = models.CharField(max_length=100, choices=variation_choices)
    variation_value = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    objects = VariationManager()
     
    def __str__(self):
        return self.variation_value
    