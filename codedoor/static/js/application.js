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

// Get the modal
var modalA = document.getElementById('application-modal');

// Get the button that opens the modal
var createAppBtn = document.getElementById("create-application-btn");

// Get the <span> element that closes the modal
// var spanA = document.getElementsByClassName("close")[0];
var spanA = document.getElementById("closeA");

// Get the submit button at the end of the form
var submitBtnA = document.getElementById("submit_button");

// When the user clicks on the button, open the modal 
createAppBtn.onclick = function() {
    modalA.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
spanA.onclick = function() {
	console.log("clicked x");
  	modalA.style.display = "none";
}
// When the user submits the form, close the modal
submitBtnA.onclick = function(event) {
	console.log("clicked submit button");
    modalA.style.display = "none";
}


document.getElementById("submit_button").addEventListener("click", function(e) {
	var position = document.getElementById("position").value;
	var season = document.getElementsByClassName("menu")[0].value;
	var year = document.getElementById("year").value;
	var difficulty = document.getElementById("difficulty").value;
	var description = document.getElementById("description").value;
	var received_offer = document.getElementById("received_offer").checked;
	var offer_details = document.getElementById("offer_details").value;
	var company = document.getElementById("company").value;

	document.getElementById("position").value = "";
	document.getElementById("company").value = "";
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
	formData.append("company", company)

	console.log("hi brian");

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
  var cFields = JSON.parse(a["c"])[0]["fields"];
  var aFields = JSON.parse(a["a"])[0]["fields"];
  var uFields = JSON.parse(a["u"])[0]["fields"];
  var entry = document.getElementById("dummy-application").cloneNode(true);
  entry.getElementsByClassName("application-company-logo")[0].src = cFields["logo"];
  entry.getElementsByClassName("application-link-text")[0].innerHTML = cFields["name"];
  entry.getElementsByClassName("application-applicant-name")[0].innerHTML = uFields["first_name"] + " " + uFields["last_name"];
  entry.getElementsByClassName("job-position")[0].innerHTML = aFields["position"];

  var season = { 1: "Fall", 2: "Winter", 3: "Spring", 4: "Summer" }[aFields.season] + aFields.year;
  entry.getElementsByClassName("job-season")[0].innerHTML = season;

  entry.getElementsByClassName("application-offer-icon")[0].style = aFields["received_offer"] ? "fill:#01959b" : "fill:#ff4d4d";
  entry.getElementsByClassName("application-offer-text")[0].innerHTML = aFields["received_offer"] ? "Received Offer" : "No Offer";

  // evaluating difficulty of interview
  var difficultyIcon = entry.getElementsByClassName("application-difficulty-icon")[0];
  var difficultyText = entry.getElementsByClassName("application-difficulty-text")[0];
  if (aFields["difficult"] > 7) {
    difficultyIcon.style = "fill:#ff4d4d";
    difficultyText.innerHTML = "Difficult Interview: " + aFields["difficult"] + "/10";
  }
  else if (aFields["difficult"] < 4) {
    difficultyIcon.style = "fill:#01959b";
    difficultyText.innerHTML = "Easy Interview: " + aFields["difficult"] + "/10";
  }
  else {
    difficultyIcon.style = "fill:#FF9B71;";
    difficultyText.innerHTML = "Average Interview: " + aFields["difficult"] + "/10";
  }
  entry.getElementsByClassName("application-desc")[0].innerHTML = aFields["description"];
  entry.className = "";
  document.getElementById("application-list").prepend(entry);
}


