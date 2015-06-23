# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from mapshop.models import Product, Category, ProductImages, Kiosk, Order, OrderItem, Client, Preorder
from image_cropping import ImageCroppingMixin
from mptt.admin import MPTTModelAdmin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_slug', 'thumb', 'price', 'rate', 'category', 'ammount')
    list_filter = ('name', 'price', 'rate')
    list_editable = ('ammount',)

class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'name_slug', 'level', 'parent')

class KioskAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Kiosk, KioskAdmin)


class ProductImagesAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('thumb', 'product', 'is_main')


admin.site.register(ProductImages, ProductImagesAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    verbose_name_plural = u'Элементы'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'session', 'kiosk', 'client', 'status')
    list_filter = ('status',)
    inlines = [
        OrderItemInline,
    ]


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'ammount')


admin.site.register(OrderItem, OrderItemAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'email', 'kiosk')


admin.site.register(Client, ClientAdmin)

class PreorderAdmin(admin.ModelAdmin):
    list_display = ('product', 'contact', 'type', 'created_at')
    list_filter = ('type',)

admin.site.register(Preorder, PreorderAdmin)



