/*
ApplicationModal.js

The JavaScript code coupled to an Application Modal component.
To give a modal template submit functionality, create a new ApplicationModal object in JS when the document loads.

@param {Object} formInitialState - The initial state of the form, ie. add in pre-populated fields here.
@param {String} onSubmitPostUrl - The URL that the form data will be submitted to.
@param {String} onSubmitListId - On form submission, a new application entry will be added to the element with this HTML Id.

Example Usage:

var applicationModal = new ApplicationModal({
    position: "SWE",
    season: "Fall",
    year: "2017",
    difficulty: "10",
    description: "Very hard interview.",
    received_offer: true,
    offer_details: "100k salary",
}, "/codedoor/createapplication/456789", "application-list");

*/

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

var ApplicationModal = function (formInitialState, onSubmitPostUrl, onSubmitListId) {
    var self = this;
    self.formInitialState = formInitialState | {
        position: "",
        season: "",
        year: "",
        difficulty: "",
        description: "",
        received_offer: false,
        offer_details: "",
    };
    self.onSubmitPostUrl = onSubmitPostUrl | "/codedoor/createapplication/";
    self.onSubmitListId = onSubmitListId | "application-list";

    // Get the modal
    self.modalA = document.getElementById('application-modal');

    // Get the button that opens the modal
    self.createAppBtn = document.getElementById("create-application-btn");

    // Get the <span> element that closes the modal
    self.spanA = document.getElementById("closeA");

    // Get the submit button at the end of the form
    self.submitBtnA = document.getElementById("submit_button");

    // When the user clicks on the button, open the modal
    self.createAppBtn.addEventListener("click", function() {
        self.modalA.style.display = "block";
    });

    // When the user clicks on <span> (x), close the modal
    self.spanA.addEventListener("click", function() {
        self.modalA.style.display = "none";
    });
    // When the user submits the form, close the modal
    self.submitBtnA.addEventListener("click", function(event) {
      console.log("clicked submit button");
        self.modalA.style.display = "none";
    });

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener("click", function(event) {
        if (event.target == self.modalA) {
            self.modalA.style.display = "none";
        }
    });

    document.getElementById("submit_button").addEventListener("click", function(e) {
      formInitialState.position = document.getElementById("position").value;
      formInitialState.season = document.getElementsByClassName("menu")[0].value;
      formInitialState.year = document.getElementById("year").value;
      formInitialState.difficulty = document.getElementById("difficulty").value;
      formInitialState.description = document.getElementById("description").value;
      formInitialState.received_offer = document.getElementById("received_offer").checked;
      formInitialState.offer_details = document.getElementById("offer_details").value;

      document.getElementById("position").value = "";
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
      var csrftoken = getCookie("csrftoken");
      headers.append('X-CSRFToken', csrftoken);
      fetch(onSubmitPostUrl, {
        method: "POST",
        body: formData,
        headers: headers,
        credentials: "include"
      }).then(function(response) {
        return response.json();
      }).then(function(json) {
        createApplicationElement(json);
      });
    });

    // a is an Application object returned from the server.
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
      document.getElementById(self.onSubmitListId).prepend(entry);
    }

    function displayApplicationForm() {
        var x = document.getElementById("hidden-application");
        if (x.style.display != "block") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }
}
