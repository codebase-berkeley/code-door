var tabURL = window.location.href.split("/")[6];

if (tabURL.includes("reviews")) {
  console.log("in if")
  showReviews();
} else if (tabURL.includes("applications")) {
  console.log("in else")
  showApplications();
} else {
  console.log("tabURL: " + tabURL);
}

function showReviews() {
    var applicationsTab = document.getElementById("applications_tab");
    var reviewsTab = document.getElementById("reviews_tab");
    var reviewsDropdown = document.getElementById("reviews-dropdown");
    var appsDropdown = document.getElementById("applications-dropdown");
    var createApplicationsBtn = document.getElementById("create-application-btn");
    reviewsTab.classList.remove("nav_item");
    reviewsTab.className += " active_item";
    applicationsTab.classList.remove("active_item");
    reviewsDropdown.style.display = "block";
    appsDropdown.style.display = "none";
    createApplicationsBtn.style.display = "none";
}

function showApplications() {
    var applicationsTab = document.getElementById("applications_tab");
    var reviewsTab = document.getElementById("reviews_tab");
    var reviewsDropdown = document.getElementById("reviews-dropdown");
    var appsDropdown = document.getElementById("applications-dropdown");
    var createApplicationsBtn = document.getElementById("create-application-btn");
    applicationsTab.classList.remove("nav_item");
    applicationsTab.className += " active_item";
    reviewsTab.classList.remove("active_item");
    reviewsDropdown.style.display = "none";
    appsDropdown.style.display = "block";
    createApplicationsBtn.style.display = "inline-block";
}

// window.addEventListener("load", function() {
//     showReviews();
// })