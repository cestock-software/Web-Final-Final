from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import UserSistema
from .forms import UserMedicoForm, UserMedicoEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from functools import reduce
from django.http import JsonResponse, HttpResponse
import operator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.
class UserCreate(generic.CreateView):
    # Vista del formulario para agregar un usuario 
    model = UserSistema
    template_name = "users/user_form.html"
    form_class = UserMedicoForm
    success_url = reverse_lazy('Cestock:PaginaPrincipal')

    def form_valid(self, form):
        return super().form_valid(form)


def user_update(request, pk):
    # Vista para el formulario de creación del modelo usuario
    user_editado = None
    user_editado = get_object_or_404(UserSistema, pk=pk)
    print(user_editado)
    if request.method == 'POST':

        form = UserMedicoEditForm(request.POST, request.FILES, instance=user_editado)
        print(request.POST)
        if form.is_valid():
            user_editado = form.save()
            user_editado.save()
            messages.add_message(request, messages.SUCCESS, 'se ha editado con exito', extra_tags='Editar perfil de usuario')
            if request.user.is_staff:
                return redirect(reverse('users:lista_users'))
            else:
                return redirect(reverse('Cestock:PaginaPrincipal'))
        else:
            print(form.errors)
    else:
        form = UserMedicoEditForm(instance=user_editado)
    data = {
        'form': form,
        'user_editado': user_editado
    }

    return render(request, 'users/user_form.html', data)


# Vista listado de usuarios(doctores)
def lista_users(request):
    context = {
    }
    print("user_list")
    return render(request, 'users/lista_users.html', context)

def lista_users2(request):
    context = {
    }
    print("user_list")
    return render(request, 'users/lista_users_false.html', context)


# Vista busqueda en listado de usuarios(doctores)
def usuario_lista_database(request):
    start = int(request.POST["start"])
    per_page = int(request.POST["length"])
    search = request.POST["search[value]"].strip()
    order_column = int(request.POST["order[0][column]"])
    order_dir = request.POST["order[0][dir]"]

    page = (start / per_page) + 1

    user_list = UserSistema.objects.filter(estado=True)
    
    print(user_list)
    if search != "":
        keywords = search.split()

        id_qs = reduce(operator.or_, (Q(id__icontains=keyword.strip()) for keyword in keywords))
        username_qs = reduce(operator.or_, (Q(username__icontains=keyword.strip()) for keyword in keywords))
        rut_qs = reduce(operator.or_, (Q(rut__icontains=keyword.strip()) for keyword in keywords))
        email_qs = reduce(operator.or_, (Q(email__icontains=keyword.strip()) for keyword in keywords))
        tipo_usuario_qs = reduce(operator.or_, (Q(tipo_usuario__icontains=keyword.strip()) for keyword in keywords))

        if len(keywords) > 0:
            user_list = user_list.filter(Q(id_qs) | Q(username_qs) | Q(rut_qs) | Q(email_qs) | Q(tipo_usuario_qs)) 

    user_list = user_list.order_by('-date_joined')

    total = user_list.count()

    paginator = Paginator(user_list, per_page)  # Show per_page

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    dataArray = []
    for user in users:
        print(user.estado)
        print('..-..-.-.-.-.-')
        try:

            url_edit = reverse('users:editar_doctor', kwargs={'pk': user.id})
            edit_button = '<a href="' + url_edit + '" title="Editar"  class="btn btn-link"><i class="fas fa-pen"></i></a>'
            invalidar_button = '<button class="btn btn-link" title="Invalidar"  onclick="invalidar_user(' + str(user.id) + ')"  ><i class="fa fa-ban"></i></button>'
            
            if user.is_staff:
                actions = edit_button 
            else:
                actions = edit_button + invalidar_button

            # dataArray.append([
            #     user.id,
            #     user.username,
            #     user.rut,
            #     user.email,
            #     user.tipo_usuario,
            #     actions,
            # ])

            if user.rut:
                # se les retira . y guion de existir un rut con este formato
                rut_sin_puntos = user.rut.replace('.', '-')
                rut = rut_sin_puntos.replace('-', '')

                cont = 0
                i = 0
                rut_con_formato = ''
                rut_invertido = ''
                rut = str(rut)

                i = len(rut) - 1
                # Se recorre los numeros del rut y se invierten  para ponerle el guion y los . X-XXX.XXX.XX
                while i >= 0:
                    rut_invertido += rut[i]
                    if i == len(rut) - 1:
                        rut_invertido += '-'
                    elif cont == 3:
                        rut_invertido += '.'
                        cont = 0

                    i -= 1
                    cont += 1
                # Se invierte otra vez el rut para que quede con el formato correcto
                j = len(rut_invertido) - 1
                while j >= 0:
                    if rut_invertido[len(rut_invertido) - 1] != '.':
                        rut_con_formato += rut_invertido[j]
                    elif j != len(rut_invertido) - 1:
                        rut_con_formato += rut_invertido[j]
                    j -= 1
            # print(rut_con_formato)
            dataArray.append([
                user.id,
                user.username,
                rut_con_formato,
                user.email,
                user.tipo_usuario,
                actions,
            ])
        except Exception as e:
            print(e)

    if order_dir == 'asc':
        dataArray = sorted(dataArray, key=lambda x: x[order_column])
    else:
        dataArray = sorted(dataArray, key=lambda x: x[order_column], reverse=True)

    output = {
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": dataArray
    }
    return JsonResponse(output)

def usuario_lista_database2(request):
    start = int(request.POST["start"])
    per_page = int(request.POST["length"])
    search = request.POST["search[value]"].strip()
    order_column = int(request.POST["order[0][column]"])
    order_dir = request.POST["order[0][dir]"]

    page = (start / per_page) + 1

    user_list = UserSistema.objects.filter(estado=False)
    print(user_list)
    if search != "":
        keywords = search.split()

        id_qs = reduce(operator.or_, (Q(id__icontains=keyword.strip()) for keyword in keywords))
        username_qs = reduce(operator.or_, (Q(username__icontains=keyword.strip()) for keyword in keywords))
        rut_qs = reduce(operator.or_, (Q(rut__icontains=keyword.strip()) for keyword in keywords))
        email_qs = reduce(operator.or_, (Q(email__icontains=keyword.strip()) for keyword in keywords))
        tipo_usuario_qs = reduce(operator.or_, (Q(tipo_usuario__icontains=keyword.strip()) for keyword in keywords))

        if len(keywords) > 0:
            user_list = user_list.filter(Q(id_qs) | Q(username_qs) | Q(rut_qs) | Q(email_qs) | Q(tipo_usuario_qs)) 

    user_list = user_list.order_by('-date_joined')

    total = user_list.count()

    paginator = Paginator(user_list, per_page)  # Show per_page

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    dataArray = []
    for user in users:
        print('................................')
        print(user.estado)
        try:
            
            # url_edit = reverse('users:editar_doctor', kwargs={'pk': user.id})
            # edit_button = '<a href="' + url_edit + '" class="btn btn-link"><i class="fas fa-pen"></i></a>'
            delete_button = '<button class="btn btn-link" onclick="delete_user(' + str(user.id) + ')" title="Eliminar"  ><i class="fas fa-trash"></i></button>'
            validar_button = '<button class="btn btn-link" onclick="validar_user(' + str(user.id) + ')" title="Validar" ><i class="fa fa-check"></i></button>'

            if user.is_staff:
                actions = validar_button
            else:
                actions = validar_button + delete_button

            # dataArray.append([
            #     user.id,
            #     user.username,
            #     user.rut,
            #     user.email,
            #     user.tipo_usuario,
            #     actions,
            # ])

            if user.rut:
                # se les retira . y guion de existir un rut con este formato
                rut_sin_puntos = user.rut.replace('.', '-')
                rut = rut_sin_puntos.replace('-', '')

                cont = 0
                i = 0
                rut_con_formato = ''
                rut_invertido = ''
                rut = str(rut)

                i = len(rut) - 1
                # Se recorre los numeros del rut y se invierten  para ponerle el guion y los . X-XXX.XXX.XX
                while i >= 0:
                    rut_invertido += rut[i]
                    if i == len(rut) - 1:
                        rut_invertido += '-'
                    elif cont == 3:
                        rut_invertido += '.'
                        cont = 0

                    i -= 1
                    cont += 1
                # Se invierte otra vez el rut para que quede con el formato correcto
                j = len(rut_invertido) - 1
                while j >= 0:
                    if rut_invertido[len(rut_invertido) - 1] != '.':
                        rut_con_formato += rut_invertido[j]
                    elif j != len(rut_invertido) - 1:
                        rut_con_formato += rut_invertido[j]
                    j -= 1
            # print(rut_con_formato)
            dataArray.append([
                user.id,
                user.username,
                rut_con_formato,
                user.email,
                user.tipo_usuario,
                actions,
            ])
        except Exception as e:
            print(e)

    if order_dir == 'asc':
        dataArray = sorted(dataArray, key=lambda x: x[order_column])
    else:
        dataArray = sorted(dataArray, key=lambda x: x[order_column], reverse=True)

    output = {
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": dataArray
    }
    return JsonResponse(output)

def eliminar_doctor(request):
    if request.POST:
        user = UserSistema.objects.filter(id=request.POST['id'])
        user.delete()
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})

def validar_usuario(request):
    if request.POST:
        user = UserSistema.objects.filter(id=request.POST['id']).first()
        user.estado=True
        user.save()
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})

def invalidar_usuario(request):
    if request.POST:
        user = UserSistema.objects.filter(id=request.POST['id']).first()
        user.estado=False
        user.save()
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})

def user_password_change(request):
    ''' Vista del formulario para cambiar contraseña de un usuario'''

    user = request.user
    form = PasswordChangeForm(user)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            print(form)
            print('tas pendejo')
            user = form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('Cestock:PaginaPrincipal'))
        else:
            print(form.errors)
    return render(request, 'users/password_update.html', {'form': form, 'user': user})