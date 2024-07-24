$(function(){
    // Get form function
    var loadForm = function(e){
        e.preventDefault();
        e.stopPropagation();
        let btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type:'get',
            dataType:'json',
            beforeSend: function(){
                $("#workspace-modal .modal-content").html("");
                $("#workspace-modal").modal("show");
            },
            success: function(data){
                $("#workspace-modal .modal-content").html(data.html_form);
            }
        });
    };

    // Save data function
    var saveForm = function(){
        let form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid){
                    $("#workspace_list").html(data.html_workspace_list);
                    $("#workspace-modal").modal("hide");
                }
                else{
                    $("#workspace-modal .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    //Binding

    //Create Workspace
    $("#workspace-create-button").click(loadForm);
    $("#workspace-modal").on("submit", ".workspace-create-form", saveForm);

    //Update Workspace
    $("#workspace-update-button").click(loadForm);
    $("#workspace-modal").on("submit", ".workspace-update-form", saveForm);

    //Delete Workspace
    $("#workspace-edit").on("click","#workspace-update-button",loadForm);
    $("#workspace-modal").on("submit", ".workspace-delete-form", saveForm);
});

// Click on button to show update and delete
$(document).on('click',".reveal-button", function(e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).siblings('.workspace-edit').toggle();
});

// Closing button anywhere
$(document).on('click', function(e) {
    if (!$(e.target).closest('.workspace-edit').length && !$(e.target).is('.reveal-button')) {
        $('.workspace-edit').hide();
    }
});

