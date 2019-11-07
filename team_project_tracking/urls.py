from django.urls import path, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # help page
    path('help_page/', views.help_page, name='help_page'),

    # user registration and authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # roles
    path('add_user_role/', views.add_user_role, name='add_user_role'),
    re_path('^edit_user_role/(?P<pk>\d+)/$', views.edit_user_role, name='edit_user_role'),
    path('assign_role/', views.assign_role, name='assign_role'),
    path('unassign_role/', views.unassign_role, name='unassign_role'),

    #  courses
    path('add_course/', views.add_course, name='add_course'),
    path('course_list/', views.course_list, name='course_list'),
    path('course_details/<int:pk>', views.course_details, name='course_details'),
    re_path('^edit_course_info/(?P<pk>\d+)/$', views.edit_course_info, name='edit_course_info'),
    # re_path('^delete_community/(?P<pk>\d+)/$', views.delete_community, name='delete_community'),

]
