$( document ).ready(function() {
    $(function() {
        $('.addMoreInput').click(function(){
            console.log("RUN")
            var newDiv = $('<input type="file" id="input" name="inputFile" accept = ".tex"><br>');
          //newDiv.style.background = "#000";
           $('.multipleInputs').append(newDiv);
        });
    });

    $(function() {
        $('#addMoreMain').click(function(){
            console.log("RUN")
            var newDiv = $('<div class="single"><div class="main"><h5>Main File (.tex)</h5><input type="file" id="myFile" name="filename" accept = ".tex"><br></div><div class="bib"><h5>Bib File (.bib)</h5><input type="file" id="bibFile" name="bibFile" accept = ".bib"><br></div><div class="input"><h5>Additional Input Tex Files (.tex)</h5><div class="multipleInputs"><input type="file" id="input" name="inputFile" accept = ".tex"><br></div><button id = "addMoreInput" class = "addMoreInput" type = "button">&#43;&nbsp;&nbsp;&nbsp;Add Another Input File</button></div></div>');
            //newDiv.style.background = "#000";
           $('.files').append(newDiv);
        });
    });
});

