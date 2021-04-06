const form = document.getElementById('formID');

$( document ).ready(function() {
    // Change button messaging
    $(function() {
        $('#submit').click(function(){
            button = document.getElementById('submit');
            button.value = 'Processing...';
            button.style.backgroundColor = '#B8B8B8';
        });
    });

    // Disable button once form has been submitted
    $("#formID").submit(function () {
        document.getElementById('submit').disabled = 'true';
    });
});

