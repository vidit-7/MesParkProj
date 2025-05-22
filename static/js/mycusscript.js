let topBtn = document.querySelector(".scrollToTop");

window.addEventListener('scroll', function() {
    if(document.body.scrollTop > 25 || document.documentElement.scrollTop > 25){
        topBtn.classList.remove("d-none");
    }
    else{
        topBtn.classList.add("d-none");
    }
});

topBtn.addEventListener('click', function(){
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
});