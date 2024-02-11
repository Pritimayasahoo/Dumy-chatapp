let show=document.getElementById("show");
let tx=document.getElementById("text");
let bt=document.getElementById("Submit")
let owner_id=document.getElementById("owner_id").value
let container=document.getElementById("container")
console.log(owner_id)
let id;
let ws

//1st connection
ws= new WebSocket('ws://127.0.0.1:8000/ws/ac/')

//Socket connection create
let WebSocketConnection=function(){
  ws= new WebSocket('ws://127.0.0.1:8000/ws/ac/')
  console.log('again connect')

  ws.onopen=function(event){
    
  }
  ws.onmessage=function(event){
    console.log(event.data)
    //show.insertAdjacentText('afterend',event.data)
    //h2.innerText=event.data
  }
  ws.onerror=function(event){
    console.log(event)
  }
  ws.onclose=function(event){
    //again connect
    console.log('connect for ever')
    WebSocketConnection()
  }  
}

 
bt.addEventListener("click",function(event){

    message={
      'owner_id':owner_id,
      'msg':tx.value,
      'otherid':id
    }
    ws.send(JSON.stringify(message))
    tx.value=""
})

//Socket close
let Socketdisconnect=function(){
  console.log('close')
  ws.close()
}

ws.onclose=function(event){
  //again connect
  console.log('1st connect')
  WebSocketConnection()
}   

// Get all elements with class 'clickable-h1'
const h1Elements = document.querySelectorAll('.clickable-h1');

// Add click event listener to each h1 element
h1Elements.forEach((h1) => {
  h1.addEventListener('click', function() {
    tx.removeAttribute('hidden')
    bt.removeAttribute('hidden')
    // Extract the id attribute of the clicked h1
    const userId = this.id;
    id=userId
    container.innerText=""
    Socketdisconnect()
    ChatGet(id)
    //console.log('Clicked h1 with id:', userId);

    // Your logic here based on the userId
  });
});

//User chat retrive

let ChatGet=async function(id)
{
  let response=await fetch(`messages/?other_id=${id}`)
  console.log(response)
  let data=await response.json()
  console.log("data type")
  console.log(data,"gooo")
  console.log(data['chats'])
  
}