
function cancelSubscription(subId, csrfToken) {
  const url = `/subscription/update/${subId}/?is_active=false`;
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken,
  };

  fetch(url, {
    method: 'POST',
    headers: headers,
  })
  .then(response => {
    if (response.status === 200) {
      let cancelButton = document.getElementById(`cancelBtn-${subId}`);
      cancelButton.outerHTML = `<button id="activateBtn-${subId}" type="button" class="btn fw-bolder btn-outline-danger"
                      onclick="activateSubscription('${subId}', '${csrfToken}')">Activate</button>`;
      let badgeActive = document.getElementById(`badgeActive-${subId}`);
      badgeActive.outerHTML = `<span id="badgeCancelled-${subId}" class="badge rounded-pill fw-bold bg-danger">Cancelled</span>`;
      let statusDiv = document.getElementById(`statusDiv-${subId}`);
        statusDiv.innerHTML = `<span class="badge rounded-pill" style="color: #00BF63; border: 1px solid #00BF63; background-color: #E5F8EF; margin-left: 5px;">✓ Completed</span>`
    }
  })
  .catch(error => console.error(error));
}

function activateSubscription(subId, csrfToken) {
  const url = `/subscription/update/${subId}/?is_active=true`;
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken,
  };

  fetch(url, {
    method: 'POST',
    headers: headers,
  })
  .then(response => {
    if (response.status === 200) {
      let activateButton = document.getElementById(`activateBtn-${subId}`);
      activateButton.outerHTML = `<button id="cancelBtn-${subId}" type="button" class="btn fw-bolder btn-outline-danger"
                      onclick="cancelSubscription('${subId}', '${csrfToken}')">Cancel</button>`;
      let badgeCancelled = document.getElementById(`badgeCancelled-${subId}`);
      badgeCancelled.outerHTML = `<span id="badgeActive-${subId}" class="badge rounded-pill fw-bold" style="background-color: #00BF63">Active</span>`;
      let statusDiv = document.getElementById(`statusDiv-${subId}`);
        statusDiv.innerHTML = `<span class="badge rounded-pill" style="color: #00BF63; border: 1px solid #00BF63; background-color: #E5F8EF; margin-left: 5px;">✓ Completed</span>`
    }
  })
  .catch(error => console.error(error));
}

function updateSubscription(subId, csrfToken) {
  const timesPerDaySelect = document.getElementById(`timesPerDaySelect-${subId}`);
  if (timesPerDaySelect.value && !Number.isInteger(Number(timesPerDaySelect.value))) {
      let timesPerDaySelect = document.getElementById(`timesPerDaySelect-${subId}`);
      timesPerDaySelect.classList.add("is-invalid");
      let errorDiv = document.createElement("div");
      errorDiv.classList.add("invalid-feedback");
      errorDiv.id = `errorDiv-${subId}`;
      errorDiv.innerHTML = 'Enter numbers only.';
      timesPerDaySelect.parentNode.appendChild(errorDiv);
      return
  }
  const url = `/subscription/update/${subId}/?times_per_day=${timesPerDaySelect.value}`;
  const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken,
  };

  fetch(url, {
  method: 'POST',
  headers: headers,
  })
  .then(response => {
    let errorDiv = document.getElementById(`errorDiv-${subId}`);
    if (errorDiv) {
      errorDiv.remove();
    }

    if (response.status === 200) {
      let timesPerDaySelect = document.getElementById(`timesPerDaySelect-${subId}`);
      let timesPerDayH6 = document.getElementById(`timesPerDay-${subId}`);
      timesPerDayH6.innerHTML = timesPerDaySelect.value;
      timesPerDaySelect.classList.remove("is-invalid");
      timesPerDaySelect.classList.add("is-valid");
      let statusDiv = document.getElementById(`statusDiv-${subId}`);
      statusDiv.innerHTML = `<span class="badge rounded-pill" style="color: #00BF63; border: 1px solid #00BF63; background-color: #E5F8EF; margin-left: 5px;">✓ Completed</span>`
    } else if (response.status === 400) {
      response.json().then(errorObj => {
        let timesPerDaySelect = document.getElementById(`timesPerDaySelect-${subId}`);
        timesPerDaySelect.classList.add("is-invalid");
        let errorDiv = document.createElement("div");
        errorDiv.classList.add("invalid-feedback");
        errorDiv.id = `errorDiv-${subId}`;
        errorDiv.innerHTML = errorObj['times_per_day'];
        timesPerDaySelect.parentNode.appendChild(errorDiv);
      });
    }
  })
  .catch(error => console.error(error));
}


function deleteSubscription(subId) {
  const url = `/subscription/delete/${subId}/`;

  fetch(url, {
    method: 'GET',
  })
  .then(response => {
    if (response.status === 200) {
        let subRow = document.getElementById(`subRow-${subId}`);
        subRow.remove();
        let subModal = document.getElementById(`subModal-${subId}`);
        subModal.remove();
        }
  })
  .catch(error => console.error(error));
}