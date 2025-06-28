let updBtns = document.querySelectorAll(".update-product-cart");
let loc = location.toString();
let page_loc = loc.split('/');

for (let updBtn of updBtns) {
    updBtn.addEventListener('click', function () {
        let productId = this.dataset.productId;
        let productAction = this.dataset.productAction;
        // from base script
        if (gb_user != "AnonymousUser") {
            console.log("client: ", productId, productAction);
            updateUserCart(productId, productAction).then((data)=>{
                if (page_loc[page_loc.length - 2] == 'cart') {
                    // handle the logic of updating quantity, price here later
                    location.reload();
                }
                else{
                    prodPgAfterResponse(data);
                }
            });
            // highlight merch or cart link here later
            // updateHighlight();
        }
        else {
            // window.location();
            console.log(gb_loginpg);
            location.href = '/login/';
        }
    });
}

async function updateUserCart(pId, pAction) {
    try {
        let response = await fetch(
            '/merchandise/update-cart/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // from base script
                },
                body: JSON.stringify({'productId': pId,'productAction': pAction})
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

function prodPgAfterResponse(data) {
    if (page_loc[page_loc.length - 2] == 'merchandise' || page_loc[page_loc.length - 2] == 'product') {
        // console.log("call");
        // updateHighlight();

        let alertAdd = document.querySelector("#pro-add-to");
        alertAdd.style.display = "none";
        alertAdd.addEventListener('click', () => {
            alertAdd.style.display = "none";
        });
        alertAdd.style.display = "block";
        alertAdd.classList.add("pro-add-to-disp");
        if (!data['full']) {
            alertAdd.innerText = `'${data['prodName']}' has been added to cart. Quantity: ${data['updQty']}. Click to dismiss`;
        }
        else {
            alertAdd.innerText = `Can't add the '${data['prodName']}'. Maximum quantity reached. Click to dismiss`;
        }
    }
    // else if(page_loc[page_loc.length - 3] == 'product'){
        // maybe add separate logic for pro page here later
    // }
}

// function updateHighlight() {
//     setTimeout(() => {
//         document.querySelector("#merchHighlight").classList.add("cartHlt");
//     }, 500);
//     document.querySelector("#merchHighlight").classList.remove("cartHlt");
// }