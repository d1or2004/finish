from django.db import models
from .helps import SaveModelFields
from django.contrib.auth.models import User


class UserMadel(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.TextField(null=True)
    is_staff = models.BooleanField(default=False, null=True)
    telegram_id = models.PositiveBigIntegerField(verbose_name="Telegram Id", unique=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username


class Product(models.Model):
    product_name = models.CharField(verbose_name="Product Name", max_length=50)
    image = models.ImageField(upload_to=SaveModelFields.product_image_path)
    price = models.DecimalField(verbose_name="Narxi", decimal_places=2, max_digits=200)
    description = models.TextField(verbose_name="Mahsulot haqida", max_length=300)
    count = models.IntegerField(max_length=1222, null=True)
    category_code = models.CharField(verbose_name="Kategoriya kodi", max_length=200)
    category_name = models.CharField(verbose_name="Category Nomi", max_length=200)
    subcategory_code = models.CharField(verbose_name="Ost-kategoriya kodi", max_length=34)
    subcategory_name = models.CharField(verbose_name="Ost-kategoriya nomi", max_length=30)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.product_name


class RecentBlogModel(models.Model):
    creator = models.CharField(max_length=100)
    create_data = models.DateField(auto_created=True)
    image = models.ImageField(upload_to='media/recentblog/', null=True)


class Costumer(models.Model):
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='media/costumer/')
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [models.Index(fields=['last_name', 'first_name'])]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Testimonial(models.Model):
    description = models.TextField()
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['description']
        indexes = [models.Index(fields=['description'])]

    def __str__(self):
        return f"{self.description}, {self.costumer}"


class TeamModel(models.Model):
    name = models.CharField(max_length=443)
    image = models.ImageField(upload_to='media/team/')
    description = models.TextField()


class ContactModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    create_data = models.DateTimeField(auto_now_add=True)


class Subscribe(models.Model):
    name = models.CharField(max_length=34)
    email = models.EmailField(max_length=32)
    date_time = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now=True)
    last_update = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title.product_name
