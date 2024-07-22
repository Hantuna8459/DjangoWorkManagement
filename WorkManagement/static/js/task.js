$(function(){
    // Get form function
    var loadForm = function(){
        let btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type:'get',
            dataType:'json',
            beforeSend: function(){
                $("#task-modal .modal-content").html("");
                $("#task-modal").modal("show");
            },
            success: function(data){
                $("#task-modal .modal-content").html(data.html_form);
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
                    $("#task_table tbody").html(data.html_task_list);
                    $("#task-modal").modal("hide");
                }
                else{
                    $("#task-modal .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    //Binding

    //Create task
    $("#task-table").on("click", "#task-create-button", loadForm);
    $("#task-modal").on("submit", ".task-create-form", saveForm);

    //Update task
    $("#task-table").on("click", "#task-update-button", loadForm);
    $("#task-modal").on("submit", ".task-update-form", saveForm);

    //Delete task
    $("#task-table").on("click", "#task-delete-button", loadForm);
    $("#task-modal").on("submit", ".task-delete-form", saveForm);
});