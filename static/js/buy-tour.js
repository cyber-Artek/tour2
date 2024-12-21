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
                window.location.href = '/'; // Перенаправляємо на головну сторінку
            } else {
                alert(response.message); // Виводимо повідомлення про помилку
            }
        },
        error: function (xhr, status, error) {
            console.error('Error:', xhr.responseText); // Виводимо деталі помилки у консоль
            alert('An error occurred. Please try again.');
        }
    });
});