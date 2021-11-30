function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("upload-img").onchange = function (e) {
    let reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function () {
        let preview = document.getElementById("render-img");
        preview.setAttribute("src", reader.result);
    };
};

function entrenamiento() {
    let div = document.getElementById('form-guardar')

    div.innerHTML =
        '<div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status">' +
        '<span class="visually-hidden">Cargando</span>' +
        '</div>'

    let form = new FormData(document.getElementById('form-entrenar'))

    fetch('/entrenar', {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        if (data.status && data.status === true) {
            div.innerHTML =
                '<div class="card">' +
                '<div class="card-header">Guardar entrenamiento</div>' +
                '<div class="card-body">' +
                '<div class="mb-3 row">' +
                '<label for="staticEmail" class="col-sm-2 col-form-label">Nombre</label>' +
                '<div class="col-sm-10">' +
                '<input type="text" class="form-control" name="title">' +
                '</div>' +
                '</div>' +
                '<div class="mb-3 row">' +
                '<label for="inputPassword" class="col-sm-2 col-form-label">Descripción</label>' +
                '<div class="col-sm-10">' +
                '<textarea rows="10" cols="50" class="form-control" name="desc"></textarea>' +
                '</div>' +
                '</div>' +
                '<button type="button" class="btn btn-primary " onclick="guardar()">Guardar</button>' +
                '</div>' +
                '</div>' +
                '<div class="mt-3" id="response-guardar"></div>'
        } else {
            div.innerHTML =
                '<div class="alert alert-danger" role="alert">' +
                data.title + ': ' + data.messege +
                '</div>'
        }

    })
}

function guardar() {
    let div = document.getElementById('response-guardar')

    div.innerHTML =
        '<div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status">' +
        '<span class="visually-hidden">Cargando</span>' +
        '</div>'

    let form = new FormData(document.getElementById('form-entrenar'))

    fetch('/guardar', {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        if (data.state && data.state === true) {
            div.innerHTML =
                '<div class="alert alert-success" role="alert">' +
                data.messege +
                '</div>'
        } else {
            div.innerHTML =
                '<div class="alert alert-danger" role="alert">' +
                data.messege +
                '</div>'
        }

    })
}

function simulacion() {
    let div = document.getElementById('response')

    div.innerHTML =
        '<div class="spinner-border text-success" style="width: 3rem; height: 3rem;" role="status">' +
        '<span class="visually-hidden">Cargando</span>' +
        '</div>'

    let form = new FormData(document.getElementById('form-simulacion'))

    fetch('/simulacion', {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        div.innerHTML =
            '<div class="card">' +
            '<div class="card-header">' +
            '<h5>¿Esta es la arraña que estas buscando?</h5>' +
            '<p>Nombre: ' + data.name + '</p>' +
            '</div>' +
            '<div class="justify-content-center" >' +
            "<img class='img-6' src='" + data.uri + "'>" +
            '</div>' +
            '<hr />' +
            '<div class="card-body">' +
            '<h5 class="card-title">Descripcion</h5>' +
            '<p class="card-text">' + data.desc + '</p>' +
            '</div>' +
            '</div>'
    })
}

