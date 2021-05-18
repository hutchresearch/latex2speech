document.getElementById('option_box').style.display = 'none';

$( document ).ready(function() {
    // Disable button once form has been submitted
    $('#formID').submit(function () {
        button = document.getElementById('submit');
        button.value = 'Processing';
        button.style.backgroundColor = '#B8B8B8';
        button.disabled = 'true';
        document.getElementById('dot-elastic').style.visibility = 'visible';
        document.getElementById('block').style.visibility = 'visible';
    });
});

function toggle_advanced_options() {
    var opt = document.getElementById('option_box');
    if (opt.style.display === 'none') {
        opt.style.display = 'block';
    } else {
        opt.style.display = 'none';
    }
}