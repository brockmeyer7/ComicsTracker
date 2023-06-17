var selectedIssues = [];
base_url = "http://127.0.0.1:8000/"

function selectIssue(issue) {
  // Toggle selection on the clicked element
  issue.classList.toggle('selected');

  // Check if the element is already selected
  var index = selectedIssues.indexOf(issue.dataset.issue);
  if (index > -1) {
    // If selected, remove it from the array
    selectedIssues.splice(index, 1);
  } else {
    // If not selected, add it to the array
    selectedIssues.push(issue.dataset.issue);
  }
}

$(document).ready(function () {
  $('.issue').click(function () {
    selectIssue(this);
  });
});

function sendIssues() {
  fetch(base_url + "add_issues", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(selectedIssues)
  })
  .then(response => {
    // Handle the response
    if (response.ok) {
      console.log("POST request successful");
    } else {
      console.log("POST request failed");
    }
  })
  .catch(error => {
    console.log("An error occurred:", error);
  });
}

