let addCommentBtn = document.querySelector("#btn-add-comment");
let commentInp = document.querySelector("#comment-data");
let remCommentBtns = document.querySelectorAll(".remove-comment");
let commentConf = document.querySelector("#comm-conf");
let commentRemCancel = document.querySelector("#comm-rem-cancel");
let commentRemConf = document.querySelector("#comm-rem-conf");
let commentInputDiv = document.querySelector("#comment-input-div");

let replyBtns = document.querySelectorAll(".btn-prompt-reply");
let replyInputDivCont = document.querySelector("#reply-input-cont");
let replySubmitBtn = document.querySelector("#btn-add-reply");
let replyCancelBtn = document.querySelector("#btn-cancel-reply");
let replyInput = document.querySelector("#reply-data");
let replyingToUser = document.querySelector("#replying-to-info");

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

let activeCommentId = -1;

for(let replyBtn of replyBtns){
    replyBtn.addEventListener('click', function(){
        let cId = this.dataset.commentId;
        let repUserName = this.dataset.repuserName;
        let repCommentBody = this.dataset.repcommentBody;
        replyingToUser.textContent = `Replying to: @${repUserName}: ${repCommentBody}`;
        activeCommentId = cId;
        console.log("selected comment ", activeCommentId);

        replyInputDivCont.classList.remove("d-none");
        replyInput.focus();
        commentInputDiv.classList.add("d-none");
    });
}

replySubmitBtn.onclick = function () {
    let replyData = replyInput.value;
    if(activeCommentId == -1){
        console.log("no comment selected");
        return;
    }
    if(replyData.trim() !== ''){
        replySubmitBtn.disabled = true;
        sendReplyToAdd(activeCommentId, replyData).then(()=>{
            location.reload();
        }).catch((err)=>{  
            replyInput.value = replyData;
            console.log(err);
        }).finally(()=>{
            replySubmitBtn.disabled = false;
            replyInputDivCont.classList.add("d-none");
            commentInputDiv.classList.remove("d-none");
            replyingToUser.textContent = "";
            replyInput.value = "";
            activeCommentId = -1;
        });
    }
    else{
        console.log("empty reply");
    }
}

replyCancelBtn.addEventListener('click', function(){
    replyInputDivCont.classList.add("d-none");
    commentInputDiv.classList.remove("d-none");
    replyingToUser.textContent = "";
    activeCommentId = -1;
});

for(let remBtn of remCommentBtns){
    remBtn.addEventListener('click', function(){
        commentConf.style.display = "block";
        commentConf.classList.remove("d-none");
        let commentId = this.dataset.commentremId;
        let commentType = this.dataset.remtype;
        commentRemConf.setAttribute('data-commentrem-id',commentId);
        commentRemConf.setAttribute('data-remtype', commentType);
        console.log("rem com", commentId, commentType);
    });
}


commentRemConf.addEventListener('click', function(){
    let commentId = this.dataset.commentremId;
    let commentType = this.dataset.remtype;
    console.log(commentId);
    commentConf.style.display = "none";
    commentConf.classList.add("d-none");
    sendCommentToDelete(commentId, commentType).then(()=>{
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

async function sendReplyToAdd(cId, replyBody) {
    try {
        let response = await fetch(
            `/community/add-reply/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // from base script
                },
                body: JSON.stringify({'commentId': cId,'replyData': replyBody})
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

async function sendCommentToDelete(commentId, commentType){
    try {
        let response = await fetch(
            `/community/delete-comment/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // from base script
                },
                body: JSON.stringify({'commentId':commentId, 'commentType': commentType})
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