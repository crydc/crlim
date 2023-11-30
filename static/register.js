document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;

    if (username.length < 3 || password.length < 6) {
        alert('用户名至少需要3个字符，密码至少需要6个字符');
        return;
    }

    if (!email.includes('@')) {
        alert('请输入有效的电子邮件地址');
        return;
    }

    // 如果验证通过，可以继续提交表单或执行其他操作
});
