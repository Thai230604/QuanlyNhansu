from django.db import models
from django.utils import timezone
from datetime import time

# Phòng Ban
class PhongBan(models.Model):
    ma_phong_ban = models.CharField(max_length=30, primary_key=True)
    ten_phong_ban = models.CharField(max_length=50)
    dia_chi = models.CharField(max_length=50)
    sdt_phong_ban = models.CharField(max_length=11)

    def __str__(self):
        return self.ten_phong_ban

# Chuyên Ngành
class ChuyenNganh(models.Model):
    ma_chuyen_nganh = models.CharField(max_length=30, primary_key=True)
    ten_chuyen_nganh = models.CharField(max_length=50)

    def __str__(self):
        return self.ten_chuyen_nganh

# Nhân Viên
class NhanVien(models.Model):
    GIOI_TINH_CHOICES = [
        (0, 'Nữ'),
        (1, 'Nam'),
    ]

    ma_nhan_vien = models.CharField(max_length=30, primary_key=True)
    mat_khau = models.CharField(max_length=100)
    ho_ten = models.CharField(max_length=50)
    ngay_sinh = models.DateField()
    que_quan = models.CharField(max_length=100)
    hinh_anh = models.ImageField(upload_to='hinh_anh_nhan_vien/', blank=True, null=True)
    gioi_tinh = models.IntegerField(choices=GIOI_TINH_CHOICES)
    dan_toc = models.CharField(max_length=10)
    sdt_nhan_vien = models.CharField(max_length=11)
    ma_chuc_vu_nv = models.ForeignKey('ChucVuNhanVien', on_delete=models.CASCADE)
    trang_thai = models.BooleanField()
    ma_phong_ban = models.ForeignKey(PhongBan, on_delete=models.CASCADE)
    ma_hop_dong = models.ForeignKey('HopDong', on_delete=models.CASCADE)
    ma_chuyen_nganh = models.ForeignKey(ChuyenNganh, on_delete=models.CASCADE)
    ma_trinh_do_hoc_van = models.ForeignKey('TrinhDoHocVan', on_delete=models.CASCADE)
    cmdn = models.CharField(max_length=50)

    def __str__(self):
        return self.ho_ten

    # def save(self, *args, **kwargs):
    #     # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
    #     if not self.pk:
    #         self.mat_khau = make_password(self.mat_khau)
    #     super().save(*args, **kwargs)


# Kỉ Luật
class KyLuat(models.Model):
    ma_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    ly_do = models.TextField()
    tien_ky_luat = models.IntegerField()
    thang_ky_luat = models.DateField()

# Lương
# class Luong(models.Model):
#     nhan_vien  = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
#     luong_thoa_thuan = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Giá trị mặc định là 0.0
#     bao_hiem = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     ngay_tra_luong = models.DateField(default=timezone.now)  # Thêm giá trị mặc định
#     so_gio_lam = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     tien_tang_ca = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     luong_tong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#     def tinh_luong_tong(self):
#         """Tính lương tổng theo công thức."""
#         if self.so_gio_lam and self.luong_thoa_thuan:
#             luong_ngay = self.luong_thoa_thuan / 26 * 8
#             luong_tang_ca = self.tien_tang_ca if self.tien_tang_ca else 0
#             self.luong_tong = luong_ngay * self.so_gio_lam + luong_tang_ca - (self.bao_hiem if self.bao_hiem else 0)
#             self.save()

#     def __str__(self):
#         return f"Lương của {self.nhan_vien.ten} - {self.ngay_tra_luong}"
class Luong(models.Model):
    nhan_vien = models.ForeignKey('NhanVien', on_delete=models.CASCADE)
    luong_co_ban = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hesoluong = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    phu_cap = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thuong = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    khau_tru = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bao_hiem_xa_hoi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bao_hiem_y_te = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bao_hiem_that_nghiep = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thue_thu_nhap_ca_nhan = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tien_tang_ca = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    luong_thuc_nhan = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ngay_tra_luong = models.DateField(default=timezone.now)
    ghi_chu = models.TextField(blank=True, null=True)

    def tinh_luong_thuc_nhan(self):
        tong_thu_nhap = (
            self.luong_co_ban* self.hesoluong +
            self.phu_cap +
            self.thuong +
            self.tien_tang_ca
        )
        tong_khau_tru = (
            self.khau_tru +
            self.bao_hiem_xa_hoi +
            self.bao_hiem_y_te +
            self.bao_hiem_that_nghiep +
            self.thue_thu_nhap_ca_nhan
        )
        self.luong_thuc_nhan = tong_thu_nhap - tong_khau_tru
        self.save()

    def __str__(self):
        return f"Lương của {self.nhan_vien.ho_ten} - {self.ngay_tra_luong}"

    class Meta:
        verbose_name = "Lương"
        verbose_name_plural = "Lương"

class ThoiViec(models.Model):
    ma_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    ly_do = models.TextField()
    ngay_thoi_viec = models.DateField()

# Trình Độ Học Vấn
class TrinhDoHocVan(models.Model):
    ma_trinh_do_hoc_van = models.CharField(max_length=30, primary_key=True)
    ten_trinh_do = models.TextField()
    he_so_bac = models.FloatField()

    def __str__(self):
        return self.ten_trinh_do


class ChucVuNhanVien(models.Model):
    ma_chuc_vu_nv = models.CharField(max_length=30, primary_key=True)
    ten_chuc_vu = models.CharField(max_length=50)
    def __str__(self):
        return self.ten_chuc_vu


class KhenThuong(models.Model):
    ma_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.CASCADE)
    thang_thuong = models.DateField()
    ly_do = models.TextField()
    tien_thuong = models.IntegerField()
    def __str__(self):
        return self.tien_thuong

# Hợp Đồng
class HopDong(models.Model):
    ma_hop_dong = models.CharField(max_length=30, primary_key=True)
    loai_hop_dong = models.CharField(max_length=50)
    ngay_bat_dau = models.DateField()
    ngay_ket_thuc = models.DateField()
    ghi_chu = models.TextField()

    def __str__(self):
        return self.loai_hop_dong



class ChamCong(models.Model):
    nhan_vien = models.ForeignKey('NhanVien', on_delete=models.CASCADE)
    ngay_cham_cong = models.DateField()
    gio_vao = models.TimeField(null=True, blank=True)
    gio_ra = models.TimeField(null=True, blank=True)
    ghi_chu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nhan_vien.ho_ten} - {self.ngay_cham_cong}"

