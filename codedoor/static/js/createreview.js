function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}


function displayReviewForm() {
    console.log("displaying review form")
    var x = document.getElementById("hidden");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


document.getElementById("submit_button").addEventListener("click", function(e) {
  var reviewtitle = document.getElementById("title1").value;
  var pk = document.getElementById("reviewcompany").value;
  var rating = document.getElementById("rating").value;
  var recommend = document.getElementsByName("recommend");
  if(recommend[0].checked) {
    recommend = "True";
  }
  else if(recommend[1].checked) {
    recommend = "False";
  }
  var review = document.getElementById("review").value;
  // document.getElementById("question").value = "";
  // document.getElementById("applicant_answer").value = "";
  // document.getElementById("company_answer").value = "";

  var formData = new FormData();

  formData.append("reviewtitle", reviewtitle);
  formData.append("pk", pk);
  formData.append("rating", rating);
  formData.append("recommend", recommend);
  formData.append("review", review);


  var headers = new Headers();
  var csrftoken = getCookie("csrftoken")  
  headers.append('X-CSRFToken', csrftoken);
  fetch("/codedoor/createdreview", {
    method: "POST",
    body: formData,
    headers: headers,
    credentials: "include"
  }).then(function(response) {
    console.log("made it here")
    return response.json();
  }).then(function(json) {
    if (json.success) {
        // document.getElementById("questList").innerHTML =

        // "<div class='post'> <h4 class='blue-text'>Question</h4> <p>" +
        // 	question + 
        // "</p> <h4 class='blue-text'>Applicant answer</h4> <p>" +
        //         	applicant_ans + 
        //         "</p> <h4 class='blue-text'>Company answer</h4><p>" +
        //         	company_ans +
        //         "</p><br><br></div>" + document.getElementById("questList").innerHTML;
        console.log("we made it");
    }
  })
  });

