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

function callbackFunc(response) {
  // do something with the response
  console.log("Made to callback func");
  console.log(response);
}

// Triggers other functions once .tex file
// has been uploaded
input.addEventListener('change', function () {
  if (objectURL) {
    URL.revokeObjectURL(objectURL);  
  }

  const file = this.files[0];

  // $.ajax({
  //   type: "POST",
  //   url: "../scripts/main.py",
  //   data: { param: "Yo iuh iuh" },
  //   success: callbackFunc
  // });

  $.ajax({
    type: "POST",
    url: "../scripts/main.py",
    data: { param: "oioihoiho" }
  }).done(function( o ) {
     // do something
     print("Um??");
  });

  //Call end function here -> Input would be file
});