function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function getRequestOptions(body = null, method = 'POST') {
  const options = {
    method: method,
    credentials: 'same-origin',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
    },
  };

  if (body) {
    options.body = body;
  }

  return options;
};

const createPostForm = document.getElementById('create-post');
const updatePostForm = document.getElementById('update-post');
const createCommentForm = document.getElementById('create-comment');

async function sendRequest(url, data, method) {
  const response = await fetch(url, getRequestOptions(data, method));
  return response;
}

if (createPostForm) {
  createPostForm.addEventListener('submit', async evt => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    const response = await sendRequest('/create', formData);
    if (response.status === 201) {
      window.location.href = '/';
    }
  });
}

if (updatePostForm) {
  updatePostForm.addEventListener('submit', async evt => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    const response = await sendRequest(window.location.href, formData);
    if (response.status === 201) {
      window.location.href = '/';
    }
  });
}

if (createCommentForm) {
  createCommentForm.addEventListener('submit', async evt => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    formData.append('post-id', evt.currentTarget.dataset.postId);
    const response = await sendRequest('/comments', formData);
    if (response.status === 201) {
      window.location.reload();
    }
  });
}

document.addEventListener('click', evt => {
  if (evt.target.classList.contains('delete-button')) {
    evt.stopPropagation();
    const button = evt.target;
    sendRequest(`/delete/${button.parentElement.dataset['postId']}`, null, 'DELETE');
  }
}, true);

const posts = document.querySelectorAll('.post-card');
posts.forEach(post => {
  post.addEventListener('click', evt => {
    window.location.href = `/posts/${post.dataset.postId}`;
  });
});

const hamburgerButton = document.querySelector('.hamburger-button');

if (hamburgerButton) {
  hamburgerButton.addEventListener('click', () => {
    if (hamburgerButton.classList.contains('active')) {
      hamburgerButton.classList.remove('active');
    } else {
      hamburgerButton.classList.add('active');
    }
  });
}