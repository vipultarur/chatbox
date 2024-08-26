from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),

    path('friend/<str:pk>', views.details, name='details'),

    path('login/', views.userlogin, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('sent_msg/<str:pk>',views.sentMessages,name='sent_msg'),

    path('rec_msg/<str:pk>',views.receivedMessage,name='rec_msg'),

    path('notify',views.chatNotification, name='notify')

]