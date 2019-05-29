from django.urls import path

##from app.views import file_list, file_content
from app import views
# Определите и зарегистрируйте конвертер для определения даты в урлах и наоборот урла по датам


urlpatterns = [
    # Определите схему урлов с привязкой к отображениям .views.file_list и .views.file_content
    path('', views.file_list, name='file_list'),
    ######path('[\d{4}-\d{2}-\d{2}]', views.file_content, name='file_list'),
    path('^file_list/(?P<date>[0-9]{4}-[0-9]{2}-?P[0-9]{2})/', views.file_content, name='file_list'),
    ####path('^file_content/(?P<name>[file_name_]+[0-9]*\.+\D*)', views.file_content, name='file_content'),
    path('file_content/<name>', views.file_content, name='file_content'),
]
