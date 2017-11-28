"""onlineshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include 
from django.conf.urls import static
#views 
from shop import views as shopviews
from shoppingcart import views as cartviews

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [	
    url(r'^admin/', admin.site.urls),
    url(r'^shop/', include('shop.urls')),
    url(r'^base/', include('shop.urls')),
    url(r'^about', shopviews.about, name="about"),
    url(r'^list/$', cartviews.shoppingcart_list, name="shoppingcart_list"),
    url(r'^add/(?P<product_id>\d+)/$', cartviews.shoppingcart_add, name="shoppingcart_add"),
    url(r'^remove/(?P<product_id>\d+)/$', cartviews.shoppingcart_remove, name="shoppingcart_remove"),
    url(r'', include('shop.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
