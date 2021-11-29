document.getElementById("upload-img").onchange = function (e) {
    let reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function () {
        let preview = document.getElementById("img-aranea");
        preview.setAttribute("src", reader.result);
    };
};

