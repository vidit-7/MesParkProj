const supportType = document.querySelector("#id_support_type");
// const typeDiv = document.querySelector("#supp_type_sel");
const bookingSelector = document.querySelector("#id_booking_sup");
const bookingSelectorDiv = document.querySelector("#div_id_booking_sup")
const orderSelector = document.querySelector("#id_ord_sup");
const orderSelectorDiv = document.querySelector("#div_id_ord_sup")

// typeDiv.style.display = "none";
// bookingSelector.setAttribute("disabled","true");
// orderSelector.setAttribute("disabled","true");

changeMenuDisplay();

supportType.addEventListener('change', function(){
    changeMenuDisplay();
});

function changeMenuDisplay(){
    if(supportType.value == "" || supportType.value == "other"){
        bookingSelectorDiv.style.display = "none";
        bookingSelector.value = "";
        orderSelectorDiv.style.display = "none";
        orderSelector.value = "";
    }
    else if(supportType.value == "booking"){
        bookingSelectorDiv.style.display = "block";
        orderSelectorDiv.style.display = "none";
        orderSelector.value = "";
    }
    else if(supportType.value == "order"){
        orderSelectorDiv.style.display = "block";
        bookingSelectorDiv.style.display = "none";
        bookingSelector.value = "";
    }
    else{
        console.log("invalid selection");
    }
}