$(document).ready(function() {
    $('#user-form').on('submit', function(e) {
        e.preventDefault();
        const name = $('#name').val();
        const birthday = $('#birthday').val();
        
        $.ajax({
            url: '/add_user',
            method: 'POST',
            data: {
                name: name,
                birthday: birthday
            },
            success: function(response) {
                if (response.status === 'success') {
                    loadUsers();
                }
            }
        });
    });

    function loadUsers() {
        $.ajax({
            url: '/get_users',
            method: 'GET',
            success: function(response) {
                $('#user-list').empty();
                response.forEach(function(user) {
                    $('#user-list').append(`<li><strong>${user[0]}</strong> - ${user[1]}, Age: ${user[2]}</li>`);
                });
            }
        });
    }

    // Initial load of users
    loadUsers();
});