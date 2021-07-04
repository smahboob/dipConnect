//PART-4 after creating the html files (10:50)
//add this script to the base file
//PART 5, put a button to show the form on profile update click

$(document).ready(function() {
    console.log("came to main js")
    $('#profile-update-model-btn').click(function() {
        console.log("Clicked button")
        $('.ui.modal')
            .modal('show');
    })
})

//fade messages
// $('#new-post-form').submit(function(e) {
//     console.log("came to post submit")
//     $("#success-message").show();
//     setTimeout(function() { $("#myElem").hide(); }, 5000);
// });