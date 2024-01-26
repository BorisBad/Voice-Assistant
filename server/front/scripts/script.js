// Expose globally your audio_context, the recorder instance and audio_stream
var audio_context;
var recorder;
var audio_stream;

var is_mic_on;
let mediaRecorder = null;
let chunks = [];
let chunks2 = [];
var requestsList;
var respounceList;
var AudioButton;
var TextButton;
var RequestText;
var ws;//websocket
var asd1
var asd2
var asd3

//#region show/hide interact types
function show(id) 
{
    var element = document.getElementById(id);
    if(element.style.display === 'none')
    {
        element.style.display = 'block';
    }
}

function hide(id)
{
    var element = document.getElementById(id);
    if(element.style.display != 'none')
    {
        element.style.display = 'none';
    }
}

function change_input_type(id)
{
    var btn = document.getElementById(id);
    
    input_types = document.getElementsByClassName('input');
    
    type_id = btn.id.substring(7,btn.id.length);
    for (let i = 0; i < input_types.length; i++) 
    {
        
        //console.log(input_types[i].id);
        if(input_types[i].id != type_id) 
        {
            console.log('hidding ' + input_types[i].id);
            hide(input_types[i].id);
        }
        else
        {
            console.log('showing ' + input_types[i].id);
            show(input_types[i].id);
        }
   }
   return;
}
//#endregion

//#region get voice

function startRecord()
{
    console.log("record audio started");

    navigator.mediaDevices
        .getUserMedia({
          audio: true,
        })
        .then((stream) => {    
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.ondataavailable = (e) => {
            console.log("record audio", e.data);
            //thats raw data
            console.log( e.data.arrayBuffer());
            chunks.push(e.data);
            chunks2.push(e.data.arrayBuffer);
          };
          mediaRecorder.onstop = (e) => {
            console.log("record screen stopped");


            // let blob = new Blob(recordingFile, { type: "audio/ogg" });
            // let file = new File([blob], 'recording.ogg');

            // const data = {
            // "user" : "test",
            // };

            // const formData = new FormData();
            // formData.append('files.file', file);
            // formData.append('data', JSON.stringify(data));
            let blob = new Blob
            (
                chunks, 
                {
                    type: "audio/webm",
                }
            );
            
            //let file2 = new File(chunks.arrayBuffer, "some.webm");
            let file = new File([blob], "some.wav");
            const formData = new FormData();
            formData.append("file.file", file);
            //sendData('audio', new Blob(chunks));
            createMediaElement("audio", "audio/wav", requestsList);
          };
          mediaRecorder.onerror = (e) => {
            console.log(e.error);
          };
          mediaRecorder.start(1000);
        })
        .catch((err) => {
          alert(`The following error occurred: ${err}`);
        });
}

function stopRecord()
{
    mediaRecorder.stop();
}

function audio()
{
    is_mic_on = !is_mic_on;
    if (is_mic_on) 
    {
        AudioButton.textContent = "Stop recorgind";
        startRecord();
    }
    else
    {
        AudioButton.textContent = "Start recorgind";
        stopRecord();
        //sendData('audio', mediaRecorder);
    }
}

function createMediaElement(mediaType, fileType, placeToAdd) 
{
    const blob = new Blob(chunks, {
      type: fileType,
    });
  
    const mediaURL = window.URL.createObjectURL(blob);
    console.log("mediaUrl", mediaURL);
    //blobToUint8Array(mediaURL);
    // asd1 = blobToBinary(blob)
    // .then(console.log)
    // .then(({asd1}) => sendData('audio', asd1));
    const element = document.createElement(mediaType);
    element.setAttribute("controls", "");
    element.src = mediaURL;
    placeToAdd.insertBefore(element, placeToAdd.firstElementChild);
    sendData('audio', new File([blob],'file.wav'));
    mediaRecorder = null;
    chunks = [];
    chunks2 = [];
    
}
//#endregion

//#region get text
function text()
{
    if (RequestText.value === '')
    {
        console.log("request is empty, please type at least something");
        return;
    }
    const newDiv = document.createElement("div");
    const element = document.createTextNode(RequestText.value);
    newDiv.appendChild(element);
    requestsList.insertBefore(newDiv,requestsList.firstElementChild);
    sendData('text', RequestText.value);
    RequestText.value = '';
}
//#endregion

//#region initialize
function Initialize() 
{
    is_mic_on = false;
    requestsList = document.querySelector("#requestsList");
    respounceList = document.querySelector("#respounseList");
    AudioButton = document.querySelector("#voice_btn_start");
    TextButton = document.querySelector("#text_btn_start");
    RequestText = document.getElementById('text');
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) 
    {
        alert("Your browser does not support recording!");
    }
    
    //ws = new WebSocket("ws://localhost:8000/ws", 'echo-protocol');
    //ws = new WebSocket(window.location.href + 'ws', 'echo-protocol');
    AudioButton.addEventListener("click",audio);
    TextButton.addEventListener("click",text);
}

 window.onload = function()
 {
    Initialize();
};

//#endregion


async function sendData(type, data)
{
    console.log(data);
    var response
    switch (type)
    {
        case 'text':
            response = await fetch
            (
                '/'+type ,
                {
                    method:'POST',
                    headers: {"Accept": "application/json", "Content-Type": "application/json" },
                    body: JSON.stringify
                    (
                        {
                            request: data
                        }
                    )
                }   
            );
            break;
        case 'audio':
            let array = await blobToBinary(data);//blov goes here
            //ws.send(data);
            response = await fetch
            (
                '/'+type ,
                {
                    method:'POST',
                    body: JSON.stringify
                    ( 
                        {
                            request: array
                        }
                    )
                }   
            );
            break;
    }

    if(!response.ok)
    {
        console.log(response);
        return;
    }
    const serverRespounce = await response.json();
    const newDiv = document.createElement("div");
    const element = document.createTextNode(serverRespounce.server_respounce);
    newDiv.appendChild(element);
    respounceList.insertBefore(newDiv,respounceList.firstElementChild);
    return;
}

// function blobToUint8Array(uri) {
//      var xhr = new XMLHttpRequest(),
//         i,
//         ui8;
    
//     xhr.open('GET', uri, false);
//     xhr.send();
    
//     URL.revokeObjectURL(uri);
    
//     ui8 = new Uint8Array(xhr.response.length);
    
//     for (i = 0; i < xhr.response.length; ++i) {
//         ui8[i] = xhr.response.charCodeAt(i);
//     }
    
//     return ui8;
// }

const blobToBinary = async (blob) => {
    const buffer = await blob.arrayBuffer();
    
    const view = new Int8Array(buffer);
    
    return [...view].map((n) => n.toString(2)).join(' ');
  };




