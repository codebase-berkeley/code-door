function validate() {
  var form = document.getElementsByTagName('form')[0];

  form.addEventListener('submit', function(event) {
    var title = document.getElementById('title1').value;
    var rating = document.getElementById('rating').value;
    var yes = document.getElementById('yes').checked;
    var no = document.getElementById('no').checked;
    var review = document.getElementById('review').value;

    var title_error = document.getElementById('title-error');
    var rating_error = document.getElementById('rating-error');
    var review_error = document.getElementById('review-error');
    var recommend_error = document.getElementById('recommend-error');

    if (!title) {
      title_error.innerHTML = 'You must provide a title';
      event.preventDefault();
    } else {
      title_error.innerHTML = '';
    }
    if (!rating) {
      rating_error.innerHTML = 'You must provide a rating';
      event.preventDefault();
    } else {
      rating_error.innerHTML = '';
    }
    if (!review) {
      review_error.innerHTML = 'You must provide a review';
      event.preventDefault();
    } else {
      review_error.innerHTML = '';
    }
    if (!yes && !no) {
      recommend_error.innerHTML = 'You must provide a recommendation';
      event.preventDefault();
    } else {
      recommend_error.innerHTML = '';
    }
  });
}
