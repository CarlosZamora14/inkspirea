import './comments.js';
import './posts.js';

const hamburgerButton = document.querySelector('.hamburger-button');

hamburgerButton.addEventListener('click', function () {
  if (this.classList.contains('active')) {
    this.classList.remove('active');
  } else {
    this.classList.add('active');
  }
});