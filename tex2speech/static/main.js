const form = document.getElementById('formID');
var count= myDropzoneNST.files.length;

$( document ).ready(function() {
    $(function() {
        $('#submit').click(function(){
            button = document.getElementById('submit');
            button.value = 'Processing...';
            button.style.backgroundColor = '#B8B8B8';
            // document.getElementById('blocker').style.visibility = 'visible';
        });
    });
});

