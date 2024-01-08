import { getRequestOptions } from './cookie_handler.js';

export function getData(endpoint, callback) {
  fetch(endpoint)
    .then(response => response.json())
    .then(data => callback(data));
}

export function sendForm(form, action, endpoint, callback) {
  const formData = new FormData(form);
  console.log(formData)
  const options = getRequestOptions();

  fetch(endpoint, { ...options, method: action, body: formData })
    .then(response => response.json())
    .then(data => callback(data));
}

export function sendFormData(formData, action, endpoint, callback) {
  const options = getRequestOptions();

  fetch(endpoint, { ...options, method: action, body: formData })
    .then(response => response.json())
    .then(data => callback(data));
}