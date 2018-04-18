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
  var company = document.getElementById("company").value;
  var season = document.getElementById("season").value;
  var year = document.getElementById("year").value;
  var difficulty = document.getElementById("difficulty").value;
  var description = document.getElementById("description").value;
  var receivedOffer = document.getElementById("received_offer").value;
  var offerDetails = document.getElementById("offer_details").value;

  document.getElementById("position").value = "";
  document.getElementById("company").value = "";
  document.getElementById("season").value = "";
  document.getElementById("year").value = "";
  document.getElementById("difficulty").value = "";
  document.getElementById("description").value = "";
  document.getElementById("received_offer").value = "";
  document.getElementById("offer_details").value = "";

  var formData = new FormData();

  formData.append("position", position);
  formData.append("company", company);
  formData.append("season", season);
  formData.append("year", year);
  formData.append("difficulty", difficulty);
  formData.append("description", description);
  formData.append("received_offer", receivedOffer);
  formData.append("offer_details", offerDetails);

  var headers = new Headers();
  var csrftoken = getCookie("csrftoken")  
  headers.append('X-CSRFToken', csrftoken);
  fetch("/codedoor/createapplication", {
    method: "POST",
    body: JSON.stringify(formData),
    headers: headers,
    credentials: "include"
  }).then(function(response) {
    // console.log(response);
    return JSON.parse(response.json());
  }).then(function(json) {
    if (json.success) {
      var A = JSON.stringify(`<table>
          <tr> +
          {% if review.company.logo != null %}
            <td rowspan="3" width="7%">
              <img src="{{a.company.logo}}" width="100" height="100">
            </td>
          {% else %}
            <td rowspan="3" width="7%">
              <img src="/static/images/temp.png" width="100" height="100">
            </td>
          {% endif %}
          <td width="93%">
            <a href="{% url 'codedoor:view_application' pk=a.pk %}">
              <h2 class="link-text">{{ a.company }}</h2>
            </a>
            <span class="applicant-name">{{ a.profile }}</span>
          </td>
        </tr>
        <tr>
          <td>
            <p><span class="info job-position">` + position + `</span>
            <span class="info job-season">` + season + year+ `</span></p>
          </td>
        </tr>
        <tr>
          <td>
            <p><span class="info colorful-boxy">
              {% if ` + received_offer +  ` %}
                <span>
                  <svg width="15" height="15">
                  <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                  style="fill:#01959b" />
                  </svg> Received Offer
                </span>
              {% else %}
                <span>
                  <svg width="15" height="15">
                  <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                  style="fill:#ff4d4d" />
                  </svg> No Offer
                </span>
              {% endif %}
            </span>
            <span class="info colorful-boxy">
              {% if a.difficult > 7 %}
                <span>
                  <svg width="15" height="15">
                  <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                  style="fill:#ff4d4d" />
                  </svg>&nbsp;&nbsp;Difficult Interview: ` + difficulty + `/10
                </span>
              {% elif ` + difficulty + `< 4 %}
                <span>
                  <svg width="15" height="15">
                  <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                  style="fill:#01959b" />
                  </svg>&nbsp;&nbsp;Easy Interview: ` + difficulty + `/10
                </span>
              {% else %}
                <span>
                  <svg width="15" height="15">
                  <rect x="0" y="0" rx="3" ry="3" width="15" height="15"
                  style="fill:#FF9B71;" />
                  </svg>&nbsp;&nbsp;Average Interview: ` + difficulty + `/10
                </span>
              {% endif %}
            </span></p>
          </td>
        </tr>
        <tr>
          <td></td>
          <td>
            <h4>Description:</h4>
            <p class="description_small_text">` + description + `</p>
          </td>
        </tr>
      </table>`);
        document.getElementById("application-list").innerHTML =
        A + document.getElementById("application-list").innerHTML;
    }
  })
  });

// var season = document.forms["create_app_form"]["season"];
// season.addEventListener("select", function (event) {
//   if (season === "--Select--") {
//     season.setCustomValidity("I expect an e-mail, darling!");
//   } else {
//     season.setCustomValidity("");
//   }
// });