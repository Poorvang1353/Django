from django.contrib import admin

from myapp.models import maincatagory,ProductModel,Order

# Register your models here.


@admin.register(maincatagory)
class maincatagoryAdmin(admin.ModelAdmin):
    list_display = ("image", "name")


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("description", "sell_price", "discount_price", "discount", "og_price", "image", "name", "mcate")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("status", "order_date", "quantity", "product", "customer", "user")
