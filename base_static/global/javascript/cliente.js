function add_carro(){
    container = document.getElementById("form-carro")
    html = "<br> <div class='row'> <div class='col-md'> <input type='text' placeholder='carro' class='form-control' name='carro'> </div> <div class='col-md'> <input type='text' placeholder='placa' class='form-control' name='placa'> </div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='ano'>  </div> </div>"
    container.innerHTML += html
}


function exibir_form(tipo){
    add_cliente = document.getElementById("add_cliente")
    att_cliente = document.getElementById("att_cliente")

    if(tipo == "1"){
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"
    }
    else if(tipo == "2"){
        add_cliente.style.display = "none"
        att_cliente.style.display = "block"
    }
}

function dados_cliente(){
    cliente = document.getElementById("cliente_select")
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    cliente_id = cliente.value
    data = new FormData()
    data.append("cliente_id", cliente_id)
    fetch("/clientes/atualizar_cliente/",{
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }). then(function(result){
        return result.json()
    }).then(function(data){
            console.log(data)
        document.getElementById('form-att-cliente').style.display = "block"

        id_cliente = document.getElementById('id_cliente')
        id_cliente.value = data['id_cliente']

        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['cliente']['sobrenome']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ""
        for(i=0; i < data['carros'].length; i++){
            console.log(data['carros'][i]['fields']['carro'])

            div_carros.innerHTML += "<form action='/clientes/update_carro/" + data['carros'][i]['id'] +"/' method='POST'>\
            <div class='row'>\
                <div class='col-md'>\
                    <input class='form-control' type='text' name='carro' value='" + data['carros'][i]['fields']['carro'] + "'>\
                </div>\
                <div class='col-md'>\
                    <input class='form-control' type='text' name='placa' value='" + data['carros'][i]['fields']['placa'] + "'>\
                </div>\
                <div class='col-md'>\
                    <input class='form-control' type='text' name='ano' value='" + data['carros'][i]['fields']['ano'] + "'>\
                </div>\
                <div class='col-md'>\
                    <input class='btn btn-success' type='submit' value='Salvar Alterações'>\
                </div>\
                <a href='/clientes/excluir_carro/" + data['carros'][i]['id'] + "/' id='excluir_carro' class='btn btn-danger'>Excluir carro</a>\
                </form>\
            </div><br>"
        }    
    })
}

function update_cliente(){
    nome = document.getElementById("nome").value
    sobrenome = document.getElementById("sobrenome").value
    email = document.getElementById("email").value
    cpf = document.getElementById("cpf").value
    id_cliente = document.getElementById("id_cliente").value

    fetch('/clientes/update_cliente/' + id_cliente + '/', {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        }, 
        body: JSON.stringify({
            'nome': nome,
            'sobrenome': sobrenome,
            'email': email,
            'cpf': cpf
        })
    }).then(function(result){
        return result.json()
    }).then(function(data){

        if (data['status'] == '200'){
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']
            console.log("Dados atualizados com sucesso")
        }else{
            console.log("Erro ao atualizar cliente")
        }
    })
}

function excluirCliente() {
    const id = document.getElementById("id_cliente").value
    window.location.href = `/clientes/excluir_cliente/${id}/`
}