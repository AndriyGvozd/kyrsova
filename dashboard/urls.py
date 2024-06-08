from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/remove2/<int:item_id>/', views.remove_from_wishlist2, name='remove_from_wishlist2'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('change_user_data/', views.change_user_data, name='change_user_data'),

]
