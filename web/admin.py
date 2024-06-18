from django.contrib import admin
from .models import UserMadel, Product, RecentBlogModel, Costumer, Testimonial, TeamModel, Cart
from import_export.admin import ImportExportModelAdmin


@admin.register(UserMadel)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('id', "first_name", "last_name")
    list_filter = ('last_name', 'first_name')
    search_fields = ('last_name', 'first_name')
    ordering = ('id',)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ("product_name", "price")
    list_filter = ("product_name", "description")
    search_fields = ("product_name",)
    ordering = ("id",)


@admin.register(RecentBlogModel)
class RecentrAdmin(ImportExportModelAdmin):
    list_display = ("creator",)
    ordering = ("id",)


@admin.register(Costumer)
class CostumerAdmin(ImportExportModelAdmin):
    list_display = ("last_name", "first_name")
    ordering = ("id",)


@admin.register(Testimonial)
class TestimonialAdmin(ImportExportModelAdmin):
    list_display = ("description",)
    ordering = ("id",)


@admin.register(TeamModel)
class TestimonialAdmin(ImportExportModelAdmin):
    list_display = ("name",)


@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'user')
    list_display_links = ('id', 'title', 'user')
    search_fields = ('title', 'id')
    ordering = ('id',)
