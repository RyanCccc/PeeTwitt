$(function() {
    $("#resend").click(function(event) {
        var created_email = $("#created_email").val();
        console.log(created_email);
        $("#resend").attr("disabled", "disabled")
        $.post("/account/resend/", {
            email: created_email
        }, function(data) {
            if (data['success'] == 1) {
                alert('Resend successfully!');
                $("#resend").removeAttr("disabled");
            };
        });
    });
});