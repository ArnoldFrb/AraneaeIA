function uploadImg(e) {
    if (e.target.files && e.target.files[0]) {
        onUpload(e);

        var reader = new FileReader();

        reader.readAsDataURL(e.target.files[0]);

        reader.onload = () => {
            setImage(reader.result);
        };
    }
};
