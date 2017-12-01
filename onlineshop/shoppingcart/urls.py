
from django.conf.urls import url
import views
from django.conf.urls import static 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   url(r'^$', views.shoppingcart_list, name="shoppingcart_list"),
   url(r'^add/(?P<product_id>\d+)/$', views.shoppingcart_add, name="shoppingcart_add"),
   url(r'^remove/(?P<product_id>\d+)/$', views.shoppingcart_remove, name="shoppingcart_remove"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
