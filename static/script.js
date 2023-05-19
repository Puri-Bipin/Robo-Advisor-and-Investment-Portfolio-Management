// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Retrieve the preferences form and notification element
  const preferencesForm = document.getElementById('preferencesForm');
  const notification = document.getElementById('notification');

  // Handle form submission
  preferencesForm.addEventListener('submit', function(event) {
    event.preventDefault();

    // Retrieve user preferences from the form
    const riskTolerance = document.getElementById('riskTolerance').value;
    const investmentAmount = document.getElementById('investmentAmount').value;
    const investmentDuration = document.getElementById('investmentDuration').value;

    // Perform any necessary validations
    if (!riskTolerance || !investmentAmount || !investmentDuration) {
      // Display an error message if any field is empty
      notification.innerHTML = 'Please fill in all fields.';
      notification.classList.remove('success');
      notification.classList.add('error');
    } else {
      // Create a new form data object
      const formData = new FormData();
      // Append the user preferences to the form data
      formData.append('riskTolerance', riskTolerance);
      formData.append('investmentAmount', investmentAmount);
      formData.append('investmentDuration', investmentDuration);

      // Send a POST request to the Flask route with the form data
      fetch('/recommendations', {
        method: 'POST',
        body: formData
      })
      .then(response => response.text())
      .then(data => {
        // Display the recommendations page returned by the server
        document.open();
        document.write(data);
        document.close();
      })
      .catch(error => {
        console.error('Error:', error);
        // Display an error message if the request fails
        notification.innerHTML = 'An error occurred. Please try again.';
        notification.classList.remove('success');
        notification.classList.add('error');
      });
    }

    // Reset the form
    preferencesForm.reset();
  });
});
