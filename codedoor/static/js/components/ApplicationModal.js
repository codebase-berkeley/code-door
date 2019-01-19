/*
ApplicationModal.js

The JavaScript code coupled to an Application Modal component.
To give a modal template submit functionality, create a new ApplicationModal object in JS when the document loads.

@param {Object} formInitialState - The initial state of the form, ie. add in pre-populated fields here.
@param {String} onSubmitPostUrl - The URL that the form data will be submitted to.
@param {String} onSubmitListId - On form submission, a new application entry will be added to the element with this HTML Id.
@param {String} modalId - The HTML ID of the application modal.

Example Usage:

var applicationModal = new ApplicationModal({
    position: "SWE",
    season: "Fall",
    year: "2017",
    difficulty: "10",
    description: "Very hard interview.",
    received_offer: true,
    offer_details: "100k salary",
    company: 456789,
}, "/codedoor/createapplication/", "application-list");

*/

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

var ApplicationModal = function (formInitialState, onSubmitPostUrl, onSubmitListId, modalId) {
    console.log(onSubmitPostUrl);
    var self = this;
    self.modalId = modalId;
    self.formInitialState = formInitialState || {
        position: "",
        season: "",
        year: "",
        difficulty: "",
        description: "",
        received_offer: false,
        offer_details: "",
    };

    self.onSubmitPostUrl = onSubmitPostUrl;
    self.onSubmitListId = onSubmitListId;

    // Get the modal
    self.modalA = document.getElementById(self.modalId);

    // Get the <span> element that closes the modal
    self.spanA = self.modalA.getElementsByClassName("modal-close-btn")[0];
    // Get the submit button at the end of the form
    self.submitBtnA = self.modalA.getElementsByClassName("modal-submit-btn")[0];

    // When the user clicks on <span> (x), close the modal
    self.spanA.addEventListener("click", function() {
        self.modalA.style.display = "none";
    });

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener("click", function(event) {
        if (event.target == self.modalA) {
            self.modalA.style.display = "none";
        }
    });

    self.positionInput = self.modalA.getElementsByClassName("modal-input-position")[0];
    self.seasonInput = self.modalA.getElementsByClassName("modal-input-season")[0];
    self.yearInput = self.modalA.getElementsByClassName("modal-input-year")[0];
    self.difficultyInput = self.modalA.getElementsByClassName("modal-input-difficulty")[0];
    self.descriptionInput = self.modalA.getElementsByClassName("modal-input-description")[0];
    self.offerCheckboxInput = self.modalA.getElementsByClassName("modal-input-offer-check")[0];
    self.offerInput = self.modalA.getElementsByClassName("modal-input-offer")[0];

    self.submitBtnA.addEventListener("click", function(e) {
      if (validate()) {
        e.preventDefault();
        return;
      }
      self.modalA.style.display = "none";
      self.formInitialState.position = self.positionInput.value;
      self.formInitialState.season = self.seasonInput.value;
      self.formInitialState.year = self.yearInput.value;
      self.formInitialState.difficulty = self.difficultyInput.value;
      self.formInitialState.description = self.descriptionInput.value;
      self.formInitialState.received_offer = self.offerCheckboxInput.checked;
      self.formInitialState.offer_details = self.offerInput.value;

      self.positionInput.value = "";
      self.yearInput.value = "";
      self.difficultyInput.value = "";
      self.descriptionInput.value = "";
      self.offerCheckboxInput.value = "";
      self.offerInput.value = "";

      var formData = new FormData();

      formData.append("company", self.formInitialState.company);
      formData.append("position", self.formInitialState.position);
      formData.append("season", self.formInitialState.season);
      formData.append("year", self.formInitialState.year);
      formData.append("difficulty", self.formInitialState.difficulty);
      formData.append("description", self.formInitialState.description);
      formData.append("received_offer", self.formInitialState.received_offer);
      formData.append("offer_details", self.formInitialState.offer_details);

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
        if (self.onSubmitListId !== "") {
          createApplicationElement(json);
        }
      });
    });

    // a is an Application object returned from the server.
    function createApplicationElement(a) {
      console.log(a);
      var cFields = JSON.parse(a["c"])[0]["fields"];
      var aFields = JSON.parse(a["a"])[0]["fields"];
      var uFields = JSON.parse(a["u"])[0]["fields"];
      var entry = document.getElementById("dummy-application").cloneNode(true);
      entry.getElementsByClassName("application-company-logo")[0].src = cFields["logo"];
      entry.getElementsByClassName("application-link-text")[0].innerHTML = cFields["name"];
      entry.getElementsByClassName("application-applicant-name")[0].innerHTML = uFields["first_name"] + " " + uFields["last_name"];
      entry.getElementsByClassName("job-position")[0].innerHTML = aFields["position"];

      var season = `${aFields.season} ${aFields.year}`;
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

    function validate() {
        var positionError = self.modalA.getElementsByClassName('modal-error-position')[0];
        var companyError = self.modalA.getElementsByClassName('modal-error-company')[0];
        var seasonError = self.modalA.getElementsByClassName('modal-error-season')[0];
        var yearError = self.modalA.getElementsByClassName('modal-error-year')[0];
        var difficultyError = self.modalA.getElementsByClassName('modal-error-difficulty')[0];

        var errors_exist = false;

        var position = self.positionInput.value;
        var season = self.seasonInput.value;
        var year = self.yearInput.value;
        var difficulty = self.difficultyInput.value;

        if (!position) {
          errors_exist = true;
          positionError.innerHTML = 'You must provide a position';
        } else {
          positionError.innerHTML = '';
        }
        if (!season) {
          errors_exist = true;
          seasonError.innerHTML = 'You must provide a season';
        } else {
          seasonError.innerHTML = '';
        }
        if (!year) {
          errors_exist = true;
          yearError.innerHTML = 'You must provide a year';
        } else {
          yearError.innerHTML = '';
        }
        if (!difficulty) {
          errors_exist = true;
          difficultyError.innerHTML = 'You must provide a difficulty';
        } else {
          difficultyError.innerHTML = '';
        }
        if (!self.formInitialState.company) {
          errors_exist = true;
          companyError.innerHTML = 'You must provide a company';
        } else {
          companyError.innerHTML = '';
        }
        return errors_exist;
    }
}
