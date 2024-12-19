from django import forms
from .models import *

from django import forms
from .models import NhanVien

class NhanVienForm(forms.ModelForm):
    class Meta:
        model = NhanVien
        fields = '__all__'
        widgets = {
            'ma_chuc_vu_nv': forms.Select(attrs={'class': 'form-select'}),
            'ma_phong_ban': forms.Select(attrs={'class': 'form-select'}),
            'ma_hop_dong': forms.Select(attrs={'class': 'form-select'}),
            'ma_chuyen_nganh': forms.Select(attrs={'class': 'form-select'}),
            'ma_trinh_do_hoc_van': forms.Select(attrs={'class': 'form-select'}),
        }

class ChamCongForm(forms.ModelForm):
    class Meta:
        model = ChamCong
        fields = ['nhan_vien', 'ngay_cham_cong', 'gio_vao', 'gio_ra', 'ghi_chu']