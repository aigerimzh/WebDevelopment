from django.contrib import admin
from django.urls import path, include
from .views.views import TasklistList,TasklistDetail , task_list, task_detail
from .views.auth import Register
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    path('task_list/', TasklistList.as_view()),
    path('task_list/<int:pk>/', TasklistDetail.as_view()),
    path('task_list/<int:pk>/tasks/', task_list),
    path('tasks/<int:pk>/', task_detail),
    # path('users/', UserList.as_view()),
    path('register/', Register.as_view()),
    path('login/', obtain_jwt_token),

]
