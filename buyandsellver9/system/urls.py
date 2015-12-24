from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ibs/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^register/$', views.user_add, name='user_add'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^home/$', views.user_home, name='user_home'),
    url(r'^home/profile/(?P<user_pk>[0-9]+)/$', views.user_view, name='user_view'),
    url(r'^home/userupdate/$', views.user_update, name='user_update'),
    url(r'^home/post/(?P<type_pk>[0-9]+)/$', views.item_add, name='item_add'),
    url(r'^home/updatepost/(?P<item_pk>[0-9]+)/$', views.item_update, name='item_update'),
    url(r'^home/deletepost/(?P<item_pk>[0-9]+)/$', views.item_delete, name='item_delete'),
    url(r'^home/browse/$', views.item_browse, name='item_browse'),
    url(r'^home/browse/(?P<type_pk>[0-9]+)/$', views.item_browse_bytype, name='item_browse_bytype'),
    url(r'^home/browse/(?P<category_pk>[0-9]+)/$', views.item_browse_bycategory, name='item_browse_bycategory'),
    url(r'^home/viewitem/(?P<item_pk>[0-9]+)/$', views.item_view, name='item_view'),
    url(r'^home/myitem/$', views.item_of_user, name='item_of_user'),
    url(r'^home/addcategory/$', views.category_add, name='category_add'),
    url(r'^home/viewcategory/$', views.category_view, name='category_view'),
    url(r'^home/deletecategory/(?P<category_pk>[0-9]+)/$', views.category_delete, name='category_delete'),
]