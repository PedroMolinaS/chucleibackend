from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, Order, Order_Detail, CategoryMain, Store, Almacen, Deliveryman, Person, \
    User, Photos


# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin."""

    list_display = ('pk', 'username', 'email',)
    list_display_links = ('pk', 'username', 'email',)

    search_fields = (
        'email',
        'username',
        'name',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'date_joined',
        'modified',
    )

    readonly_fields = ('date_joined', 'modified',)


class CategoryMainAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(CategoryMain, CategoryMainAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class StoreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Store, StoreAdmin)


class AlmacenAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Almacen, AlmacenAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin, )


# class CustomerAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#
#
# admin.site.register(Customer, CustomerAdmin, )


class DeliveryManAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Deliveryman, DeliveryManAdmin)


# class UserAdmin(admin.ModelAdmin):
#     # def image_tag(self, obj):
#     #    return format_html('<img src="{}" width="150" ,height="150" />'.format(obj.imagen.url))
#
#     # image_tag.short_description = 'Image'
#     list_display = ['username', 'email', 'name']
#
#     search_fields = (
#         'email',
#         'username',
#         'name',
#     )


admin.site.register(User, UserAdmin)

admin.site.register([Order, Order_Detail, Person, Photos])
