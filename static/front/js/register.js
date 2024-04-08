document.getElementById('captcha-btn').addEventListener('click', function () {
    var email = document.getElementById('email').value;
    $.ajax({
        url: "email/captcha?email=" + email,
        method: "GET",
        success: function (result) {
            var code = result['code'];
            if (code == 200) {
                alert("Email code sent successfully!");
            }
            else {
                alert(result['message']);
            }
        },
        fail: function (error) {
            console.log(error);
        }
    });
});