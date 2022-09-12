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
