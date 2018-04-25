

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}


function displayQuestionForm() {
    var x = document.getElementById("myModal");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


function displayEditApplicationForm() {
    var x = document.getElementById("myModal2");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}



// Get the modal
var modal = document.getElementById('myModal');
var modal2 = document.getElementById("myModal2");

// Get the button that opens the modal
var qBtn = document.getElementById("qBtn");
var aBtn = document.getElementById("aBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var span2 = document.getElementsByClassName("close")[1];

// When the user clicks on the button, open the modal 
qBtn.onclick = function() {
    modal.style.display = "block";
}

aBtn.onclick = function() {
  modal2.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

span2.onclick = function() {
  modal2.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
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
  var logo = document.getElementById("logo").value;
  var company = document.getElementById("company").value;
  var profile = document.getElementById("profile").value;
  

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
    var comp;
    if(logo != null) {
      comp = `<td rowspan="3" width="7%">
            <img src="` + logo + `" alt="Company logo" width="100" height="100">
          </td`;
    } else {
      comp = `<td rowspan="3" width="7%">
            <img src="/static/images/temp.png" alt="Company logo" width="100" height="100">
          </td>`;
    }
    var rec;
    if(received_offer) {
      rec = `<span>
                <svg width="15" height="15">
                <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                style="fill:#01959b" />
                </svg> Received Offer
              </span>`;
    } else {
      rec = `<span>
                <svg width="15" height="15">
                <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                style="fill:#ff4d4d" />
                </svg> No Offer
                </span>`;
    }

    var diff;
    if(difficulty > 7) {
      diff = `<span>
                <svg width="15" height="15">
                <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                style="fill:#ff4d4d" />
                </svg>&nbsp;&nbsp;Difficult Interview: ` + difficulty/10 +
              `</span>`;
    } else if(difficulty < 4) {
      diff = `<span>
                <svg width="15" height="15">
                <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                style="fill:#01959b" />
                </svg>&nbsp;&nbsp;Easy Interview: ` + difficulty/10 +
              `</span>`;
    } else {
      diff = `<span>
                <svg width="15" height="15">
                <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                style="fill:#FF9B71;" />
                </svg>&nbsp;&nbsp;Average Interview: ` + difficulty/10 + 
              `</span>`;
    }


    var A = `<tr>` +
        comp +
          `<td rowspan="3" width="7%">
            <img src="/static/images/temp.png" alt="Company logo" width="100" height="100">
          </td>
        <td width="93%">
          <a href="{% url 'codedoor:viewcompany' pk=a.company.pk %}">
            <h2 class="link-text">` + company + `</h2>
          </a>
          <span class="applicant-name">` + profile + `</span>
        </td>
      </tr>
      <tr>
        <td>
          <p><span class="info job-position">`+position+`</span>
          <span class="info job-season">` + season + ` ` + year + `</span></p>
        </td>
      </tr>
      <tr>
        <td>
          <p><span class="info colorful-boxy">`
            + rec +
          `</span>
          <span class="info colorful-boxy">`
            + diff +
          `</span></p>
        </td>
      </tr>
      <tr>
        <td></td>
        <td>
          <h4>Description:</h4>
          <p>` + description +`</p>
        </td>
      </tr>
      <tr>
        <td></td>
        <td>
          <h4>Offer details:</h4>
          <p>` + offer_details + `</p>
        </td>
      </tr>`;

    document.getElementById("app").innerHTML = A;

  })

});
