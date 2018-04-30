function showReviews() {
    var applicationsTab = document.getElementById("applications_tab");
    var reviewsTab = document.getElementById("reviews_tab");
    var createApplicationsBtn = document.getElementById("create-application-btn");
    var a = document.getElementById("applications");
    var r = document.getElementById("reviews");
    reviewsTab.classList.remove("nav_item");
    reviewsTab.className += " active_item";
    applicationsTab.classList.remove("active_item");
    r.style.display = "block";
    a.style.display = "none";
    createApplicationsBtn.style.display = "none";
}

function showApplications() {
    var applicationsTab = document.getElementById("applications_tab");
    var reviewsTab = document.getElementById("reviews_tab");
    var createApplicationsBtn = document.getElementById("create-application-btn");
    var a = document.getElementById("applications");
    var r = document.getElementById("reviews");
    applicationsTab.classList.remove("nav_item");
    applicationsTab.className += " active_item";
    reviewsTab.classList.remove("active_item");
    a.style.display = "block";
    r.style.display = "none";
    createApplicationsBtn.style.display = "inline-block";
}

window.addEventListener("load", function() {
    showReviews();
})