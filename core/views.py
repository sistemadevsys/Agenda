from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User

#def index(request):
#    return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        
        messages.error(request, "Usuário ou senha inválida.")
    
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(days=180) #para retornar com vencidos há 1h
    evento =  Evento.objects.filter(usuario=usuario,
                                    data_evento__gt=data_atual)#__gt só Maior, __lt só Menor
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local_evento = request.POST.get('local_evento')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.local_evento = local_evento
                evento.save()
            #Evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento, descricao=descricao, local_evento=local_evento)
        else:
            Evento.objects.create(titulo=titulo,
                                data_evento=data_evento,
                                descricao=descricao,
                                local_evento=local_evento,
                                usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

# retornar JsonResponse para trabalhar com JavaScript, Ajax...
# para pegar por usuário (id), sem decoretor. @login_required(login_url='/login/')
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario) #request.user
    evento =  Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False) #safe=False porque nao é dicionário.



def index(request):
    # modelo de outro projeto
    nome_da_empresa = "Agendamentos"
    descricao_da_empresa = "Desenvolve páginas web de agenda."

    contato_empresa = {
        "endereco": "Campos do Jordão - SP",
        "telefone": "12997865680",
        "email": "c-costa-@outlook.com.br"
    }

    cursos_home = {
        "1": {"titulo": "Django Fundamentos", "descricao": "Aprenda toda a base do Django agora mesmo!!"},
        "2": {"titulo": "Flask Fundamentos", "descricao": "Aprenda toda a base do Flask agora mesmo!!"},
        "3": {"titulo": "Python OO", "descricao": "Aprenda a orientação à objetos com Python agora mesmo!!"},
    }

    return render(request, 'index.html', {'nome_empresa':nome_da_empresa, 'descricao_empresa':descricao_da_empresa,
                                                  'contato_empresa': contato_empresa, 'cursos_home':cursos_home})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')