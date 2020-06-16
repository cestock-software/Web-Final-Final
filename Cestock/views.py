from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from .forms import *
from django.utils import timezone
from django.urls import reverse
from django.db.models import Count
from .models import *
from django.contrib import messages
from .filters import *
import datetime
import locale
# Create your views here.


# def index(request):
#     if request.method =="POST":
#         username=request.POST['username']   
#         password=request.POST['password']     
#         user=authenticate(username=username,password=password) 
#         if user is not None:
#             login(request,user)
#             return redirect('Cestock:PaginaPrincipal')     
#         else:
#             return render(request,"Cestock/login.html") 
#     else:
#         return render(request,"Cestock/login.html")

def get_atencion_detalle(request):
    if request.POST:
        atencion = Atencion_Medica.objects.filter(id=request.POST['id']).first()
        detalle_atencion = Detalle_Atencion.objects.filter(atencion_medica=atencion).first()
        ficha = Carnet_Paciente.objects.filter(nro_ficha=int(str(atencion.nro_ficha))).first()
        date = atencion.fecha_atencion_medica.strftime('%d/%m/%Y')
        nombre_paciente = ficha.rut_paciente.nombre + ' ' + ficha.rut_paciente.ap_paterno + ' ' + ficha.rut_paciente.ap_materno

        output = {
            'id': atencion.id,
            'doctor': atencion.nombre_medico,
            'ficha': str(atencion.nro_ficha),
            'fecha': date,
            'paciente': nombre_paciente,
            'sintomas': detalle_atencion.sintomas,
            'diagnostico': detalle_atencion.diagnostico,
            'tratamiento': detalle_atencion.tratamiento,
            'observacion': detalle_atencion.observacion,
        }
    return JsonResponse(output)

def index(request):
    ''' Vista para iniciar sesión '''
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Cestock:PaginaPrincipal'))
    user=None
    if request.method == 'POST':
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        userobj=UserSistema.objects.filter(rut=rut,tipo_usuario="medico",estado=True).first()
        if userobj:
            user = auth.authenticate(username=userobj.username, password=password)
        form = LoginForm(user, request.POST)

        if user:
            auth.login(request=request, user=user)

            return redirect(reverse('Cestock:PaginaPrincipal'))
        else:
            userobj=UserSistema.objects.filter(rut=rut,tipo_usuario="administrador").first()
            if userobj:
                user = auth.authenticate(username=userobj.username, password=password)
            form = LoginForm(user, request.POST)
            if user:
                auth.login(request=request, user=user)

                return redirect(reverse('Cestock:PaginaPrincipal'))
            else:
                print(form.errors)
                messages.add_message(request, messages.ERROR, 'Rut de usuario o contraseña incorrecta',extra_tags='inicio de sesión')
    else:
        form = LoginForm()
    return render(request, 'Cestock/login.html', {'form': form, 'hidden_register': True})


def logoutt(request):
    auth.logout(request)
    return redirect(reverse('Cestock:loginn'))


def PaginaPrincipal(request):
    # Para que te tome el tiempo local
    locale.setlocale(locale.LC_TIME, '')

    atenciones_medicas_data = []
    dia_actual = datetime.datetime.now()
    # 0 es lunes y 6 es domingo
    numero_dia_en_semana = datetime.datetime.weekday(dia_actual)
    # el lunes es el dia actual menos en numero de este en la semana, el domingo es el primero mas 6
    primer_dia_semana = dia_actual - datetime.timedelta(days=numero_dia_en_semana)
    ultimo_dia_semana = primer_dia_semana + datetime.timedelta(days=6)
    d = datetime.timedelta(days=1)

    # Recorres del primer dia a el ultimo contado las atenciones medicas de ese dia
    while primer_dia_semana <= ultimo_dia_semana:
        if request.user.is_staff:
            atenciones_medicas_dia = Atencion_Medica.objects.filter(fecha_atencion_medica__day=primer_dia_semana.day, fecha_atencion_medica__month=primer_dia_semana.month, fecha_atencion_medica__year=primer_dia_semana.year)
        else:
            atenciones_medicas_dia = Atencion_Medica.objects.filter(nombre_medico=request.user.username,fecha_atencion_medica__day=primer_dia_semana.day, fecha_atencion_medica__month=primer_dia_semana.month, fecha_atencion_medica__year=primer_dia_semana.year)
        # Cambio el formato de la fecha %d es dia en número , %b es mes de manera corta
        date_text = str(primer_dia_semana.strftime("%d %b. "))

        # total(cantidad) de atenciones en ese dia, fecha seleccionada
        info = {}
        info['fecha'] = date_text
        info['total_cant_atenciones'] = len(atenciones_medicas_dia)

        atenciones_medicas_data.append(info)
        primer_dia_semana += d
    if request.user.is_staff:
        ultimas_atenciones_medicas = Atencion_Medica.objects.order_by('-id')[:4]
    else:
        ultimas_atenciones_medicas = Atencion_Medica.objects.filter(nombre_medico=request.user.username).order_by('-id')[:4]
    context = {
        'ultimas_atenciones_medicas': ultimas_atenciones_medicas,
        'atenciones_medicas_data': atenciones_medicas_data,
        'year': dia_actual.year

    }

    return render(request, "Cestock/PaginaPrincipal.html", context)

# def Prescripcion(request, pk=None):
#     obj = Atencion_Medica.objects.filter(id=pk).first()
#     if request.method == "POST":
#         formP = FormPrescripcion(request.POST)
#         if formP.is_valid():
#             presc=formP.save()
#             presc.id = obj.id
#             presc.save()
#             print(formP)
#             return redirect('Cestock:PaginaPrincipal')
#         else:
#             print('form.errors_preinscripcion')
#             print(formP.errors)
#     else:
#         formP = FormPrescripcion()
#     return render(request,'Cestock/Prescripcion.html',{'formP':formP, 'pk': obj})

def crearAtencionMedica(request):
    if request.method == "POST":
        form = FormAtencion(request.POST)
        formP = FormPrescripcion(request.POST)
        if form.is_valid() and formP.is_valid():
            atencionmedica = form.save()
            atencionmedica.fecha_atencion_medica= timezone.now()
            atencionmedica.save()
            print(atencionmedica)
            messages.add_message(request, messages.SUCCESS, 'se ha creado con exito', extra_tags='Atencion Medica')
            presc=formP.save()
            # presc.save()
            # print(presc)
            # if atencionmedica:
            presc.atencion_medica_id = atencionmedica.id
            presc.save()
            return redirect(('Cestock:PaginaPrincipal'))
            # boton()
        else:
            print(form.errors)
    
    form = FormAtencion()
    formP = FormPrescripcion()

    context = {
        'form': form,
        'formP': formP,
        
    }    
    return render(request,'Cestock/AtencionMedica.html',  context )

def validar_rut(request):
    resp = 0
    if request.POST:
        rut = request.POST['rut']
        print(rut)
        usuario = UserSistema.objects.filter(rut=rut).first()
        if usuario:
            resp = 1

        output = {
            'resp': resp,
        }
    return JsonResponse(output)
#-----------------------views Nico--------------------
def ListaPacientes(request):
    pacientes = Paciente.objects.all()

    pacientefilter = PacienteFilter(request.GET, queryset=pacientes)
    pacientes = pacientefilter.qs
    
    context = {'pacientes': pacientes, 'pacientefilter': pacientefilter}

    return render(request, "Cestock/ListaPacientes.html", context)


def StockMedicamento(request):
    medicamentos = Medicamento.objects.all().order_by('id_medicamento')
    filtro = MedicamentoFilter(request.GET, queryset=medicamentos)
    medicamentos = filtro.qs

    context = { 
        'medicamentos': medicamentos,
        'filtro': filtro
    }

    return render(request, "Cestock/StockMedicamento.html", context)

def InfoPersonalPaciente(request, rut):
    paciente = Paciente.objects.get(rut_paciente=rut)

    if request.method == 'GET':
        form = PacienteForm(instance=paciente)
    
    return render(request, 'Cestock/InfoPersonal.html', {'form': form})


def InfoCarnetPaciente(request, rut):
    carnet = Carnet_Paciente.objects.get(rut_paciente=rut)

    if request.method == 'GET':
        form = CarnetForm(instance=carnet)

    return render(request, 'Cestock/InfoCarnet.html', {'form': form})

def ListaAtenciones(request):
    carnets = Carnet_Paciente.objects.all()
    # recetas = Receta_Medica.objects.all()
    atenciones = Atencion_Medica.objects.all()

    filtro = AtencionFilter(request.GET, queryset=atenciones)
    atenciones = filtro.qs

    context = {
        'carnets': carnets,
        # 'recetas': recetas, 
        'atenciones': atenciones, 
        'filtro': filtro
    }
    return render(request, "Cestock/ListaAtenciones.html", context)

def InfoDetalleAtencion(request, id_atencion):
    detalle = Detalle_Atencion.objects.get(atencion_medica=id_atencion)

    if request.method == 'GET':
        form = DetalleAtencionForm(instance=detalle)
    
    context = {
        'form': form
    }

    return render ('Cestock/InfoDetalleAtencion.html', context)

def InfoMedicamentoRecetado(request, id_med):
    med_recetado = Medicamento_Recetado.objects.get(id_receta_medica=id_med)
    medicamentos = Medicamento.objects.all()
    if request.method == 'GET':
        form = MedicamentoRecetadoForm(instance=med_recetado)

    context = {
        'medicamentos': medicamentos,
        'form': form
    }

    return render(request, 'Cestock/InfoMedicamentoRecetado.html', context)


def base(request):   
    return render(request,'Cestock/base.html')