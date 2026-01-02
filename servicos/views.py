from django.shortcuts import render


def novo_servico(request):
    return render(request, 'servicos/novo_servico.html')
