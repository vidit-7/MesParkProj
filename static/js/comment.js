let addCommentBtn = document.querySelector("#add-comment");
let commentInp = document.querySelector("#comment-data");
let remCommentBtns = document.querySelectorAll(".remove-comment");
let commentConf = document.querySelector("#comm-conf");
let commentRemCancel = document.querySelector("#comm-rem-cancel");
let commentRemConf = document.querySelector("#comm-rem-conf");

let loc = location.toString();
let page_loc = loc.split('/');

commentConf.style.display = "none";

addCommentBtn.addEventListener('click', function(){
    let pId = this.dataset.postId;
    let commentData = commentInp.value;
    console.log(pId, commentData);
    if(commentData.trim() !== ''){
        commentInp.value = "";
        addCommentBtn.disabled = true;
        sendCommentToAdd(pId,commentData).then(()=>{
            location.reload();
        }).catch((err)=>{  
            commentInp.value = commentData;
            console.log(err);
        }).finally(()=>{
            addCommentBtn.disabled = false;
        });
    }
    else{
        console.log("empty comment");
    }
});


for(let remBtn of remCommentBtns){
    remBtn.addEventListener('click', function(){
        console.log("rem com");
        commentConf.style.display = "block";
        commentConf.classList.remove("d-none");
        let commentId = this.dataset.commentremId;
        commentRemConf.setAttribute('data-commentrem-id',commentId);
    });
}


commentRemConf.addEventListener('click', function(){
    let commentId = this.dataset.commentremId;
    console.log(commentId);
    commentConf.style.display = "none";
    commentConf.classList.add("d-none");
    sendCommentToDelete(commentId).then(()=>{
        location.reload();
    }).catch(err=>console.log(err));
});

commentRemCancel.addEventListener('click', function(){
    commentConf.style.display = "none";
    commentConf.classList.add("d-none");
});


async function sendCommentToAdd(pId, commentBody) {
    try {
        let response = await fetch(
            `/community/add-comment/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // from base script
                },
                body: JSON.stringify({'postId':pId,'commentData': commentBody})
            }
        );
        let data = await response.json();
        console.log(data);
        // handle the logic of adding comment w/o reloading here later
        // location.reload();
    }
    catch (e) {
        console.log(e);
    }
}

async function sendCommentToDelete(commentId){
    try {
        let response = await fetch(
            `/community/delete-comment/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // from base script
                },
                body: JSON.stringify({'commentId':commentId})
            }
        );
        let data = await response.json();
        console.log(data);
        // handle the logic of removing comment w/o reloading here later
        // location.reload();
    }
    catch (e) {
        console.log(e);
    }
}