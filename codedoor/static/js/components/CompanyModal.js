/*
CompanyModal.js

The JavaScript code coupled to an Company Modal component.
To give a modal template submit functionality, create a new CompanyModal object in JS when the document loads.

@param {Object} formInitialState - The initial state of the form, ie. add in pre-populated fields here.
@param {String} onSubmitPostUrl - The URL that the form data will be submitted to.
@param {String} modalId - The HTML ID of the application modal.

Example Usage:

var companyModal = new CompanyModal({
    logo: null,
    name: "Google",
    industry: "Search",
    website: "google.com",
    structure: "Large",
}, "/codedoor/createcompany", "company-modal");

*/

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

var CompanyModal = function (formInitialState, onSubmitPostUrl, modalId) {
    var self = this;
    self.formInitialState = formInitialState || {
        logo: null,
        name: "",
        industry: "",
        website: "",
        structure: "",
    };
    self.onSubmitPostUrl = onSubmitPostUrl || "/codedoor/createcompany";
    self.modalId = modalId;
    self.modalC = document.getElementById(self.modalId);
    
    self.nameInput = self.modalC.getElementsByClassName('modal-input-name')[0];
    self.industryInput = self.modalC.getElementsByClassName('modal-input-industry')[0];
    self.websiteInput = self.modalC.getElementsByClassName('modal-input-website')[0];
    self.logoInput = self.modalC.getElementsByClassName('modal-input-logo')[0];
    self.structureInput = self.modalC.getElementsByClassName('modal-input-structure')[0];

    // Get the <span> element that closes the modal
    var spanC = self.modalC.getElementsByClassName("modal-close-btn")[0];
        
    // When the user clicks on <span> (x), close the modal
    spanC.addEventListener("click", function() {
      self.modalC.style.display = "none";
    });

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener("click", function(event) {
        if (event.target == self.modalC) {
            self.modalC.style.display = "none";
        }
    });
    
    self.modalC.getElementsByClassName("modal-submit-btn")[0].addEventListener("click", function(e) {
        var errors_exist = validate();
        console.log(errors_exist);
        var logo = self.logoInput.files[0];
        var name = self.nameInput.value;
        var industry = self.industryInput.value;
        var website = self.websiteInput.value;
        var structure = self.structureInput.value;
    
        var formData = new FormData();
    
        formData.append("logo", logo);
        formData.append("name", name);
        formData.append("industry", industry);
        formData.append("website", website);
        formData.append("structure", structure);
    
        var headers = new Headers();
        var csrftoken = getCookie("csrftoken")
        headers.append('X-CSRFToken', csrftoken);

        if(!errors_exist) {
            self.logoInput.value = null;
            self.nameInput.value = "";
            self.industryInput.value = "";
            self.websiteInput.value = "";

            fetch(self.onSubmitPostUrl, {
              method: "POST",
              body: formData,
              headers: headers,
              credentials: "include"
            }).then(function(response) {
              return response.json();
            }).then(function(json) {
              if (json.success) {
                  // redirect to the new company page.
                  window.location.replace('/codedoor/viewcompany/' + json.pk + '/reviews');
              }
            })
        }
    });
    
    function validate() { 
        var name_error = self.modalC.getElementsByClassName('modal-error-name')[0];
        var industry_error = self.modalC.getElementsByClassName('modal-error-industry')[0];
        var website_error = self.modalC.getElementsByClassName('modal-error-website')[0];
        var type_error = self.modalC.getElementsByClassName('modal-error-structure')[0];
        var display_error = self.modalC.getElementsByClassName('modal-error-display')[0];
        
        var drop_downs = document.getElementsByClassName("companies");
        var drop1 = drop_downs[0];
        var drop2 = drop_downs[1];
        
        display_error.innerHTML = '';
        
        var errors_exist = false;

        var logo = self.logoInput.files[0];
        var name = self.nameInput.value;
        var industry = self.industryInput.value;
        var website = self.websiteInput.value;
        var structure = self.structureInput.value;
        
        if (!name || name === 'None' || name.trim().length == 0) {
          errors_exist = true;
          name_error.innerHTML = 'You must provide a company name';
        } else {
          name_error.innerHTML = '';
        }
        if (!industry || industry === 'None' || industry.trim().length == 0) {
          errors_exist = true;
          industry_error.innerHTML = 'You must provide an industry name';
        } else {
          industry_error.innerHTML = '';
        }
        if (!website) {
          errors_exist = true;
          website_error.innerHTML = 'You must provide a company website';
        } else {
          website_error.innerHTML = '';
        }
        return errors_exist;
    }
}