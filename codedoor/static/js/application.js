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
	console.log(a);
	// console.log(a["c"][0]);
	// console.log("IMPORTANT");
	var cFields = JSON.parse(a["c"])[0]["fields"];
	var aFields = JSON.parse(a["a"])[0]["fields"];
	var uFields = JSON.parse(a["u"])[0]["fields"];
	console.log(cFields);
	console.log(aFields);
	console.log(uFields);
	// console.log(a["c"])
	// a["c"] = JSON.parse(a["c"][0]);
	var entry = document.getElementById("hidden-element").cloneNode(true);
	var parent = document.getElementById("hidden-element");
	// document.getElementById("hidden-logo").src = cFields["logo"];
	// document.getElementById("hidden-company-name").innerHTML = cFields["name"];
	// document.getElementById("hidden-profile-name").innerHTML = uFields["first_name"] + " " + uFields["last_name"];
	// document.getElementById("hidden-position").innerHTML = aFields["position"];
	parent.getElementsByClassName("hidden-logo")[0].src = cFields["logo"];
	parent.getElementsByClassName("hidden-company-name")[0].innerHTML = cFields["name"];
	parent.getElementsByClassName("hidden-profile-name")[0].innerHTML = uFields["first_name"] + " " + uFields["last_name"];
	parent.getElementsByClassName("hidden-position")[0].innerHTML = aFields["position"];

	console.log("LOGO SRC: " + parent.getElementsByClassName("hidden-logo").src);
	console.log("company name class list: " + parent.getElementsByClassName("hidden-company-name").classList);
	console.log("HIDDEN COMPANY NAME: " + parent.getElementsByClassName("hidden-company-name").innerHTML);	

	if (aFields["season"] == 1) {
		console.log("going in here");
		document.getElementById("hidden-season").innerHTML = "Fall";
		parent.getElementsByClassName("hidden-season").innerHTML = "Fall";
	}
	else if (aFields["season"] == 2) {
		document.getElementById("hidden-season").innerHTML = "Winter";
		parent.getElementsByClassName("hidden-season").innerHTML = "Winter";
	}
	else if (aFields["season"] == 3) {
		document.getElementById("hidden-season").innerHTML = "Spring";
		parent.getElementsByClassName("hidden-season").innerHTML = "Spring";
	}
	else {
		document.getElementById("hidden-season").innerHTML = "Summer";
		parent.getElementsByClassName("hidden-season").innerHTML = "Summer";
	}

	console.log("YEAR:")
	console.log(document.getElementById("hidden-year"));
	document.getElementById("hidden-year").innerHTML = aFields["year"];

	if (aFields["received_offer"]) {
		document.getElementById("hidden-square").style = "fill:#01959b";
		document.getElementById("hidden-offer-text").innerHTML = "Received Offer";
	}
	else { //no offer
		document.getElementById("hidden-square").style = "fill:#ff4d4d";
		document.getElementById("hidden-offer-text").innerHTML = "No Offer";
	} 
	// evaluating difficulty of interview
	if (aFields["difficult"] > 7) {
		document.getElementById("hidden-difficulty-square").style = "fill:#ff4d4d";
		document.getElementById("hidden-difficulty-text").innerHTML = "Difficult Interview: " + aFields["difficult"] + "/10";
	}
	else if (aFields["difficult"] < 4) {
		document.getElementById("hidden-difficulty-square").style = "fill:#01959b";
		document.getElementById("hidden-difficulty-text").innerHTML = "Easy Interview: " + aFields["difficult"] + "/10";
	}
	else {
		document.getElementById("hidden-difficulty-square").style = "fill:#FF9B71;";
		document.getElementById("hidden-difficulty-text").innerHTML = "Average Interview: " + aFields["difficult"] + "/10";
	}
	document.getElementById("hidden-description").innerHTML = aFields["description"];

	console.log("made it here");
	
	console.log("hidden element before: " + document.getElementById("hidden-element"));

	document.getElementById("hidden-element").classList.add("display");
	document.getElementById("hidden-element").id = "";
	entry.id = "hidden-element";

	console.log("hidden element after: " + document.getElementById("hidden-element"));
	console.log("entry: " + entry);
	console.log("entry id: " + entry.id);

	console.log("entry: " + entry);

	var p = document.getElementById("application-list");
	p.insertBefore(parent, p.children[0]);
	p.insertBefore(entry, parent);
}


