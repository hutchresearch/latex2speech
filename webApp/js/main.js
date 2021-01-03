const input = document.getElementById('upload');
const link = document.getElementById('link');
let objectURL;
var name = "";
var contents = "";

// Initialize the Amazon Cognito credentials provider
AWS.config.region = 'us-east-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-1:3abd773d-8e66-4229-92ff-27f644e942de',
});

var polly = new AWS.Polly();
var s3 = new AWS.S3();

function getOutput(err, data) {
  if (err) console.log(err, err.stack);
  else {
    var file = new File(data.Body, name + ".mp3", {
      type: data.ContentType
    });
    objectURL = URL.createObjectURL(file);
    link.download = file.name;
    link.href = objectURL;
    // TODO: Call s3.deleteObject()
  }
}

// TODO: Don't block main thread like a dingus
function waitForSynthesis(err, data) {
  if (err) console.log(err, err.stack);
  else if (data.SynthesisTask.TaskStatus == "scheduled" || 
           data.SynthesisTask.TaskStatus == "inProgress") {
    var params = {
      TaskId: data.SynthesisTask.TaskId
    }
    polly.getSpeechSynthesisTask(params, waitForSynthesis);
  }
  else if (data.SynthesisTask.TaskStatus == "failed") {
    console.log("speech failed");
    console.log(data.SynthesisTask.TaskStatusReason);
  }
  else { // data.SynthesisTask.TaskStatus == "completed"
    console.log("speech recieved");
    var params = {
      Bucket: "tex2speech-storage",
      Key: data.SynthesisTask.OutputUri
    }
    s3.getObject(params, getOutput);
  }
}

// Function creates new SSML file of contents
function requestSpeechSynthesis() {
  var params = {
    OutputFormat: "mp3",
    OutputS3BucketName: "tex2speech-storage",
    Text: "<speak>\n"  + contents + "\n</speak>",
    VoiceId: "Amy",
    TextType: "ssml"
  }
  console.log("speech requested\n");
  polly.startSpeechSynthesisTask(params, waitForSynthesis);
}

// Gets contents of file
function getFileContents(file) {
  var reader = new FileReader();

  console.log("file got\n");
  reader.readAsText(file, "UTF-8");
  reader.onload = function (evt) {
    name = file.name;
    contents = evt.target.result;
    requestSpeechSynthesis();
  };
}

// Triggers other functions once .tex file
// has been uploaded
input.addEventListener('change', function () {
  if (objectURL) {
    URL.revokeObjectURL(objectURL);  
  }

  const file = this.files[0];
  getFileContents(file);
});
