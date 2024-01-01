function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function getPostRequestOptions(body) {
  const options = {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
    },
    body: body,
  };

  return options;
};

const createPostForm = document.getElementById('create-post');
const updatePostForm = document.getElementById('update-post');

async function sendPostRequest(data, url) {
  const response = await fetch(url, getPostRequestOptions(data));
  const json = await response.json();
  console.log(json);
}

if (createPostForm) {
  createPostForm.addEventListener('submit', evt => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    sendPostRequest(formData, '/create');
  });
}

if (updatePostForm) {
  updatePostForm.addEventListener('submit', evt => {
    evt.preventDefault();
    const formData = new FormData(evt.currentTarget);
    sendPostRequest(formData, window.location.href);
  });
}
