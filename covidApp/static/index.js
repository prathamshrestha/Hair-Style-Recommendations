var video = document.querySelector("#videoElement");
var downloadButton = document.getElementById("downloadButton");
var imageURL="";
var a = document.createElement("a");


function capture() {
    var canvas = document.getElementById('canvas');
    var prev = window.location.href;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
    canvas.toBlob = (blob) => {
        const img = new Image();
        img.src = window.URL.createObjectUrl(blob);
    };
    imageURL = canvas.toDataURL("images/png");
    window.location.href = imageURL.replace("image/png", "image/octet-stream");
    window.location.href = prev;
    console.log("capture clicked");
}

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err0r) {
            console.log("Something went wrong!");
        });
}