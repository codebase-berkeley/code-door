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
  var company = document.getElementById("company").value;
  var season = document.getElementById("season").value;
  var year = document.getElementById("year").value;
  var difficulty = document.getElementById("difficulty").value;
  var description = document.getElementById("description").value;
  var receivedOffer = document.getElementById("received_offer").value;
  var offerDetails = document.getElementById("offer_details").value;

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
  formData.append("company", company);
  formData.append("season", season);
  formData.append("year", year);
  formData.append("difficulty", difficulty);
  formData.append("description", description);
  formData.append("received_offer", receivedOffer);
  formData.append("offer_details", offerDetails);

  var headers = new Headers();
  var csrftoken = getCookie("csrftoken")  
  headers.append('X-CSRFToken', csrftoken);
  fetch("/codedoor/createapplication", {
    method: "POST",
    body: JSON.stringify(formData),
    headers: headers,
    credentials: "include"
  }).then(function(response) {
    // console.log(response);
    return response.json();
  }).then(function(json) {
    if ("application" in json) {
      createApplicationElement(json.application);
    }
    else {
      console.log("something is wrong :(")
    }
  })
  });

// var season = document.forms["create_app_form"]["season"];
// season.addEventListener("select", function (event) {
//   if (season === "--Select--") {
//     season.setCustomValidity("I expect an e-mail, darling!");
//   } else {
//     season.setCustomValidity("");
//   }
// });

// a is an Application object
function createApplicationElement(a) {
  var entry = document.getElementById("hidden-table").cloneNode();
  entry.getElementById("position").innerHTML = a.position;
  entry.getElementById("company-name").innerHTML = a.company;
  entry.getElementById("profile-name").innerHTML = a.profile;
  entry.getElementById("season").innerHTML = a.season;
  entry.getElementById("year").innerHTML = a.year;
  if (a.receivedOffer) {
    entry.getElementById("square").style = "fill:#01959b";
    entry.getElementById("offer_text").innerHTML = "Received Offer";
  }
  else { //no offer
    entry.getElementById("square").style = "fill:#ff4d4d";
    entry.getElementById("offer_text").innerHTML = "No Offer";
  } 
  // evaluating difficulty of interview
  if (a.difficult > 7) {
    entry.getElementById("difficulty-square").style = "fill:#ff4d4d";
    entry.getElementById("difficulty-text").innerHTML = "Difficult Interview: " + a.difficult + "/10";
  }
  else if (a.difficult < 4) {
    entry.getElementById("difficulty-square").style = "fill:#01959b";
    entry.getElementById("difficulty-text").innerHTML = "Easy Interview: " + a.difficult + "/10";
  }
  else {
    entry.getElementById("difficuly-square").style = "fill:#FF9B71;";
    entry.getElementById("difficulty-text").innerHTML = "Average Interview: " + a.difficult + "/10";
  }
  entry.getElementById("description").innerHTML = a.description;
}