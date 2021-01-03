const input = document.getElementById('uploadFile');

// Triggers other functions once .tex file
// has been uploaded
input.addEventListener('change', function () {
    if (objectURL) {
      URL.revokeObjectURL(objectURL);  
    }

    // Show upload button

});