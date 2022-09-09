from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('learn/<int:category_id>', views.learn_card_view, name='learn'),
    path('new-card/', views.add_new_card_view, name='add_new_card'),
    path('new-category/', views.add_new_category_view, name='add_new_category'),
    path('category/<int:category_id>', views.single_category_view, name='single_category'),
    path('delete-category/<int:category_id>', views.delete_category_view, name='delete_category'),
]
