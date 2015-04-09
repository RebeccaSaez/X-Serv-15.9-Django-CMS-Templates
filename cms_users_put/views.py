from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Table
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
import time

# Create your views here.


def login(request):
    if request.user.is_authenticated():
        message = "You're: " + request.user.username
        link = "/admin/logout/"
        name = "Logout"
    else:
        message = "You aren't registred"
        link = "/admin/"
        name = "Login"
    return (message, link, name, request.user.username)


def all_no(request):
    list = Table.objects.all()
    out = "<ul>\n"
    for i in list:
        out += "<li><a href=agenda/" + i.name + ">" + i.name + "</a></li>\n"
    out += "</ul>\n"
    (message, link, name, user) = login(request)
    out += "<br>" + message + "<br><a href='" + link + "'>" + name + "</a>"
    return HttpResponse(out)


def all_template(request):
    (message, link, name, user) = login(request)
    list = Table.objects.all()
    template = get_template("index.html")
    date = time.strftime("%c")
    c = Context({'contenido': "Todos tus numeros son:",
                 'lista': list,
                 'fecha': "Ultima consulta: " + date,
                 'recurso': "Numeros guardados",
                 'mensaje_out': message,
                 'link_out': link,
                 'name_out': name})
    return HttpResponse(template.render(c))


@csrf_exempt
def number(request, recurso):
    if request.method == "GET":
        list = Table.objects.filter(name=recurso)
        if not list:
            phone = notfound(request, recurso)
        else:
            phone = ""
            for i in list:
                phone += i.name + ": " + str(i.number) + " "
    if request.method == "PUT":
        if request.user.is_authenticated():
            new = Table(name=recurso, number=request.body)
            new.save()
            phone = ("Saved Page, check it with GET")
        else:
            phone = ("You must be registred")
    (message, link, name, user) = login(request)
    return (phone, message, link, name, user)


@csrf_exempt
def number_no(request, recurso):
    (phone, message, link, name, user) = number(request, recurso)
    out = "<br>" + message + "<br><a href='" + link + "'>" + name + "</a>"
    return HttpResponse(phone + out)


@csrf_exempt
def number_template(request, recurso):
    (phone, message, link, name, user) = number(request, recurso)
    template = get_template("index.html")
    date = time.strftime("%c")
    c = Context({'contenido': phone,
                 'fecha': "Ultimo cambio: " + date,
                 'recurso': "Telefono de " + recurso,
                 'mensaje_out': message,
                 'link_out': link,
                 'name_out': name})
    return HttpResponse(template.render(c))


def notfound(request, recurso):
    out = ("Not found: " + recurso)
    return out
