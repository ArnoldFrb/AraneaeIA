document.getElementById("upload-img").onchange() = function () {
    let reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function () {
        document.getElementById("img-aranea").setAttribute("src", reader.result);
    };
}


