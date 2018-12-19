function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

// Modal relies on a single global object, reviewData.
// Setup the modal and initialize reviewData.
// reviewData is returned as a global variable to allow for an escape hatch for other functions to manipulate it.
// reviewData represents the state of the form and is set and used by the modal form on submission.
var reviewData = (function () {
    var displayReviewForm = function () {
        console.log("displaying review form")
        var x = document.getElementById("reviewmodal");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    };
    var modalR = document.getElementById('reviewmodal');
    // Get the button that opens the modal
    var qBtn = document.getElementById("createreviewbutton");
    // Get the <span> element that closes the modal
    var spanR = document.getElementById("closeR");
    // When the user clicks on the button, open the modal
    qBtn.onclick = function() {
      modalR.style.display = "block";
    }
    // When the user clicks on <span> (x), close the modal
    spanR.onclick = function() {
      modalR.style.display = "none";
    }

    document.getElementById("submit_button_review").addEventListener("click", function(e) {
      var err = validate_review();
      recommendCheckbox = document.getElementsByName("recommend");

      reviewData.reviewTitle = document.getElementById("title1").value;
      reviewData.rating = document.getElementById("rating").value;
      if(recommendCheckbox[0].checked) {
        reviewData.recommend = "True";
      }
      else if(recommendCheckbox[1].checked) {
        reviewData.recommend = "False";
      }
      reviewData.review = document.getElementById("review").value;

      var formData = new FormData();

      formData.append("reviewtitle", reviewData.reviewTitle);
      formData.append("pk", reviewData.pk);
      formData.append("rating", reviewData.rating);
      formData.append("recommend", reviewData.recommend);
      formData.append("review", reviewData.review);

      var headers = new Headers();
      var csrftoken = getCookie("csrftoken")
      headers.append('X-CSRFToken', csrftoken);

      console.log(err);
      if(!err) {
          document.getElementById("title1").value = "";
          document.getElementById("rating").value = "";
          document.getElementsByName("recommend")[0].checked = false;
          document.getElementsByName("recommend")[1].checked = false;
          document.getElementById("review").value = "";
          displayReviewForm();
          fetch("/codedoor/createreview", {
            method: "POST",
            body: formData,
            headers: headers,
            credentials: "include"
          }).then(function(response) {
            return response.json();
          }).then(function(json) {
            if (json.success) {
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
              document.getElementById("reviews").prepend(reviewEl);
            }
          });
        }
    });

    var reviewData = {
      reviewTitle: "",
      rating: 1,
      recommend: "False",
      review: "",
      pk: "0",
    };

    return reviewData;
})();

function validate_review() {
  var err = false;

    var title = document.getElementById('title1').value;
    var rating = document.getElementById('rating').value;
    var yes = document.getElementById('yes').checked;
    var no = document.getElementById('no').checked;
    var review = document.getElementById('review').value;

    var title_error = document.getElementById('title-error');
    var rating_error = document.getElementById('rating-error');
    var review_error = document.getElementById('review-error');
    var recommend_error = document.getElementById('recommend-error');

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
    if (!yes && !no) {
      err = true;
      recommend_error.innerHTML = 'You must provide a recommendation';
      event.preventDefault();
    } else {
      recommend_error.innerHTML = '';
    }
    return err;
}
