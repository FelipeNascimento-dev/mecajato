from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cliente, Carro
import re
import json
from django.core import serializers
from django.views.decorators.http import require_POST


def clientes(request):
    if request.method == 'GET':
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes/clientes.html', {'clientes': clientes_list})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        cliente = Cliente.objects.filter(cpf=cpf)
        if cliente.exists():
            return render(request, 'clientes/clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos)})

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes/clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)})

        cliente = Cliente(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            cpf=cpf
        )
        cliente.save()

        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(
                carro=carro,
                placa=placa,
                ano=ano,
                cliente=cliente
            )
            car.save()

        return HttpResponse("Cliente e carros salvos com sucesso!")


def att_cliente(request):
    cliente_id = request.POST.get('cliente_id')
    cliente = Cliente.objects.filter(id=cliente_id)
    carros = Carro.objects.filter(cliente=cliente[0])
    cliente_json = json.loads(
        serializers.serialize('json', cliente))[0]['fields']
    id_cliente = json.loads(
        serializers.serialize('json', cliente))[0]['pk']
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields'], 'id': carro['pk']}
                   for carro in carros_json]
    data = {'cliente': cliente_json,
            'carros': carros_json, 'id_cliente': id_cliente}
    return JsonResponse(data)

def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('clientes')

@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')

    carro = Carro.objects.get(id=id)
    list_carros = Carro.objects.filter(placa=placa).exclude(id=id)
    if list_carros.exists():
        return HttpResponse('Placa já existente')

    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()
    return HttpResponse("Dados alterados com sucesso!")

@require_POST
def adicionar_carro(request, id):
    carro = request.POST.get('carro')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')

    cliente = get_object_or_404(Cliente, id=id)

    # valida placa duplicada
    if Carro.objects.filter(placa=placa).exists():
        return JsonResponse({'status': 'error', 'msg': 'Placa já cadastrada'})

    Carro.objects.create(
        cliente=cliente,
        carro=carro,
        placa=placa,
        ano=ano
    )

    return JsonResponse({'status': 'ok'})


def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'?aba=att_cliente&cliente_id={id}')
    except:
        return redirect(reverse('clientes')+f'?aba=att_cliente&cliente_id={id}')


def update_cliente(request, id):
    body = json.loads(request.body)
    nome = body.get('nome')
    sobrenome = body.get('sobrenome')
    email = body.get('email')
    cpf = body.get('cpf')
    cliente = get_object_or_404(Cliente, id=id)
    try:
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse({'status': '200', 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
    except:
        return JsonResponse({'status': '500'})
