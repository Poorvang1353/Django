"""kriii URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from mailbox import MaildirMessage
from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf import settings # --------> this
from django.conf.urls.static import static# --------> this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView,name='home'),
    path('signup/',signup, name='signup'),
    path('login/',LoginInfo, name='login'),
    path('logout/',LogoutView,name='logout'),
    path('productdetail/<int:id>/',Productdetails,name='productdetail'),
    path('cart/',CartView,name='cart/'),
    path('addtocart/<int:id>/', Add_to_cartView),
    path('pluscart/<int:id>/', pluse_quantity),
    path('minuscart/<int:id>/', minus_quantity),
    path('Delete/<int:id>/',DeleteView),
    path('clearcart/', clearcart),
    path('wishlist/',WishListView),
    path('addtowishlist/<int:id>/', Add_to_wishlist),
    path('Listdelete/<int:id>/',ListDeleteView),
    path('address/',CustomerAddressView),
    path('Addressdelete/<int:id>/',AddressDeleteView),
    path('Addressupdate/<int:id>/',UpdateaddressView),
    path('checkout/', CheckoutView),
    path('order/', OrderView),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # --------> this
