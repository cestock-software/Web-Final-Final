from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('crear/', views.UserCreate.as_view(), name='crear_doctor'),
    path('editar/<int:pk>/', views.user_update, name='editar_doctor'),
    path('lista/', views.lista_users, name='lista_users'),
    path('lista2/', views.lista_users2, name='lista_users2'),
    path('eliminar/', views.eliminar_doctor, name='eliminar_doctor'),
    path('validar/', views.validar_usuario, name='validar_usuario'),
    path('invalidar/', views.invalidar_usuario, name='invalidar_usuario'),
    #envian los datos de los usuarios a listas invalidar_usuario
    path('datatable2/', views.usuario_lista_database2, name='usuario_lista_database2'),
    path('datatable/', views.usuario_lista_database, name='usuario_lista_database'),
    path('update/password/', views.user_password_change, name='password_update'),

]