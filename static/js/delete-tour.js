$('.delete-tour-btn').click(function () {
    if (confirm('Are you sure you want to delete this tour?')) {
        const tourId = $(this).data('id');
        $.ajax('/delete-tour', {
            type: 'POST',
            data: { tour_id: tourId },
            success: function (response) {
                alert(response.message);
                location.reload();
            },
            error: function () {
                alert('Failed to delete tour. Please try again.');
            },
        });
    }
});