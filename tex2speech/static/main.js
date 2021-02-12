$( document ).ready(function() {
    $(function() {
        $('#addMoreInput').click(function(){
            console.log("RUN")
            var newDiv = $('<input type="file" id="input" name="inputFile" accept = ".tex"><br>');
          //newDiv.style.background = "#000";
           $('.multipleInputs').append(newDiv);
        });
    });

    // $(function() {
    //     $('#addMoreMain').click(function(){
    //         console.log("RUN")
    //         var newDiv = $('<div class="single"><div class="main"><h5>Main File (.tex)</h5><input type="file" id="myFile" name="filename" accept = ".tex"><br></div><div class="bib"><h5>Bib File (.bib)</h5><input type="file" id="bibFile" name="bibFile" accept = ".bib"><br></div><div class="input"><h5>Additional Input Tex Files (.tex)</h5><div class="multipleInputs"><input type="file" id="input" name="inputFile" accept = ".tex"><br></div></div></div>');
    //         //newDiv.style.background = "#000";
    //        $('.files').append(newDiv);
    //     });
    // });

    $(function() {
        $('#addMoreMain').click(function(){
            console.log("RUN")
            var newDiv = $('<div class="single"><div class="main"><h5>Main File (.tex)&nbsp;&nbsp;<i class="fa fa-info-circle mainInfo" style="font-size:15px;color:#008080"><span class = "mainToolTip">The main file are files that have \begin document and \end document commands. Can upload a single file here.</span></i></h5><input type="file" id="myFile" name="filename" accept = ".tex"><br></div><div class="bib"><h5>Bib File (.bib)&nbsp;&nbsp;<i class="fa fa-info-circle bibInfo" style="font-size:15px;color:#008080"><span class = "bibToolTip">(Optional upload) You can upload .bib files here that correspond to the main tex file that you have uploaded. Can upload a single file here.</span></i></h5><input type="file" id="bibFile" name="bibFile" accept = ".bib"><br></div><div class="input"><h5>Associated Input Files (.tex)&nbsp;&nbsp;<i class="fa fa-info-circle inputInfo" style="font-size:15px;color:#008080"><span class = "inputToolTip">(Optional upload) You can upload extra input files here. These files correspond to the main tex file you have uploaded and do not have \begin or \end tags. Can upload multiple files here.</span></i></h5><div class="multipleInputs"><input type="file" id="input" name="inputFile" accept = ".tex" multiple><br></div></div></div>');
            //newDiv.style.background = "#000";
           $('.files').append(newDiv);
        });
    });
});

