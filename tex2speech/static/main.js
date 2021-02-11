$( document ).ready(function() {
    $(function() {
        $('#addMoreInput').click(function(){
            console.log("RUN")
            var newDiv = $('<input type="file" id="input" name="inputFile" accept = ".tex"><br>');
          //newDiv.style.background = "#000";
           $('.multipleInputs').append(newDiv);
        });
    });

    $(function() {
        $('#addMoreMain').click(function(){
            console.log("RUN")
            var newDiv = $('<input type="file" id="input" name="inputFile" accept = ".tex"><br>');
          //newDiv.style.background = "#000";
           $('.multipleInputs').append(newDiv);
        });
    });
});

