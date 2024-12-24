$(document).on('click', '.edit-tour-btn', function() {
    $('#editTourId').val($(this).data('id'));
    $('#editTourName').val($(this).data('name'));
    $('#editTourCity').val($(this).data('city'));
    $('#editTourDays').val($(this).data('days'));
    $('#editTourPrice').val($(this).data('price'));
    $('#editTourDate').val($(this).data('date'));
    $('#editTourModal').modal('show');
});

$('#saveEditTour').on('click', function() {
    const id = $('#editTourId').val();
    const data = {
        tour_id: id,
        name: $('#editTourName').val(),
        city: $('#editTourCity').val(),
        days: $('#editTourDays').val(),
        price: $('#editTourPrice').val(),
        date: $('#editTourDate').val(),
    };
    $.post('/edit-tour', data, function(response) {
        if (response.status === 'success') {
            location.reload();
        } else {
            alert(response.message);
        }
    });
});