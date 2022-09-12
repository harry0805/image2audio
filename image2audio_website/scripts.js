// function load(){
//     uploadButton = document.getElementById('uploadButton')
//     uploadButton.type = 'file';
//     uploadButton.id = 'uploadButton';
//     uploadButton.onchange = function() {
//     var file = this.files[0];
//     var reader = new FileReader();
//     reader.onload = function(e) {
//         base64 = e.target.result;
//         var copyButton = document.createElement('button');
//         copyButton.innerHTML = 'Copy';
//         copyButton.onclick = function() {
//         var textArea = document.createElement('textarea');
//         textArea.value = base64;
//         document.body.appendChild(textArea);
//         textArea.select();
//         document.execCommand('copy');
//         document.body.removeChild(textArea);
//         };
//         document.body.appendChild(copyButton);
//     };
//     reader.readAsDataURL(file);
//     };
//     document.body.appendChild(uploadButton);
// }

// button = document.getElementById('button')
// function log(){
//     console.log(base64)
// }

function htmlGet(url) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function upload() {
    file = document.getElementById('fileInput').files[0];
    var reader = new FileReader();
    var base64;
    reader.onload = () => {
        base64 = reader.result.replace(/^.+;base64,/, '');
        console.log(base64)
        // var xml = XMLHttpRequest()
        // $.post('https://qocbvltca4.execute-api.us-east-1.amazonaws.com/Prod/image2audio',
        //     {image: 'abcdefg HELLO'},
        // function(returnedData) {
        //     console.log(returnedData);
        // });

        request = $.ajax({
            url: "https://qocbvltca4.execute-api.us-east-1.amazonaws.com/Prod/image2audio",
            type: "post",
            crossDomain: true,
            // dataType: 'json',
            // contentType: "application/json",
            data: JSON.stringify({image: base64})
        });
    
        // Callback handler that will be called on success
        request.done(function (response, textStatus, jqXHR){
            // Log a message to the console
            console.log("Hooray, it worked!");
            console.log(response)
        });
    
        // Callback handler that will be called on failure
        request.fail(function (jqXHR, textStatus, errorThrown){
            // Log the error to the console
            console.error(
                "The following error occurred: "+
                textStatus, errorThrown
            );
        });
    
        // Callback handler that will be called regardless
        // if the request failed or succeeded
        request.always(function () {
            // Reenable the inputs
            $inputs.prop("disabled", false);
        });
    }
    reader.readAsDataURL(file);
}


// submitButton.onclick = function() {
//   var file = document.getElementById('fileInput').files[0];
//   var reader = new FileReader();
//   reader.onload = function(e) {
//     var dataURL = reader.result;
//     var output = document.getElementById('result');
//     output.innerHTML = dataURL;
//   };
//   reader.readAsDataURL(file);
// };
//