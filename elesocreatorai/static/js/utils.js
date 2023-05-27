
  function createDocument(url, formData) {
    // send the form data to the server
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
      },
      body: JSON.stringify(formData),
      credentials: 'same-origin', // include cookies in the request
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to save document');
      }
      return response.json();
    })
    .then(data => {
      showAlert("session saved","Document saved successfully")
      //console.log('Document saved:', data);
      return data;
    })
    .catch(error => {
      console.error(error);
      throw error;
    });
  }
  
