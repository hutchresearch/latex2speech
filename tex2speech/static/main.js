// initial state of options
document.getElementById('advanced_options_box').style.display = 'none';
document.getElementById('advanced_options_button').textContent = 'Advanced Options \u2BC8';
updateAdvancedSuboptions();

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
    var optBox = document.getElementById('advanced_options_box');
    var optButton = document.getElementById('advanced_options_button');
    if (optBox.style.display === 'none') {
        optBox.style.display = 'block';
        optButton.textContent =  'Advanced Options \u2BC6';
    } else {
        optBox.style.display = 'none';
        optButton.textContent =  'Advanced Options \u2BC8';
    }
}

function updateAdvancedSuboptions() {
    var mathErrorType = document.getElementById('math_error_type');
    if (mathErrorType.options[mathErrorType.selectedIndex].text == 'Message') {
        document.getElementsByClassName('math_error_text')[0].style.display = 'table-row'
        document.getElementsByClassName('math_error_break')[0].style.display = 'none'
    }
    
    if (mathErrorType.options[mathErrorType.selectedIndex].text == 'Break') {
        document.getElementsByClassName('math_error_text')[0].style.display = 'none'
        document.getElementsByClassName('math_error_break')[0].style.display = 'table-row'
    }

    var boldType = document.getElementById('bold_type');
    if (boldType.options[boldType.selectedIndex].text == 'emphasis') {
        for (let e of document.getElementsByClassName('bold_emphasis')) { e.style.display = 'table-row'}
        for (let e of document.getElementsByClassName('bold_prosody')) { e.style.display = 'none'}
    }
    if (boldType.options[boldType.selectedIndex].text == 'prosody') {
        for (let e of document.getElementsByClassName('bold_emphasis')) { e.style.display = 'none'}
        for (let e of document.getElementsByClassName('bold_prosody')) { e.style.display = 'table-row'}
    }
}