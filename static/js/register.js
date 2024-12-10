$('#saveUser').click(function(){
    $.ajax('/add-user', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'username': $('#userName').val(),
            'email':    $('#userEmail').val()
                },

        'success': function(response){
                let usersDiv = document.getElementById('users');                                    //записуємо окрему змінну дів і викликаємо: -->
                usersDiv.innerHTML = `<h3>${$('#userName').val()}</h3>` + usersDiv.innerHTML;
                usersDiv.innerHTML = `<h3>${$('#userEmail').val()}</h3>` + usersDiv.innerHTML;      //він дорівнює новому user і вст назву в середину і додоємо код HTML щоб додався на початок -->                                                                  //він дорівнює новому туру і вст назву в середину і додоємо код HTML щоб додався на початок -->
                $('#userName').val('')                                                              //очистка форми//
                $('#userEmail').val('')
                let userModal = new bootstrap.Modal('#userModal');                                  //викликаємо hide і закриваємо вікно
                userModal.hide();
        }
     })
});
