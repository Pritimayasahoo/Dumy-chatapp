let tx = document.getElementById("messageInput");
let bt = document.getElementById("sendMessageBtn")
const msg_history = document.querySelector('.msg_history')
const messagesContainer = document.querySelector('.mesgs')
const my_profile_id = document.getElementById("my_profile_id").value
const my_profile = document.getElementById("my_profile").value
const container = document.getElementById("container")
let Otherid = 0;
let ws
let profileImgSrc


messageInput.addEventListener("keypress", function (event) {
    // Check if the Enter key is pressed (key code 13)
    if (event.key === "Enter") {
        // Trigger the click event of the submit button
        bt.click();
    }
})



//Time formating 

// Function to format the time in 12-hour format with AM/PM
function formatTime(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // Handle midnight (0 hours)
    minutes = minutes < 10 ? '0' + minutes : minutes; // Add leading zero to minutes
    return hours + ':' + minutes + ' ' + ampm;
}

// Function to compare dates and determine if it's today, yesterday, or another day
function formatDate(date) {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
        return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
        return 'Yesterday';
    } else {
        // Format date in DD-MM-YYYY format
        const formattedDate = date.getDate() + '-' + (date.getMonth() + 1) + '-' + date.getFullYear();
        return formattedDate;
    }
}


//find out current time
function getCurrentTime() {
    const currentTime = new Date();
    let hours = currentTime.getHours();
    let minutes = currentTime.getMinutes();

    // Convert hours to 12-hour format
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12 || 12; // Convert midnight (0) to 12

    // Add leading zero to single-digit minutes
    minutes = minutes < 10 ? '0' + minutes : minutes;

    // Concatenate hours, minutes, and AM/PM
    const formattedTime = hours + ':' + minutes + ' ' + ampm;

    return formattedTime;
}






//1st dumy connection
ws = new WebSocket('ws://' + '127.0.0.1:8000' + '/ws/ac/' + Otherid + '/')

//Socket connection create
let WebSocketConnection = function () {
    ws = new WebSocket('ws://' + '127.0.0.1:8000' + '/ws/ac/' + Otherid + '/')

    ws.onmessage = function (event) {
        data = JSON.parse(event.data)
        const formattedTime = getCurrentTime()
        tx.focus()
        if (data.otherid == my_profile_id) {

            const messagediv = document.createElement('div');
            const paragraph = document.createElement('p');
            const span = document.createElement('span');
            const incomingdiv = document.createElement('div');
            const received_withd_msg = document.createElement('div');
            const incoming_msg_img = document.createElement('div');
            const imgElement = document.createElement("img");
            imgElement.classList.add('incoming-img')

            imgElement.src = profileImgSrc;

            incoming_msg_img.classList.add('incoming_msg_img')
            incomingdiv.classList.add('incoming_msg');
            messagediv.classList.add('message');
            messagediv.classList.add('received_msg')
            span.classList.add('time_date');
            received_withd_msg.classList.add('received_withd_msg')

            incoming_msg_img.appendChild(imgElement)
            imgElement.classList.add('incoming-img')

            paragraph.textContent = data.msg;
            span.textContent = `${formattedTime}    |    Today`;

            received_withd_msg.appendChild(paragraph)
            received_withd_msg.appendChild(span)


            messagediv.appendChild(received_withd_msg)

            incomingdiv.appendChild(incoming_msg_img)
            incomingdiv.appendChild(messagediv)
            msg_history.appendChild(incomingdiv)

        }

        else {

            const messagediv = document.createElement('div');
            const paragraph = document.createElement('p');
            const span = document.createElement('span');
            const outgoingdiv = document.createElement('div');

            const msg_history = document.querySelector('.msg_history')

            outgoingdiv.classList.add('outgoing_msg');
            messagediv.classList.add('message');
            messagediv.classList.add('sent_msg')
            span.classList.add('time_date');


            paragraph.textContent = data.msg;
            span.textContent = `${formattedTime}    |    Today`;

            messagediv.appendChild(paragraph)
            messagediv.appendChild(span)

            outgoingdiv.appendChild(messagediv)
            msg_history.appendChild(outgoingdiv)
        }

        let isScrolledToBottom = msg_history.scrollHeight - msg_history.clientHeight <= msg_history.scrollTop + 110;
        if (isScrolledToBottom) {
            msg_history.scrollTop = msg_history.scrollHeight;

        }

    }



    ws.onclose = function (event) {
        //re connect
        WebSocketConnection()
    }
}


bt.addEventListener("click", function (event) {
    if (tx.value) {
        message = {
            'my_profile_id': my_profile_id,
            'msg': tx.value,
            'otherid': Otherid
        }
        tx.value = ""
        ws.send(JSON.stringify(message))
    }


})

//Socket close
let Socketdisconnect = function () {
    ws.close()
}

ws.onclose = function (event) {
    //again connect
    WebSocketConnection()
}


// Get all elements with class 'clickable-h1'
const h1Elements = document.querySelectorAll('.clickable-h1');

// Add click event listener to each h1 element
h1Elements.forEach((h1) => {
    h1.addEventListener('click', function () {


        const OtherProfileId = this.id;
        Otherid = OtherProfileId
        profileImgSrc = h1.dataset.profileImg;
        // Clear previous messages
        msg_history.innerHTML = '';

        Socketdisconnect()

        ChatGet(Otherid, profileImgSrc)
        messagesContainer.style.display = "block";
        tx.focus()
    });
});

//User chat retrive
let ChatGet = async function (Otherid, profileImgSrc) {
    let response = await fetch(`messages/?other_id=${Otherid}`)
    let data = await response.json()

    // Append new messages to the messages container
    data.Chats.forEach(chat => {

        // Convert datetime string to a JavaScript Date object
        const dateFromDjango = new Date(chat.fields.sendtime);



        // Format the time
        const formattedTime = formatTime(dateFromDjango);
        // Format the date
        const formattedDate = formatDate(dateFromDjango);
        // Combine time and date
        const finalDateTime = formattedTime + ' | ' + formattedDate;

        if (chat.fields.user == my_profile_id) {

            const messagediv = document.createElement('div');
            const paragraph = document.createElement('p');
            const span = document.createElement('span');
            const outgoingdiv = document.createElement('div');

            outgoingdiv.classList.add('outgoing_msg');
            messagediv.classList.add('message');
            messagediv.classList.add('sent_msg')
            span.classList.add('time_date');

            paragraph.textContent = chat.fields.context;
            span.textContent = finalDateTime;

            messagediv.appendChild(paragraph)
            messagediv.appendChild(span)

            outgoingdiv.appendChild(messagediv)
            msg_history.appendChild(outgoingdiv)

        }

        else {

            const messagediv = document.createElement('div');
            const paragraph = document.createElement('p');
            const span = document.createElement('span');
            const incomingdiv = document.createElement('div');
            const received_withd_msg = document.createElement('div');
            const incoming_msg_img = document.createElement('div');
            const imgElement = document.createElement("img");
            imgElement.classList.add('incoming-img')
            imgElement.src = profileImgSrc;

            incoming_msg_img.classList.add('incoming_msg_img')
            incomingdiv.classList.add('incoming_msg');
            messagediv.classList.add('message');
            messagediv.classList.add('received_msg')
            span.classList.add('time_date');
            received_withd_msg.classList.add('received_withd_msg')

            incoming_msg_img.appendChild(imgElement)
            paragraph.textContent = chat.fields.context;
            span.textContent = finalDateTime;

            received_withd_msg.appendChild(paragraph)
            received_withd_msg.appendChild(span)


            messagediv.appendChild(received_withd_msg)

            incomingdiv.appendChild(incoming_msg_img)
            incomingdiv.appendChild(messagediv)
            msg_history.appendChild(incomingdiv)

        }

        msg_history.scrollTop = msg_history.scrollHeight;

    });



}