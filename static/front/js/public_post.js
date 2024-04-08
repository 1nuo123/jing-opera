document.getElementById('submit-btn').addEventListener('click', function () {
    var title = "input[name='title']".val();
    var board_id = "select[name='board_id']".val();
    var content = E.getText();
    $.ajax({
        url: "/post/public",
        method: "POST",
        data: { title, board_id, content },
        success: function (result) {
            var code = result['code'];
            if (code == 200) {
                alert("发送成功！");
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