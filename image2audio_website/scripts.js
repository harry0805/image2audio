function htmlGet(url) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function upload() {
    file = document.getElementById('fileInput').files[0];
    inverse = document.getElementById('inverse').checked
    edge = document.getElementById('edge').checked

    if (file == undefined){
        $('#messageBox').text('Please select a file!');
        return
    }

    var reader = new FileReader();
    var base64;
    reader.onload = () => {
        base64 = reader.result.replace(/^.+;base64,/, '');
        console.log(base64)
        request = $.ajax({
            url: 'https://qocbvltca4.execute-api.us-east-1.amazonaws.com/Prod/image2audio',
            type: 'POST',
            crossDomain: true,
            dataType: 'json',
            // contentType: 'application/json',
            data: JSON.stringify({'image': base64, 'inverse': +inverse,'edge': +edge}),
            success: function (response) {
                if (response != 0) {
                } else {
                    alert('file not uploaded');
                }
            },

            error: function (e) {
                console.log(e);
            },
        });
    
        // Callback handler that will be called on success
        request.done(function (response, textStatus, jqXHR){
            // Log a message to the console
            console.log(response)
            if ($('#audioPlayer').length){
                $('#audioPlayer').attr('src', response)
            }
            else {
                $('#audioContainer').append('<audio controls src=\"'+ response +'\"></audio>')
            }
            
        });
    
        // Callback handler that will be called on failure
        request.fail(function (jqXHR, textStatus, errorThrown){
            // Log the error to the console
            console.error(
                "The following error occurred: "+
                textStatus, errorThrown
            );
        });
    }
    reader.readAsDataURL(file);
}

function runtest(){
    console.log($('html').length)
}