from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^hom', views.home),
    url(r'^reg/(?P<id>\d+)$', views.home),
    url(r'^reg/(?P<id>\d+)/create$', views.create),
    url(r'^addproduct$', views.addproduct),
    url(r'^logout$', views.logout),
    url(r'^product/(?P<product_id>\d+)$', views.showproduct),
    url(r'^product/confirm_add_product/(?P<id>\d+)$', views.join),
    url(r'^product/confirm_delete_product/(?P<product_id>\d+)$', views.delete_product),
    url(r'^product/confirm_remove_product/(?P<product_id>\d+)$', views.remove),

]