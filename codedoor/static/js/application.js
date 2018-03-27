function validateForm() {
  var position = document.forms["create_app_form"]["position"].value;
  if (position == "") {
    document.getElementById("error0").innerHTML="Enter a valid position";
    document.getElementById("error0").className = "error";
    return false;
  }
}