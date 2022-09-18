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
            url: 'https://qocbvltca4.execute-api.us-east-1.amazonaws.com/Prod/image2audio',
            type: 'POST',
            // crossDomain: true,
            // dataType: 'json',
            // contentType: 'application/json',
            // headers: {
            //     "Access-Control-Allow-Origin": "*",
            //     "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
            //     "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"

            // },
            body: JSON.stringify(base64),
            success: function (response) {
                if (response != 0) {
                    console.log(response);
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
