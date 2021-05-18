// initial state of options
document.getElementById('option_box').style.display = 'none';
document.getElementById('advanced_options_button').textContent = 'Advanced Options \u2BC8'

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
    var optBox = document.getElementById('option_box');
    var optButton = document.getElementById('advanced_options_button')
    if (optBox.style.display === 'none') {
        optBox.style.display = 'block';
        optButton.textContent =  'Advanced Options \u2BC6'
    } else {
        optBox.style.display = 'none';
        optButton.textContent =  'Advanced Options \u2BC8'
    }
}