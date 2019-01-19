/*
ReviewModal.js

The JavaScript code coupled to an Review Modal component.
To give a modal template submit functionality, create a new ReviewModal object in JS when the document loads.

@param {Object} formInitialState - The initial state of the form, ie. add in pre-populated fields here.
@param {String} onSubmitPostUrl - The URL that the form data will be submitted to.
@param {String} onSubmitListId - On form submission, a new application entry will be added to the element with this HTML Id.
@param {String} modalId - The HTML ID of the review modal.

Example Usage:

var reviewModal = new ReviewModal({
    reviewTitle: "Very bad",
    company: "456789",
    rating: "4",
    recommend: false,
    review: "fucc zucc",
}, "/codedoor/createreview", "reviews", "review-modal");

*/

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

var ReviewModal = function (formInitialState, onSubmitPostUrl, onSubmitListId, modalId) {
    var self = this;
    self.modalId = modalId;
    self.formInitialState = formInitialState || {
      reviewTitle: "",
      rating: 1,
      recommend: "False",
      review: "",
      company: null,
    };
    self.onSubmitPostUrl = onSubmitPostUrl;
    self.onSubmitListId = onSubmitListId;

    self.modalR = document.getElementById(self.modalId);
    // all input elements.
    self.titleInput = self.modalR.getElementsByClassName("modal-input-title")[0];
    self.ratingInput = self.modalR.getElementsByClassName("modal-input-rating")[0];
    self.recommendCheckboxInput = self.modalR.getElementsByClassName("modal-input-recommend-check")[0];
    self.reviewInput = self.modalR.getElementsByClassName("modal-input-review")[0];

    function validate_review() {
        var err = false;

        var title = self.titleInput.value;
        var rating = self.ratingInput.value;
        var review = self.reviewInput.value;

        var title_error = document.getElementsByClassName('modal-title-error')[0];
        var rating_error = document.getElementsByClassName('modal-rating-error')[0];
        var review_error = document.getElementsByClassName('modal-review-error')[0];
        var recommend_error = document.getElementsByClassName('modal-recommend-error')[0];
        var company_error = document.getElementsByClassName("modal-company-error")[0];

        if (!title || title.trim().length == 0 || title === 'None') {
          err = true;
          title_error.innerHTML = 'You must provide a title';
          event.preventDefault();
        } else {
          title_error.innerHTML = '';
        }
        if (!rating || rating > 5 || rating < 0) {
          err = true;
          rating_error.innerHTML = 'You must provide a valid rating';
          event.preventDefault();
        } else {
          rating_error.innerHTML = '';
        }
        if (!review || review.trim().length == 0 || review === 'None') {
          err = true;
          review_error.innerHTML = 'You must provide a review';
          event.preventDefault();
        } else {
          review_error.innerHTML = '';
        }
        console.log(self.formInitialState);
        // company input is handled by external dropdown code.
        if (!self.formInitialState.company) {
          err = true;
          company_error.innerHTML = 'You must select a commpany';
          event.preventDefault();
        } else {
          company_error.innerHTML = '';
        }
        return err;
    }

    var displayReviewForm = function () {
        var x = document.getElementById(self.modalId);
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    };
    // Get the <span> element that closes the modal
    self.spanR = self.modalR.getElementsByClassName("modal-close-btn")[0];
    // When the user clicks on <span> (x), close the modal
    self.spanR.addEventListener("click", function() {
      self.modalR.style.display = "none";
    });

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener("click", function(event) {
        if (event.target == self.modalR) {
            self.modalR.style.display = "none";
        }
    });

    self.modalR.getElementsByClassName("modal-submit-btn")[0].addEventListener("click", function(e) {
      var err = validate_review();

      self.formInitialState.reviewTitle = self.titleInput.value;
      self.formInitialState.rating = self.ratingInput.value;
      if(self.recommendCheckboxInput.checked) {
        self.formInitialState.recommend = "True";
      } else {
        self.formInitialState.recommend = "False";
      }
      self.formInitialState.review = self.reviewInput.value;

      var formData = new FormData();

      formData.append("title", self.formInitialState.reviewTitle);
      formData.append("company", self.formInitialState.company);
      formData.append("rating", self.formInitialState.rating);
      formData.append("recommend", self.formInitialState.recommend);
      formData.append("review", self.formInitialState.review);

      var headers = new Headers();
      var csrftoken = getCookie("csrftoken")
      headers.append('X-CSRFToken', csrftoken);

      console.log(err);
      if(!err) {
          self.titleInput.value = "";
          self.ratingInput.value = "";
          self.recommendCheckboxInput.checked = false;
          self.reviewInput.value = "";
          displayReviewForm();
          fetch(self.onSubmitPostUrl, {
            method: "POST",
            body: formData,
            headers: headers,
            credentials: "include"
          }).then(function(response) {
            return response.json();
          }).then(function(json) {
            console.log(json);
            if (json.success && self.onSubmitListId !== "") {
              // Create a new review element.
              var reviewEl = document.getElementById("dummy-review").cloneNode(true);
              reviewEl.getElementsByClassName("review-company-logo")[0].src = json.companyLogo;
              reviewEl.getElementsByClassName("review-company-link")[0].href = `/codedoor/viewcompany/${json.companypk}/reviews`;
              reviewEl.getElementsByClassName("review-link-text")[0].innerHTML = json.companyname;
              reviewEl.getElementsByClassName("review-applicant-name")[0].innerHTML = json.reviewername;
              reviewEl.getElementsByClassName("review-title")[0].href = "#"; // FIXME to point to review.
              reviewEl.getElementsByClassName("review-title")[0].innerHTML = json.title;
              reviewEl.getElementsByClassName("review-recommend-icon")[0].style = json.recommend ? "fill:#01959b" : "fill:#ff4d4d";
              reviewEl.getElementsByClassName("review-recommend-text")[0].innerHTML = json.recommend ? "Recommends" : "Doesn't recommend";

              var reviewStarsEl = reviewEl.getElementsByClassName("review-stars")[0];
              reviewStarsEl.innerHTML = "";
              for (var i = 0; i < 5; i++) {
                if (i < json.rating) {
                  reviewStarsEl.innerHTML += "<img src='/static/images/blackstar.png' height='20' width='20'>";
                } else {
                  reviewStarsEl.innerHTML += "<img src='/static/images/whitestar.png' height='20' width='20'>";
                }
              }
              reviewEl.getElementsByClassName("review-desc")[0].innerHTML = json.review;

              reviewEl.className = ""; // clear the hidden class from the review element
              document.getElementById(self.onSubmitListId).prepend(reviewEl);
            }
          });
        }
    });
};
