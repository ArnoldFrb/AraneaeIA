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

function entrenar() {
    let form = new FormData(document.getElementById('form-entrenar'))
    fetch('/prueba', {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
}

function simulacion() {
    let form = new FormData(document.getElementById('form-simulacion'))
    fetch('/prueba', {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        console.log(data)
    })
}
