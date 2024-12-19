// static/validation.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        const sdtInput = document.querySelector('input[name="sdt_nhan_vien"]');
        const matKhauInput = document.querySelector('input[name="mat_khau"]');

        // Kiểm tra số điện thoại
        const sdtRegex = /^[0-9]*$/; // Chỉ cho phép số
        if (!sdtRegex.test(sdtInput.value)) {
            alert('Số điện thoại chỉ được phép chứa chữ số.');
            event.preventDefault(); // Ngăn không cho gửi form
            return;
        }

        // Kiểm tra mật khẩu mạnh
        const matKhauRegex = /^(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/; // Ít nhất 8 ký tự và chứa ký tự đặc biệt
        if (matKhauInput.value && !matKhauRegex.test(matKhauInput.value)) {
            alert('Mật khẩu phải có ít nhất 8 ký tự và chứa ít nhất một ký tự đặc biệt.');
            event.preventDefault(); // Ngăn không cho gửi form
            return;
        }
    });
});
