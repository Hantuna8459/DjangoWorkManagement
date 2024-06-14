document.querySelector('form').addEventListener('submit', function(e) {
    var checkbox = document.getElementById('RegisterCheck');
    if (!checkbox.checked) {
        e.preventDefault();
        alert('You must agree to the Terms and Conditions.');
    }
});