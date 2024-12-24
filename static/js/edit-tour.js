$('.edit-tour-btn').click(function () {
    const tourId = $(this).data('id');
    const tourName = $(this).data('name');
    const tourCity = $(this).data('city');
    const tourDays = $(this).data('days');
    const tourPrice = $(this).data('price');
    const tourDate = $(this).data('date');

    // Відображення даних у формі редагування
    $('#editTourId').val(tourId);
    $('#editTourName').val(tourName);
    $('#editTourCity').val(tourCity);
    $('#editTourDays').val(tourDays);
    $('#editTourPrice').val(tourPrice);
    $('#editTourDate').val(tourDate);

    $('#editTourModal').modal('show');
});

$('#saveEditTour').click(function () {
    $.ajax('/edit-tour', {
        type: 'POST',
        data: {
            tour_id: $('#editTourId').val(),
            name: $('#editTourName').val(),
            city: $('#editTourCity').val(),
            days: $('#editTourDays').val(),
            price: $('#editTourPrice').val(),
            date: $('#editTourDate').val(),
        },
        success: function (response) {
            alert(response.message);
            location.reload();
        },
        error: function () {
            alert('Failed to update tour. Please try again.');
        },
    });
});