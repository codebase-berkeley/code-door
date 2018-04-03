function validateForm() {
  var position = document.forms["create_app_form"]["position"].value;
  var valid = true; //change to false if it doesn't pass any of these validations
  if (position == "") {
    event.preventDefault();
    document.getElementById("error0").innerHTML="Enter a valid position";
    document.getElementById("error0").classList.add("error"); //this line doesn't work???
    valid = false;
  } 
  var season = document.forms["create_app_form"]["season"].value;
  if (season == "Select") {
    event.preventDefault();
    document.getElementById("error1").innerHTML="Select a season";
    valid = false;
  } 
  var year = document.forms["create_app_form"]["year"].value;
  if (year == "" || !Number.isInteger(year)) {
    event.preventDefault();
    document.getElementById("error2").innerHTML="Enter a valid year";
    valid = false;
  } 
  var difficulty = document.forms["create_app_form"]["difficulty"].value;
  if (difficulty == "" || !Number.isInteger(difficulty) || difficulty > 10 || difficulty < 1) {
    event.preventDefault();
    document.getElementById("error3").innerHTML="Enter a valid difficulty";
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