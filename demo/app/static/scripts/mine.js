function get_login_status() {
    $.ajax({
        url: "http://127.0.0.1:5000/api/login_status",
        type: 'GET',
        dataType: 'JSON',
        success: function (data) {
            if (data == null) {
                $('#nav').append('<li><a href="">注册</a></li><li><a href="/login">登录</a></li>')
            }
            else {
                $('#nav').append('<li><span>' + data['name'] + '</span></li><li><a href="/user/center">用户中心</a></li><li><a href="/logout">注销</a></li>')
            }
        }
    })
}