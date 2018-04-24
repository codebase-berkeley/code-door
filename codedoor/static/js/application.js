function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

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

function displayApplicationForm() {
    var x = document.getElementById("hidden-application");
    if (x.style.display != "block") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


document.getElementById("submit_button").addEventListener("click", function(e) {
  var position = document.getElementById("position").value;
  var season = document.getElementsByClassName("menu")[0].value;
  var year = document.getElementById("year").value;
  var difficulty = document.getElementById("difficulty").value;
  var description = document.getElementById("difficulty").value;
  var received_offer = document.getElementById("received_offer").checked;
  var offer_details = document.getElementById("offer_details").value;

  document.getElementById("position").value = "";
  document.getElementById("company").value = "";
  document.getElementById("season").value = "";
  document.getElementById("year").value = "";
  document.getElementById("difficulty").value = "";
  document.getElementById("description").value = "";
  document.getElementById("received_offer").value = "";
  document.getElementById("offer_details").value = "";  

  var formData = new FormData();

  formData.append("position", position);
  formData.append("season", season);
  formData.append("year", year);
  formData.append("difficulty", difficulty);
  formData.append("description", description);
  formData.append("received_offer", received_offer);
  formData.append("offer_details", offer_details);

  var headers = new Headers();
  var csrftoken = getCookie("csrftoken")  
  headers.append('X-CSRFToken', csrftoken);
  fetch("/codedoor/createapplication", {
    method: "POST",
    body: formData,
    headers: headers,
    credentials: "include"
  }).then(function(response) {
    return response.json();
  }).then(function(json) {
    createApplicationElement(json);
  })
  });
// a is an Application object
function createApplicationElement(a) {
  var entry = document.getElementById("hidden-element").cloneNode();
  document.getElementById("position").innerHTML = position;
  document.getElementById("company-name").innerHTML = company;
  document.getElementById("season").innerHTML = season;
  document.getElementById("year").innerHTML = year;
  if (received_offer) {
    document.getElementById("square").style = "fill:#01959b";
    document.getElementById("offer_text").innerHTML = "Received Offer";
  }
  else { //no offer
    document.getElementById("square").style = "fill:#ff4d4d";
    document.getElementById("offer_text").innerHTML = "No Offer";
  } 
  // evaluating difficulty of interview
  if (difficulty > 7) {
    document.getElementById("difficulty-square").style = "fill:#ff4d4d";
    document.getElementById("difficulty-text").innerHTML = "Difficult Interview: " + difficulty + "/10";
  }
  else if (difficulty < 4) {
    document.getElementById("difficulty-square").style = "fill:#01959b";
    document.getElementById("difficulty-text").innerHTML = "Easy Interview: " + difficulty + "/10";
  }
  else {
    document.getElementById("difficulty-square").style = "fill:#FF9B71;";
    document.getElementById("difficulty-text").innerHTML = "Average Interview: " + difficulty + "/10";
  }
  document.getElementById("description").innerHTML = description;

  console.log("made it here");
  
  var parent = document.getElementById("application-list");
  parent.insertBefore(entry, document.getElementById("existing-applications"));

  entry.style.display = "block";
}


