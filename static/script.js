const checkboxes = document.querySelectorAll(".tick");

checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('click', function(e) {
        // Toggles icon to checked when clicked
        e.target.classList.toggle('fa-regular');
        e.target.classList.toggle('fa-square');
        e.target.classList.toggle('fa-solid');
        e.target.classList.toggle('fa-square-check');

        // Takes the parent node of clicked icon and selects the todo-item that is within the same node
        const parentEl = e.target.closest('.row');
        const todoItem = parentEl.querySelector('.todo-item');

        // Toggles checked class
        if (todoItem) {
            todoItem.classList.toggle('checked');
        }
    });
});

const btnCollapse = document.querySelectorAll(".btnCollapse")

btnCollapse.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
        const icon = btn.querySelector('i');
        icon.classList.toggle('fa-chevron-down');
        icon.classList.toggle('fa-chevron-up');
    });
});

// Reloads the page per interval to display any changes, if any
setInterval(function() {
    // AJAX request
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ someData: 'example' })
    })
    .then(response => {
        // Handle the response from the server
        console.log(response);
        if (response.ok) {
            // Reload the page
            window.location.reload();
        }
    })
    .catch(error => {
        // Handle any errors that occur during the request
        console.error(error);
    });
}, 1800000);
`