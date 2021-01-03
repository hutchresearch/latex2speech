const input = document.getElementById('upload');
const link = document.getElementById('link');
let objectURL;
var contents = "";

// Function to display download portion of
// new file
function end(file) {
  objectURL = URL.createObjectURL(file);
  link.download = file.name;
  link.href = objectURL;
}

// Function creates new SSML file of contents
function createSSMLFile(file) {
    // Create file
    var ssmlFile = new File(["<speak>\n"  + contents + "</speak>"], file.name + ".ssml", {
      type: "text/plain",
    });
    end(ssmlFile);
}

// Gets contents of file
function getFileContents(file) {
  var reader = new FileReader();

  reader.readAsText(file, "UTF-8");
  reader.onload = function (evt) {
    contents = evt.target.result;
    createSSMLFile(file);
  };
}

// Triggers other functions once .tex file
// has been uploaded
input.addEventListener('change', function () {
  if (objectURL) {
    URL.revokeObjectURL(objectURL);  
  }

  const file = this.files[0];
  var reader = new FileReader();
  getFileContents(file);
});