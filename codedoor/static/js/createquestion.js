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

  console.log(question + applicant_ans + company_ans);
  var formData = new FormData();

  formData.append("question", question);
  formData.append("applicant_answer", applicant_ans);
  formData.append("company_answer", company_ans);

  console.log(formData["question"]);
  fetch("example.com/hello", {
    method: "POST",
    body: formData,
  });
});