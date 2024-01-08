import { sendForm, sendFormData} from './request.js';

const createPostForm = document.getElementById('create-post');
const updatePostForm = document.getElementById('update-post');

if (createPostForm) {
  createPostForm.addEventListener('submit', async evt => {
    evt.preventDefault();

    sendForm(evt.currentTarget, 'POST', '/create', () => {
      window.location.href = '/';
    });
  });
}

if (updatePostForm) {
  updatePostForm.addEventListener('submit', async evt => {
    evt.preventDefault();

    sendForm(evt.currentTarget, 'POST', window.location.href, () => {
      window.location.href = '/';
    });
  });
}

document.addEventListener('click', async evt => {
  const elem = evt.target;

  if (elem.classList.contains('delete-button')) {
    evt.stopPropagation();
    const postCard = elem.closest('.post-card');
    const postId = postCard.getAttribute('data-post-id');

    sendForm(document.createElement('form'), 'DELETE', `/delete/${postId}`, () => {
      window.location.reload();
    });

  } else if (elem.classList.contains('like-button')) {
    evt.stopPropagation();
    const postCard = elem.closest('.post-card');
    const postId = postCard.getAttribute('data-post-id');

    const formData = new FormData();
    formData.append('post-id', postId)

    sendFormData(formData, 'POST', '/likes', () => {
      window.location.reload();
    });
  }
}, true);

const posts = document.querySelectorAll('.post-card');
posts.forEach(post => {
  post.addEventListener('click', () => {
    window.location.href = `/posts/${post.getAttribute('data-post-id')}`;
  });
});
