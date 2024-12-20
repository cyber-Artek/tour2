$('#buyTourForm').submit(function (e) {
    e.preventDefault();

    const selectedTourId = $('#tourSelect').val();

    $.ajax('/buy-tour', {
        type: 'POST',
        async: true,
        dataType: 'json',
        data: {
            tour_id: selectedTourId
        },
        success: function (response) {
            if (response.status === 'success') {
                alert(response.message);
                // Додатково можна переадресувати користувача на іншу сторінку:
                // window.location.href = '/';
            } else {
                alert(response.message);
            }
        },
        error: function () {
            alert('An error occurred. Please try again.');
        }
    });
});