$('#saveTour').click(function(){
    $.ajax('/create-tour', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'name': $('#tourName').val(),
            'city': $('#tourCity').val(),
            'days': $('#tourDays').val(),
            'price': $('#tourPrice').val(),
            'date': $('#tourDate').val()
                },

        'success': function(response){
            document.getElementById(`tours`).innerHTML +=
                `
                <div class="card-body">
                    <div class="card-title">
                    </div>
                    <div class="card-text" id="tourCard${response.id}">
                        <ul id="tour${response.id}">
                            <h5>${$('#tourName').val()}</h5>
                            <li>${$('#tourCity').val()}</li>
                            <li>${$('#tourDays').val()}</li>
                            <li>${$('#tourPrice').val()}</li>
                            <li>${$('#tourDate').val()}</li>
                        </ul>
                    </div>
                </div>
                `;
            $('#tourName').val('');
            $('#tourCity').val('');
            $('#tourDays').val('');
            $('#tourPrice').val('');
            $('#tourDate').val('');
        }
    });
});

