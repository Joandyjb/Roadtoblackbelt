from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('user/create', views.create),
    path('user/login', views.login),
    path('user/quotes', views.Dashboard),
    path('user/create_quotes', views.create_quotes),
    path('user/logout', views.logout),
    path('user/<int:Userposter_id>', views.UserPosterProfile),
    path('myaccount/<int:current_user_id>', views.editprofile),
    path('user/update/<int:UserUptade_id>',views.updatedprofile),
    path('user/returnp', views.returnp),
    path('delete_quote/<int:quote_id>', views.delete),
    path('like_quote/<int:quote_id>', views.like_quote)
    
] 