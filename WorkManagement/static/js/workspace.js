// now move to templates
$(document).ready(function(){
    $('#revealButton').click(function(){
        $('#workspace-create').load('/workspace_create/', function(status, xhr){
            $('#create-form').on('submit', function(e){
                e.preventDefault();
                let formData = $(this).serialize();
                $.ajax({
                    async: true,
                    type: 'POST',
                    url: "{% url 'workspace_create' %}",
                    data: formData,
                    success: function(data){
                        
                    }
                })
            })
            $('#returnButton').click(function() {
                $('#create-form').hide();
                $('#revealButton').show();
            });
        });
    });
});