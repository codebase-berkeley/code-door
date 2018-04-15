function displayQuestionForm() {
    var x = document.getElementById("hidden");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}