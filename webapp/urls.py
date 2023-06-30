from django.urls import path
from . import views 

urlpatterns=[
    path('',views.home, name="home"),
    path('login/',views.login_view, name="login_view"),
    path('register_view/',views.register_view, name="register_view"),
    path('logout/', views.logout_view, name='logout'),
    path('products/',views.product_list, name='product_list'),
    path('profile/', views. profile_view, name='profile'),

    path('profile/edit/', views.profile_edit, name='profile_edit'),

    path('cart/', views.cart, name='cart'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove-cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('order/', views.create_order, name='create_order'),
    path('order/successfull/', views.successfull_view, name='successfull'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('update-quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    

    
    #path('profile/create/', views.create_profile, name='detail'),
    #path('profile/detail/', views.profile_detail, name='detail'),

]
