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
                alert(response.message); // Залишаємо для JSON
                // Якщо сервер повертає HTML, використовуємо DOMParser або простий перехід на сторінку:
                window.location.href = '/success';
            },
            error: function (xhr, status, error) {
                alert('An error occurred. Please try again.');
            }
    });
});