var apigClient = apigClientFactory.newClient({apiKey: "ATzL6u8N632m4Sr5HRndn4KXwnPKlub31Z9XTbEM"});
var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
var speechRec = new SpeechRecognition()
var fileName = '';
var encoded = null;
var fileObject = null;
var fileExt = null;
function searchimg(){
    var inputtext = document.getElementById("searchInput").value;
    if (inputtext[inputtext.length-1] == "s"){
        var processed_input = inputtext.substr(0, inputtext.length-1)
    }
    else{
        var processed_input = inputtext
    }
    console.log(processed_input)
    var params = {
        "q": processed_input,
    };

    var body = {
      "q": processed_input,
    };
    var additionalParams = {
      // queryParams:{
      //   "q": document.getElementById("searchInput").value,
      // }
    };
    apigClient.searchGet(params, body, additionalParams)
    .then(function(result){
      console.log("search result success");
      displayRes(result.data);
      console.log(result.data)
    }).catch( function(result){
      console.log("search result fail");
    });
}


function voiceSearch(){
    speechRec.start();
    speechRec.onresult = (event) => {
      var text = event.results[0][0].transcript;
      console.log(text)
      document.getElementById("searchInput").value = text
      searchimg();
    }
}

function displayRes(result){
    var generateImg = document.getElementById("imgs");
    console.log(generateImg)
    console.log(result)
    while (generateImg.firstChild) {
        generateImg.removeChild(generateImg.firstChild)
    }
    for (var i = 0; i < result.length; i++){
      console.log(result[i])
      var generateImg = document.getElementById("imgs");
      var newImg = document.createElement("img");
      newImg.style.height = '200px';
      newImg.classList.add();
      newImg.src = result[i];
      generateImg.appendChild(newImg);
    }
}


function uploadimg(){
  var fileReader = new FileReader();
  var fileLocation = (document.getElementById("fileinput").value).split("\\");
  var fileName = fileLocation.at(-1);
  var fileObject = document.getElementById("fileinput").files[0];

  const file = document.getElementById("fileinput").files[0] // your uploaded File object

  file.constructor = () => file;
 
  var imgtypeArr = ["jpeg", "png"]
  if ( (!fileLocation) || (!imgtypeArr.some(type => fileName.includes(type))) ){
    alert("This is not a valid image type. Please try inputing valid images")
  }
  else{
    console.log("valid image")
    var customLabel = document.getElementById("custom_label").value
    if (customLabel[customLabel.length-1] == "s"){
        var customLabelParam = customLabel.substr(0, customLabel.length-1)
    }
    else{
        var customLabelParam = customLabel
    }
    var params = {
      item: fileName,
      folder: "photo-storage-bucket",
      "x-amz-meta-customLabels" : customLabelParam
    }

    var additionalParams = {
      headers: {
        "Access-Control-Allow-Origin" : "*",
        'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Credentials' : true,
        "Content-Type": fileObject.type,
      }
    }
  
    fileReader.onload = function(event){
      eventBody = event.target.result;
      
      body = btoa(eventBody)
      return apigClient.uploadFolderItemPut(params, file, additionalParams)
        .then(function(result){
          console.log(result);
        })
        .catch(function(error){
          console.log(error);
        })
    }
    fileReader.readAsBinaryString(fileObject)
  }
}