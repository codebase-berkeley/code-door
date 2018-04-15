function displayQuestionForm() {
    var x = document.getElementById("hidden");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

console.log(document.getElementById("submit_button"));

document.getElementById("submit_button").addEventListener("click", function(e) {
  var question = document.getElementById("question").value;
  var applicant_ans = document.getElementById("applicant_answer").value;
  var company_ans = document.getElementById("company_answer").value;
  var pk = document.getElementById("pk").value;

  console.log(question + applicant_ans + company_ans + pk);
  var formData = new FormData();

  formData.append("question", question);
  formData.append("applicant_answer", applicant_ans);
  formData.append("company_answer", company_ans);
  formData.append("pk", pk);


  var headers = new Headers();
  // console.log(csrftoken);
  // headers.append('X-CSRFToken', csrftoken);
  fetch(pk, {
    method: "POST",
    body: formData,
    headers: headers,
    credentials: "include"
  }).then(function(response) {
    return response.json();
  }).then(function(json) {
    if (json.success) {
        document.getElementById("questList").innerHTML =

        "<div class='post'> <h4 class='blue-text'>Question</h4> <p>{{ " +
        	question + 
        "}}</p> <h4 class='blue-text'>Applicant answer</h4> <p>{{ " +
                	applicant_ans + 
                "}}</p> <h4 class='blue-text'>Company answer</h4><p>{{ " +
                	company_ans +
                "}}</p><br><br></div>" + document.getElementById("questList").innerHTML;
    }
  })
  });
