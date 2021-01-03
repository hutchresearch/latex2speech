const input = document.getElementById('upload');
const link = document.getElementById('link');
let objectURL;

// Function to display download portion of
// new file
function end(file) {
  objectURL = URL.createObjectURL(file);
  link.download = file.name;
  link.href = objectURL;
}

// Triggers other functions once .tex file
// has been uploaded
input.addEventListener('change', function () {
  if (objectURL) {
    URL.revokeObjectURL(objectURL);  
  }

  const file = this.files[0];

  //Call end function here -> Input would be file
});