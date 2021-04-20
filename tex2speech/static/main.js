$( document ).ready(function() {
    // Disable button once form has been submitted
    $("#formID").submit(function () {
        button = document.getElementById('submit');
        button.value = 'Processing';
        button.style.backgroundColor = '#B8B8B8';
        button.disabled = 'true';
        document.getElementById('dot-elastic').style.visibility = 'visible';
        document.getElementById('block').style.visibility = 'visible';
    });
});