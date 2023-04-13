let selectedIssues = []
function addData() {
    let data = this.getAttribute('data');
    selectedIssues.push(data)
    console.log(selectedIssues.length)
}

function sendIssues() {
    $.ajax({
        url: '/add_issues',
        type: 'POST',
        data: {
          'selected_issues': selectedIssues
        },
        success: function() {
          // Redirect the user to another page on the website
          window.location.href = '/search_series/';
        }
      });
}

