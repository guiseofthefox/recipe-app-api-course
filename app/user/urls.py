"""
URL mappings for the user API
"""
from django.urls import path

from user import views

app_name = 'user'  # namespace for the URL names; used in reverse() method

urlpatterns = [
    # path(<route>, <view_function>, <name_for_reverse_lookup>)
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
