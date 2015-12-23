from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^ibs/register/$', views.user_add, name='user_add'),
    url(r'^ibs/login/$', views.user_login, name='user_login'),
    url(r'^ibs/logout/$', views.user_logout, name='user_logout'),
    url(r'^ibs/home/$', views.user_home, name='user_home'),
    url(r'^ibs/home/profile/(?P<user_pk>[0-9]+)/$', views.user_view, name='user_view'),
    url(r'^ibs/home/userupdate/$', views.user_update, name='user_update'),
    url(r'^ibs/home/post/(?P<type_pk>[0-9]+)/$', views.item_add, name='item_add'),
    url(r'^ibs/home/updatepost/(?P<item_pk>[0-9]+)/$', views.item_update, name='item_update'),
    url(r'^ibs/home/deletepost/(?P<item_pk>[0-9]+)/$', views.item_delete, name='item_delete'),
    url(r'^ibs/home/browse/$', views.item_browse, name='item_browse'),
    url(r'^ibs/home/browse/(?P<type_pk>[0-9]+)/$', views.item_browse_bytype, name='item_browse_bytype'),
    url(r'^ibs/home/browse/(?P<category_pk>[0-9]+)/$', views.item_browse_bycategory, name='item_browse_bycategory'),
    url(r'^ibs/home/viewitem/(?P<item_pk>[0-9]+)/$', views.item_view, name='item_view'),
    url(r'^ibs/home/myitem/$', views.item_of_user, name='item_of_user'),
    url(r'^ibs/home/addcategory/$', views.category_add, name='category_add'),
    url(r'^ibs/home/viewcategory/$', views.category_view, name='category_view'),
    url(r'^ibs/home/deletecategory/(?P<category_pk>[0-9]+)/$', views.category_delete, name='category_delete'),
]