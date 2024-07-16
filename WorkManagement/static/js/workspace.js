// $('#reveal-button').onClick(function(){
//     $('#workspace-create-button').show();
//     event.stopPropagation();
// })
function toggleButtons(event) {
    const sideButtons = document.getElementById('workspace-button-update');
    sideButtons.classList.toggle('show');
    event.stopPropagation(); // Prevents the event from bubbling up to parent elements
}