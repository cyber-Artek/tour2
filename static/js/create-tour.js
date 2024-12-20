$('#saveTour').click(function (e) {
    e.preventDefault(); // Зупиняє стандартну поведінку кнопки

    $.ajax('/create-tour', {
        type: 'POST',
        async: true,
        dataType: 'json',
        data: {
            name: $('#tourName').val(),
            city: $('#tourCity').val(),
            days: $('#tourDays').val(),
            price: $('#tourPrice').val(),
            date: $('#tourDate').val(),
        },
        success: function (response) {
            // Додаємо новий тур у таблицю
            $('#toursTable tbody').append(`
                <tr>
                    <td>${$('#tourName').val()}</td>
                    <td>${$('#tourCity').val()}</td>
                    <td>${$('#tourDays').val()}</td>
                    <td>${$('#tourPrice').val()}</td>
                    <td>${$('#tourDate').val()}</td>
                </tr>
            `);

            // Очищення форми після додавання
            $('#tourName').val('');
            $('#tourCity').val('');
            $('#tourDays').val('');
            $('#tourPrice').val('');
            $('#tourDate').val('');

            alert('Tour created successfully!');
        },
        error: function () {
            alert('Failed to create tour. Please try again.');
        },
    });
});