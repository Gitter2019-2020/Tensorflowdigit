var data;

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            data = reader.result.split(",")[1];
            $("#digit")
                .attr("src", reader.result)
                .width(28)
                .height(28);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function uploadFile(url) {
    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: "text",
        processData: false,
        contentType: false,
        success: function(response) {
            $('#prediction')[0].value = response
        },
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        }
    });
}