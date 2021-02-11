$( document ).ready(function() {
    $(function() {
        $('#addMoreUpload').click(function(){
            console.log("RUN")
            var newDiv = $('<input type="file" id="myFile" name="filename" accept = ".tex"><br>');
          //newDiv.style.background = "#000";
           $('.files').append(newDiv);
        });
    });
});

