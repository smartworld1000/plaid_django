from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup-plus/', views.signup_plus, name='signup_plus'),
    url(r'^plaid_verify/', views.plaid_verify, name='plaid_verify'),
    url(r'^complete_signup/', views.complete_signup, name='complete_signup'),
]