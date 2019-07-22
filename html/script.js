var imageId = 0;
var imgArray = [
    "https://jarvis-dailmer.s3.amazonaws.com/Tools1.jpeg",
    "https://jarvis-dailmer.s3.amazonaws.com/Fuel.jpeg",
    "https://images.pexels.com/photos/40799/paper-colorful-color-loose-40799.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
    "https://images.pexels.com/photos/743986/pexels-photo-743986.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
    "video.mp4"
];
var imageUrl = "";

function fetchdata(){
    $.ajax({
        url: 'http://3.85.188.25:8080/current_question',
        type: 'get',
        success: function(response){
            // Perform operation on the return value
            console.log("success");
            updateImage(response);
        },
        error: function(response) {
            console.log("error");
            console.log(response);
            //updateImage(response);
        }
    });
}

function updateImage(response) {
    console.log(response);
    myimg = document.getElementById("myimg");
    myvid = document.getElementById("myvid");
    var newImageUrl = response['img_url'];
    //imageUrl = imgArray[imageId];
    if (!newImageUrl) {
        newImageUrl = "https://jarvis-dailmer.s3.amazonaws.com/truck.jpeg";
    }
    if (newImageUrl != imageUrl ) {
        imageUrl = newImageUrl;
        if (imageUrl.includes('video.mp4')) {
            console.log("video");
            myvid.src = imageUrl;
            myimg.style.display = "none";
            myvid.style.display = "inline";
        } else {
            myimg.src = imageUrl;
            myvid.style.display = "none";
            myimg.style.display = "inline";
        }
    }
    imageId += 1;
    imageId = imageId % 5;
}

$(document).ready(function() {
    setInterval(fetchdata, 2000);
});