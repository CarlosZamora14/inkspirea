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

async function sendRequest(url, data, method) {
  const response = await fetch(url, getRequestOptions(data, method));
  if (response.status === 201) {
    window.location.href = '/';
  }
  // const json = await response.json();
  // console.log(json);
}

if (createPostForm) {
  createPostForm.addEventListener('submit', evt => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    sendRequest('/create', formData);
  });
}

if (updatePostForm) {
  updatePostForm.addEventListener('submit', evt => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    sendRequest(window.location.href, formData);
  });
}

document.addEventListener('click', evt => {
  if (evt.target.classList.contains('delete-button')) {
    const button = evt.target;
    sendRequest(`/delete/${button.dataset['postId']}`, null, 'DELETE');
  }
});
