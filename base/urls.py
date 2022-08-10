from django.urls import path

from .views import TaskDelete, TaskList, TaskCreate, TaskUpdate, CategoryCreate

app_name = 'base'
urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),

    path('category-create/', CategoryCreate.as_view(), name='category-create'),
]
