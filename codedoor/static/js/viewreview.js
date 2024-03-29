function getCookie(name) {
  var value = '; ' + document.cookie;
  var parts = value.split('; ' + name + '=');
  if (parts.length == 2)
    return parts
      .pop()
      .split(';')
      .shift();
}

document.getElementById("cancel").addEventListener("click", function() {
        document.getElementById("addbody").value="";

});

console.log('Do somethings');

document.getElementById('submit').addEventListener('click', function() {
  console.log('In the addEventListener');
  var error = validate_comment();

  if (!error) {
    var title = "";
  var content = document.getElementById('addbody').value;
  document.getElementById("addbody").value="";

  var commentData = new FormData();
  commentData.append('title', title);
  commentData.append('content', content);
  var review = document.getElementById('reviewpk').value;
  commentData.append('review', review);
  var headers = new Headers();

  var csrftoken = getCookie('csrftoken');
  headers.append('X-CSRFToken', csrftoken);
  console.log('CSRFToken', csrftoken);

  fetch('/codedoor/addrc/', {
    method: 'POST',
    body: commentData,
    headers: headers,
    credentials: 'include'
  })
    .then(function(response) {
      return response.json();
    })
    .then(function(json) {
      if (json.success) {
        document.getElementById('comment').innerHTML =
          '<div id="comment"><div id="profile-img" style="background-image: url(' +
          json.profile_url +
          ');">' +
          "</div><p id='commenter'>" +
          json.name +
          '</p>' +
          "<p class='commentcontents'>" +
          json.content +
          '</p><br></div>' +
          document.getElementById('comment').innerHTML;
      }
    });
  }

});


function validate_comment() {
  var content = document.getElementById('addbody').value;
  var display_error = document.getElementById('display-error').value;
  if (!content || content.trim().length == 0 || content === 'None') {
      error_exists = true;
      display_error.innerHTML += 'You must provide a comment';
      event.preventDefault();
  }
}

(function() {
    // Get the buttons that open the edit review
    var editReviewBtn = document.getElementById("edit-review-btn");
    editReviewBtn.addEventListener("click", function() {
        document.getElementById("review-modal").style.display = "block";
    });
})();
