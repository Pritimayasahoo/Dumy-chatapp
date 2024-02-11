let show=document.getElementById("show");
let tx=document.getElementById("text");
let bt=document.getElementById("Submit")

ws= new WebSocket('ws://127.0.0.1:8000/ws/ac/')
console.log(ws)
 ws.onopen=function(event){
    //console.log('websocket connection opened', event)
    //ws.send('helo server')
   //ws.send('helo')
}
ws.onmessage=function(event){
    console.log(event.data)
    show.insertAdjacentText('afterend',event.data)
    //h2.innerText=event.data
    
}
ws.onerror=function(event){
    console.log(event)
}
bt.addEventListener("click",function(event){
    ws.send(tx.value)
    tx.value=""
})
