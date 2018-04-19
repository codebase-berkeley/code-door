function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}


function displayQuestionForm() {
    var x = document.getElementById("hidden");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


function displayEditApplicationForm() {
    var x = document.getElementById("hidden2");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}



document.getElementById("submit_button").addEventListener("click", function(e) {
  var question = document.getElementById("question").value;
  var applicant_ans = document.getElementById("applicant_answer").value;
  var company_ans = document.getElementById("company_answer").value;
  var pk = document.getElementById("pk").value;

  document.getElementById("question").value = "";
  document.getElementById("applicant_answer").value = "";
  document.getElementById("company_answer").value = "";

  var formData = new FormData();

  formData.append("question", question);
  formData.append("applicant_answer", applicant_ans);
  formData.append("company_answer", company_ans);
  formData.append("pk", pk);


  var headers = new Headers();
  var csrftoken = getCookie("csrftoken")  
  headers.append('X-CSRFToken', csrftoken);
  fetch("/codedoor/createdquestion", {
    method: "POST",
    body: formData,
    headers: headers,
    credentials: "include"
  }).then(function(response) {
    return response.json();
  }).then(function(json) {
    if (json.success) {
        document.getElementById("questList").innerHTML =

        "<div class='post'> <h4 class='blue-text'>Question</h4> <p>" +
        	question + 
        "</p> <h4 class='blue-text'>Applicant answer</h4> <p>" +
                	applicant_ans + 
                "</p> <h4 class='blue-text'>Company answer</h4><p>" +
                	company_ans +
                "</p><br><br></div>" + document.getElementById("questList").innerHTML;
    }
  })
  });



document.getElementById("submit_button_edit").addEventListener("click", function(e) {
  var position = document.getElementById("position").value;
  var season = document.getElementsByClassName("menu")[0].value;
  var year = document.getElementById("year").value;
  var difficulty = document.getElementById("difficulty").value;
  var description = document.getElementById("difficulty").value;
  var received_offer = document.getElementById("received_offer").checked;
  var offer_details = document.getElementById("offer_details").value;
  var pk = document.getElementById("pk").value;
  var a = document.getElementById("a").value;


  var formData = new FormData();

  formData.append("position", position);
  formData.append("season", season);
  formData.append("year", year);
  formData.append("difficulty", difficulty);
  formData.append("description", description);
  formData.append("received_offer", received_offer);
  formData.append("offer_details", offer_details);
  formData.append("pk", pk);


  var headers = new Headers();
  var csrftoken = getCookie("csrftoken")  ;
  headers.append('X-CSRFToken', csrftoken);
  fetch("/codedoor/editapplication", {
    method: "POST",
    body: formData,
    headers: headers,
    credentials: "include"
  }).then(function(response) {
    return response.json();
  }).then(function(json) {
    // if (json.success) {
    //     document.getElementById("app").innerHTML = "{% if a.company.logo != null %} <td rowspan="3" width="7%"><img src=" + 
    //     a.company_logo + "alt='Company logo' width="100" height="100"> </td> {% else %} <td rowspan="3" width="7%">" +
    //         "<img src='/static/images/temp.png' alt='Company logo' width='100' height='100'></td> {% endif %} <td width="93%"> " +
    //       "<a href='{% url 'codedoor:viewcompany' pk=a.company.pk %}'> <h2 class='link-text'>" + 
    //       a.company + "</h2> </a> <span class='applicant-name'>" + 
    //       a.profile +"</span></td>"
    // }
    console.log("success")
  })

});
