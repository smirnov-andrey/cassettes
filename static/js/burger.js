
var burgerBtn = document.querySelector('.burger');
var burgerMenu = document.querySelector('.header-menu__wrapper');


console.log(burgerBtn)
burgerBtn.addEventListener("click", function() {
    burgerMenu.classList.toggle('burger-show');
})



