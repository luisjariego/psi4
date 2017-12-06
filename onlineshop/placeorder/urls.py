
from django.conf.urls import url
import views
from django.conf.urls import static 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   url(r'^create_order/$', views.createOrder, name="create_order"),
   url(r'^confirm_order/$', views.confirmOrder, name="confirm_order"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
