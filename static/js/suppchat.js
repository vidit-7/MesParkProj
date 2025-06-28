const messageInp = document.querySelector("#message-data");
const sendMessageBtn = document.querySelector("#send-suppmsg");
const messageSectionDiv = document.querySelector("#chatArea");

function scrollToLastChatMsg(){
    // messageInp.style.height = "auto";
    let lastMsg = messageSectionDiv.lastElementChild;
    if(lastMsg!=null){
        lastMsg.scrollIntoView({behaviour: "instant", block:"end"});
    }
}

scrollToLastChatMsg();

messageInp.addEventListener("input", function(){
    this.style.height = "auto";
    if(this.scrollHeight<=180){
        this.style.height = `${this.scrollHeight}px`;
    }
    else{
        this.style.height = "180px";
    }
});


sendMessageBtn.addEventListener('click', function(){
    let tId = this.dataset.ticketId;
    let messageData = messageInp.value;
    console.log(tId, messageData);
    if(messageData.trim() !== ""){
        messageInp.value = "";
        sendMessageBtn.disabled = true;
        sendMessageToAdd(tId, messageData).then((data)=>{
            location.reload();
        }).catch((err)=>{
            console.log(err);
        }).finally(()=>{
            sendMessageBtn.disabled = false;
        });
        
    }
    else{
        console.log("invalid empty message");
    }
});


async function sendMessageToAdd(ticketId, messageBody){
    try{
        let response = await fetch(
            '/support/add-supmessage/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({'ticketId': ticketId, 'messageBody': messageBody})
            }
        );
        let data = await response.json();
        console.log(data);
        return data;
    }
    catch(err){
        console.log(err);
    }
}