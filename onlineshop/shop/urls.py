# New urls for our app

from django.conf.urls import url
from shop import views
from django.conf.urls import static 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<catSlug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<prodSlug>[-\w]+)/$', views.product_detail, name='product_detail'),
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
