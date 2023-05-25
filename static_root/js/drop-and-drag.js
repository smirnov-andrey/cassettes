
var dropContainer = document.querySelectorAll('.dropContainer');

for(var i = 0; i < dropContainer.length; i++){
    dropContainer[i].addEventListener("dragenter", function (evt) {
        evt.preventDefault();
    });
    dropContainer[i].addEventListener("dragover", function (evt) {
        evt.preventDefault();
    });
    dropContainer[i].addEventListener("drop", function (evt) {
        var parent = this;
        console.log(evt.dataTransfer.files);
        parent.querySelector('.fileInput').files = evt.dataTransfer.files;
        const dT = new DataTransfer();
        dT.items.add(evt.dataTransfer.files[0]);
        parent.querySelector('.fileInput').files = dT.files;
        evt.preventDefault();

        var src = URL.createObjectURL( parent.querySelector('.fileInput').files[0]);
        parent.querySelector('.dropContainer__image-wrapper').style.display = 'flex';
        parent.querySelector('.dropContainer__image-wrapper>.preview').src = src;
    })
}


var addPhotos = document.querySelectorAll('.fileInput');
var delBtn = document.querySelectorAll('.img-delete');

for(var i = 0; i < addPhotos.length; i++){
    addPhotos[i].addEventListener("change", function () {
        var src = URL.createObjectURL( this.files[0]);
        var parent = this.parentElement;
        parent.querySelector('.dropContainer__image-wrapper>.preview').src = src;
        parent.querySelector('.dropContainer__image-wrapper').style.display = 'flex';
    })
}

for(var i = 0; i < delBtn.length; i++){
    delBtn[i].addEventListener("click", function () {
        var parent = this.parentElement.parentElement;

        parent.querySelector('.dropContainer__image-wrapper').style.display = 'none';
        parent.querySelector('.fileInput').value = '';
    })
}