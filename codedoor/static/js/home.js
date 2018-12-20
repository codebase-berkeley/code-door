// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    var appModal = document.getElementById('application-modal');
    var reviewModal = document.getElementById('reviewmodal');
    var companyModal = document.getElementById('companyModal');

    if (event.target == appModal) {
        console.log("clicked outside the window");
        appModal.style.display = "none";
    }
    if (event.target == reviewModal) {
        console.log("clicked outside the window");
        reviewModal.style.display = "none";
    }
    if (event.target == companyModal) {
        console.log("clicked outside the window");
        companyModal.style.display = "none";
    }
});

(function() {
    // Get the buttons that open the modals
    var createAppBtn = document.getElementById("create-application-btn");
    var createReviewBtn = document.getElementById("create-review-btn");
    // When the user clicks on the button, open the modal
    createAppBtn.addEventListener("click", function() {
        document.getElementById("application-modal").style.display = "block";
    });
    // When the user clicks on the button, open the modal
    createReviewBtn.addEventListener("click", function() {
        document.getElementById("review-modal").style.display = "block";
    });
})();