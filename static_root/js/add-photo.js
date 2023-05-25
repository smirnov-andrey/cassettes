
// document.getElementById('file').onchange = function () {
//     var src = URL.createObjectURL(this.files[0]);
//     document.getElementById('file-temp').style.display = 'none';
//     document.getElementById('del-image').style.display = 'block';
//     document.getElementById('input-image').style.display = 'block';
//     document.getElementById('input-image').src = src;
// }

var addPhotos = document.querySelectorAll('.add-photo__inputChange');
var delBtn = document.querySelectorAll('.add-photo-delete');

for(var i = 0; i < addPhotos.length; i++){
    addPhotos[i].addEventListener("change", function () {
        var src = URL.createObjectURL( this.files[0]);
        var parent = this.parentElement;
        parent.querySelector('.add-photo-image').src = src;
        parent.querySelector('.add-photo-image').style.display = 'block';
        parent.querySelector('.add-photo-delete').style.display = 'block';
        parent.querySelector('.add-photo__input').style.display = 'none';
    })
}

for(var i = 0; i < delBtn.length; i++){
    delBtn[i].addEventListener("click", function () {
        var parent = this.parentElement;

        parent.querySelector('.add-photo-image').style.display = 'none';
        parent.querySelector('.add-photo__inputChange').value = '';
        parent.querySelector('.add-photo-delete').style.display = 'none';
        parent.querySelector('.add-photo__input').style.display = 'flex';
    })
}
