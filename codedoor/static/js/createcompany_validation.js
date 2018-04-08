function validate() {
  var form = document.getElementsByTagName('form')[0];

  form.addEventListener('submit', function(event) {
    var name = document.getElementById('name').value;
    var industry = document.getElementById('industry').value;
    var website = document.getElementById('website').value;
    var startup = document.getElementById('startup').checked;
    var boutique = document.getElementById('boutique').checked;
    var small = document.getElementById('small').checked;
    var medium = document.getElementById('medium').checked;
    var large = document.getElementById('large').checked;

    var name_error = document.getElementById('name-error');
    var industry_error = document.getElementById('industry-error');
    var website_error = document.getElementById('website-error');
    var type_error = document.getElementById('type-error');
    var display_error = document.getElementById('display-error');
    display_error.innerHTML = '';

    if (!name) {
      display_error.innerHTML += 'You must provide a company name <br>';
      name_error.innerHTML = 'You must provide a company name';
      event.preventDefault();
    } else {
      name_error.innerHTML = '';
    }
    if (!industry) {
      display_error.innerHTML += 'You must provide an industry name <br>';
      industry_error.innerHTML = 'You must provide an industry name';
      event.preventDefault();
    } else {
      industry_error.innerHTML = '';
    }
    if (!website) {
      display_error.innerHTML += 'You must provide a company website <br>';
      website_error.innerHTML = 'You must provide a company website';
      event.preventDefault();
    } else {
      website_error.innerHTML = '';
    }
    if (!startup && !boutique && !small && !medium && !large) {
      display_error.innerHTML += 'You must provide a company type <br>';
      type_error.innerHTML = 'You must provide a company type';
      event.preventDefault();
    } else {
      type_error.innerHTML = '';
    }
  });
}
