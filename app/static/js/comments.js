import { sendForm } from './request.js';

const createCommentForm = document.getElementById('create-comment');

if (createCommentForm) {
  createCommentForm.addEventListener('submit', evt => {
    evt.preventDefault();

    sendForm(evt.currentTarget, 'POST', '/comments', () => {
      window.location.reload();
    });
  });
}