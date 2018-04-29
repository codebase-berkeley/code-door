
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
    var display_error = document.getElementById('display-error');
    display_error.innerHTML = '';

    if (!title || title.trim().length == 0 || title === 'None') {
      display_error.innerHTML += 'You must provide a title <br>';
      title_error.innerHTML = 'You must provide a title';
      event.preventDefault();
    } else {
      title_error.innerHTML = '';
    }
    if (!rating) {
      display_error.innerHTML += 'You must provide a rating<br>';
      rating_error.innerHTML = 'You must provide a rating';
      event.preventDefault();
    } else {
      rating_error.innerHTML = '';
    }
    if (!review || review.trim().length == 0 || review === 'None') {
      display_error.innerHTML += 'You must provide a review <br>';
      review_error.innerHTML = 'You must provide a review';
      event.preventDefault();
    } else {
      review_error.innerHTML = '';
    }
    if (!yes && !no) {
      display_error.innerHTML += 'You must provide a recommendation <br>';
      recommend_error.innerHTML = 'You must provide a recommendation';
      event.preventDefault();
    } else {
      recommend_error.innerHTML = '';
    }
  });
}
