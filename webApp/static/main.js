const input = document.getElementById('uploadFile');
const uploadButton = document.getElementsByClassName('uploadButton');

// Triggers other functions once .tex file
// has been uploaded
input.addEventListener('change', function () {
    if (objectURL) {
      URL.revokeObjectURL(objectURL);  
    }

    // Show upload button
    uploadButton.style.display = "block";

});