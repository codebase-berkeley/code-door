

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function displayReviewForm() {
    console.log("displaying review form")
    var x = document.getElementById("commentmodal");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

document.getElementById("addcomment").addEventListener("click", function(){

document.getElementById("commentmodal").style.display = "block";
console.log("debugged");
});

var modal = document.getElementById('commentmodal');

// Get the button that opens the modal
var qBtn = document.getElementById("addcomment");

// Get the <span> element that closes the modal
// var span2 = document.getElementsByClassName("close")[1];
var span = document.getElementById("close");

// When the user clicks on the button, open the modal
qBtn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}


console.log("Do somethings");

document.getElementById("submit").addEventListener("click", function() {
    console.log("In the addEventListener");


    var title = document.getElementById("addtitle").value;
    var content = document.getElementById("addbody").value;

    var commentData = new FormData();
    commentData.append("title", title);
    commentData.append("content", content);
    var review = document.getElementById("reviewpk").value;
    commentData.append("review", review )
    var headers = new Headers();

    var csrftoken = getCookie("csrftoken")
    headers.append('X-CSRFToken', csrftoken);
    console.log("CSRFToken", csrftoken)

    fetch("/codedoor/addrc/", {
        method: "POST",
        body: commentData,
        headers: headers,
        credentials: "include"
    }).then(function(response) {
        return response.json();
    }).then(function(json) {
        if (json.success) {
            document.getElementById("comment").innerHTML =


            "<div id=\"comment\"><div id=\"profile-img\" style=\"background-image: url(" +json.profile_url+ ");\">"
              +"</div><p id='commenter'>"+json.name+"</p>"
              +"<p class='commentcontents'>"+json.content+"</p><br></div>"
               + document.getElementById("comment").innerHTML;
        }
    })

  document.getElementById("commentmodal").style.display = "none";
  document.getElementById('addtitle').value = ''
  document.getElementById('addbody').value = ''
});
