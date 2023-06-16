var selectedIssues = [];

function selectElement(element) {
  // Toggle selection on the clicked element
  element.classList.toggle('selected');

  // Check if the element is already selected
  var index = selectedIssues.indexOf(element.textContent);
  if (index > -1) {
    // If selected, remove it from the array
    selectedIssues.splice(index, 1);
  } else {
    // If not selected, add it to the array
    selectedIssues.push(element.textContent);
  }
}

$(document).ready(function () {
  $('.element').click(function () {
    selectElement(this);
    console.log(selectedIssues);
  });
});

function sendIssues() {
  $.ajax({
    url: '/add_issues',
    type: 'POST',
    data: {
      'selected_issues': selectedIssues
    },
    success: function () {
      // Redirect the user to another page on the website
      window.location.href = '/search_series/';
    }
  });
}

