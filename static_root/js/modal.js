var btnModal = document.querySelectorAll('.btn-modal');

var btnClose =  document.querySelectorAll('.modal__close');


for( var i = 0; i < btnClose.length; i++){
    btnClose[i].addEventListener("click", function() {
        var modal = this.parentElement.parentElement;
        modal.classList.remove("active");
    })
}


for( var i = 0; i < btnModal.length; i++){
    btnModal[i].addEventListener("click", function() {
        var modal = document.querySelector('#'+this.getAttribute('data-modal'));
        modal.classList.add("active");
    })
}