from django.conf.urls import url
from records import views

urlpatterns = [
    url(r'^api/records$', views.record_list),
    url(r'^api/records/(?P<pk>[0-9]+)$', views.record_detail),
]