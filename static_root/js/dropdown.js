window.onload = function() {
    var dropdown = document.querySelectorAll(".dropdown__select")

    var options = document.querySelectorAll(".dropdown__options>li")

    var allOptions = document.querySelectorAll('.dropdown__options');

    for (let i = 0; i < dropdown.length; i++) {
        dropdown[i].addEventListener("click", function() {
            var parentEl = this.parentElement;
            for (let j = 0; j < allOptions.length; j++) {
                if(i == j) continue;
                allOptions[j].classList.remove('show');
            }
            parentEl.querySelector('.dropdown__options').classList.toggle('show');
        })
    }

    for (let i = 0; i < options.length; i++) {
        options[i].addEventListener("click", function() {
            var parentEl = this.parentElement.parentElement;
            for (let j = 0; j < parentEl.querySelectorAll(".dropdown__options>li").length; j++) {
                parentEl.querySelectorAll(".dropdown__options>li")[j].classList.remove("active");
            }
            this.classList.add("active");
            parentEl.querySelector('.dropdown__select').innerText = this.outerText;
            parentEl.querySelector('.dropdown__options').classList.toggle('show');
        });
    }
};


