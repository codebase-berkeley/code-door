function validateForm() {
  var position = document.forms["create_app_form"]["position"].value;
  var valid = true; //change to false if it doesn't pass any one of these validations
  if (position == "") {
    event.preventDefault();
    document.getElementById("error0").innerHTML="Enter a valid position";
    valid = false;
  } 
  var description = document.forms["create_app_form"]["description"].value;
  if (description == "") {
    event.preventDefault();
    document.getElementById("error4").innerHTML="Enter a description";
    valid = false;
  } 
  var received_offer = document.forms["create_app_form"]["received_offer"].value;
  if (received_offer != "Yes" && received_offer != "No") {
    event.preventDefault();
    document.getElementById("error5").innerHTML="Select a response";
    valid = false;
  } 
  //providing details about the offer is optional
  else {
    console.log("something is terribly wrong D:");
  }

  if (valid == false) {
    alert("Fix your responses!");
  }
  return valid;
}

// var season = document.forms["create_app_form"]["season"];
// season.addEventListener("select", function (event) {
//   if (season === "--Select--") {
//     season.setCustomValidity("I expect an e-mail, darling!");
//   } else {
//     season.setCustomValidity("");
//   }
// });