let numVisitorsSel = document.querySelector("#id_num_visitors");
let bookingDateSel = document.querySelector("#id_booking_date");
// let nextFreeSlot = document.querySelector("#nextFreeSlot");

let spanTourId = document.querySelector("#spantour_id");
let tourId = spanTourId.dataset.tourId;

let displayBookable = document.querySelector("#isBookable");

numVisitorsSel.addEventListener('change', function(){
    console.log(tourId);
    n_vis = numVisitorsSel.value;
    b_date = bookingDateSel.value;
    
    if(n_vis!="" && b_date!=""){    
        getTourData(tourId, n_vis, b_date, 'check').then((data)=>{
            changeDispText(data);
        }).catch(err=>console.log(err));
    }
});

bookingDateSel.addEventListener('change', function(){
    console.log(tourId);
    n_vis = numVisitorsSel.value;
    b_date = bookingDateSel.value;
    if(n_vis!="" && b_date!=""){    
        getTourData(tourId, n_vis, b_date, 'check').then((data)=>{
            changeDispText(data);
        }).catch(err=>console.log(err));
    }
});

function changeDispText(data){
    displayBookable.classList.remove('text-secondary');
    displayBookable.textContent = data['show_message'];
    if(!data["success"]){
        displayBookable.classList.remove('text-success');
        displayBookable.classList.add('text-danger');
    }
    else{
        displayBookable.classList.remove('text-danger');
        displayBookable.classList.add('text-success');
    }
}

async function getTourData(tourId, numVis, bookDate, purpose) {
    try {
        let response = await fetch(
            '/tours/check-booking-status/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // from base script
                },
                body: JSON.stringify({'tourId':tourId, 'numVis': numVis, 'bookDate': bookDate, 'purpose': null})
            }
        );
        let data = await response.json();
        console.log(data);
        return data;
    }
    catch (e) {
        console.log(e);
    }
}

