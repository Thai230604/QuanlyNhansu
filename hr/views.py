
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth import logout
from .models import *
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import openpyxl
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from .forms import *
from datetime import time


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect về trang chủ hoặc trang đăng nhập
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Kiểm tra tên đăng nhập và mật khẩu
        try:
            user = NhanVien.objects.get(ma_nhan_vien=username)

            
            password_valid = user.mat_khau == password

            if password_valid:
                
                role = user.ma_chuc_vu_nv.ten_chuc_vu  # Giả sử 'quản lý' cho quản lý và 'nhân viên' cho nhân viên

                
                if role.lower() == 'quản lý':  # Sử dụng .lower() để so sánh không phân biệt hoa thường
                    request.session['user_role'] = 'quản lý'
                    request.session['user_id'] = user.ma_nhan_vien
                    return redirect('home')  # Chuyển hướng đến trang home cho quản lý
                elif role.lower() == 'nhân viên':
                    request.session['user_role'] = 'nhân viên'
                    request.session['user_id'] = user.ma_nhan_vien
                    return redirect('home_nhanvien')  # Chuyển hướng đến trang home cho nhân viên
                else:
                    messages.error(request, "Vai trò của bạn không được hỗ trợ.")
                    return redirect('login')
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")

        except NhanVien.DoesNotExist:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")

    return render(request, 'login.html')  # Trả về trang đăng nhập # Trả về trang đăng nhập


def home_view(request):
    # Kiểm tra nếu người dùng là quản lý
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if user_id and user_role == 'quản lý':
        # Lấy thông tin nhân viên dựa trên user_id
        nhan_vien = get_object_or_404(NhanVien, ma_nhan_vien=user_id)
        return render(request, 'home.html', {'nhan_vien': nhan_vien, 'message': "Chào mừng bạn đến với trang quản lý!"})
    else:
        return redirect('login')


def home_nhanvien_view(request):
    # Kiểm tra nếu người dùng là nhân viên
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if user_id and user_role == 'nhân viên':
        user = get_object_or_404(NhanVien, ma_nhan_vien=user_id)

        # Kiểm tra trạng thái tài khoản nếu cần
        if not user.trang_thai:
            messages.error(request, "Tài khoản của bạn không hoạt động.")
            return redirect('login')  # Chuyển hướng về đăng nhập nếu tài khoản không hoạt động

        if request.method == 'POST':
            # Cập nhật thông tin nhân viên
            user.ho_ten = request.POST.get('ho_ten', user.ho_ten)
            user.ngay_sinh = request.POST.get('ngay_sinh', user.ngay_sinh)
            user.que_quan = request.POST.get('que_quan', user.que_quan)
            user.sdt_nhan_vien = request.POST.get('sdt_nhan_vien', user.sdt_nhan_vien)
            new_password = request.POST.get('mat_khau')
            if new_password:
                user.mat_khau = new_password  # Cập nhật mật khẩu mới

            user.save()  # Lưu thông tin đã cập nhật
            messages.success(request, "Thông tin đã được cập nhật thành công.")
            return redirect('home_nhanvien')  # Chuyển hướng về trang nhân viên

        return render(request, 'home_nhanvien.html', {'user': user})  # Gửi thông tin người dùng lên template
    else:
        return redirect('login')  # Nếu không phải nhân viên, chuyển hướng về đăng nhập


def view_salary_nhanvien(request, ma_nhan_vien):
    nhan_vien = get_object_or_404(NhanVien, ma_nhan_vien=ma_nhan_vien)
    luong_list = Luong.objects.filter(nhan_vien=nhan_vien)

    return render(request, 'view_salary_nhanvien.html', {
        'nhan_vien': nhan_vien,
        'luong_list': luong_list
    })
def update_info_view(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        user = NhanVien.objects.get(ma_nhan_vien=user_id)

        if request.method == 'POST':
            user.ho_ten = request.POST.get('ho_ten', user.ho_ten)
            user.ngay_sinh = request.POST.get('ngay_sinh', user.ngay_sinh)
            user.que_quan = request.POST.get('que_quan', user.que_quan)
            user.sdt_nhan_vien = request.POST.get('sdt_nhan_vien', user.sdt_nhan_vien)
            user.dan_toc = request.POST.get('dan_toc', user.dan_toc)
            user.hinh_anh = request.FILES.get('hinh_anh', user.hinh_anh)

            user.save()
            messages.success(request, "Cập nhật thông tin thành công!")
            return redirect('home_nhanvien')

        return render(request, 'home_nhanvien.html', {'user': user})

    return redirect('login')

def banner(request):
    return render(request, 'banner.html')

def insurance(request):
    return render(request, 'insurance.html')

def contract(request):
    return render(request, 'contract.html')

def leave(request):
    return render(request, 'leave.html')

def reward_punishment(request):
    return render(request, 'reward_punishment.html')

# def deduction(request):
#     phong_ban_list = PhongBan.objects.all()

#     # Xử lý thêm, xóa, sửa, tìm kiếm theo yêu cầu của bạn
#     # Tùy chỉnh theo yêu cầu cụ thể

#     return render(request, 'deduction.html', {'phong_ban_list': phong_ban_list})

def edit_phong_ban(request, ma_phong_ban):
    phong_ban = get_object_or_404(PhongBan, ma_phong_ban=ma_phong_ban)
    if request.method == 'POST':
        phong_ban.ten_phong_ban = request.POST.get('ten_phong_ban')
        phong_ban.dia_chi = request.POST.get('dia_chi')
        phong_ban.sdt_phong_ban = request.POST.get('sdt_phong_ban')
        phong_ban.save()
        return redirect('deduction')
    return render(request, 'edit_phong_ban.html', {'phong_ban': phong_ban})

def delete_phong_ban(request, ma_phong_ban):
    phong_ban = get_object_or_404(PhongBan, ma_phong_ban=ma_phong_ban)
    if request.method == 'POST':  # Xóa chỉ khi xác nhận qua POST
        phong_ban.delete()
        return redirect('deduction')
    return render(request, 'confirm_delete_phong_ban.html', {'phong_ban': phong_ban})

def deduction_view(request):
    if request.method == "POST":
        ma_phong_ban = request.POST.get('ma_phong_ban')
        ten_phong_ban = request.POST.get('ten_phong_ban')
        dia_chi = request.POST.get('dia_chi')
        sdt_phong_ban = request.POST.get('sdt_phong_ban')

        # Tạo đối tượng PhongBan mới và lưu vào cơ sở dữ liệu
        phong_ban = PhongBan(
            ma_phong_ban=ma_phong_ban,
            ten_phong_ban=ten_phong_ban,
            dia_chi=dia_chi,
            sdt_phong_ban=sdt_phong_ban
        )
        phong_ban.save()

        # Chuyển hướng về trang quản lý phòng ban sau khi thêm thành công
        return redirect('deduction')

    phong_ban_list = PhongBan.objects.all()  # Lấy danh sách tất cả phòng ban
    return render(request, 'deduction.html', {'phong_ban_list': phong_ban_list})



def attendance_view(request):
    search_date = request.GET.get('search_date', timezone.now().date())
    
    # Lọc chấm công theo ngày tìm kiếm
    cham_cong = ChamCong.objects.filter(ngay_cham_cong=search_date)

    if request.method == "POST":
        for nhan_vien in NhanVien.objects.all():
            ngay_cham_cong = request.POST.get(f'ngay_cham_cong_{nhan_vien.ma_nhan_vien}')
            gio_vao = request.POST.get(f'gio_vao_{nhan_vien.ma_nhan_vien}')
            gio_ra = request.POST.get(f'gio_ra_{nhan_vien.ma_nhan_vien}')
            ghi_chu = request.POST.get(f'ghi_chu_{nhan_vien.ma_nhan_vien}')

            if ngay_cham_cong:  # Kiểm tra nếu có ngày chấm công
                # Kiểm tra xem có bản ghi nào của nhân viên cho ngày này chưa
                existing_records = ChamCong.objects.filter(
                    nhan_vien=nhan_vien,
                    ngay_cham_cong=ngay_cham_cong
                )

                if existing_records.exists():
                    # Nếu có, cập nhật bản ghi đầu tiên
                    cham_cong_instance = existing_records.first()
                    cham_cong_instance.gio_vao = gio_vao
                    cham_cong_instance.gio_ra = gio_ra
                    cham_cong_instance.ghi_chu = ghi_chu
                    cham_cong_instance.save()
                else:
                    # Nếu không có, tạo mới
                    ChamCong.objects.create(
                        nhan_vien=nhan_vien,
                        ngay_cham_cong=ngay_cham_cong,
                        gio_vao=gio_vao,
                        gio_ra=gio_ra,
                        ghi_chu=ghi_chu
                    )
        
        return redirect('attendance')  # Chuyển hướng để tránh gửi lại form

    employees = NhanVien.objects.all()
    context = {
        'cham_cong': cham_cong,
        'employees': employees,
        'search_date': search_date
    }
    return render(request, 'attendance.html', context)

def salary_view(request):
    search_query = request.GET.get('ma_nhan_vien', '')
    
    if search_query:
        employees = NhanVien.objects.filter(ma_nhan_vien__icontains=search_query)
    else:
        employees = NhanVien.objects.all()

    return render(request, 'salary.html', {'employees': employees})
def view_salary_view(request, ma_nhan_vien):
    nhan_vien = get_object_or_404(NhanVien, ma_nhan_vien=ma_nhan_vien)
    luong_list = Luong.objects.filter(nhan_vien=nhan_vien)

    return render(request, 'view_salary.html', {
        'nhan_vien': nhan_vien,
        'luong_list': luong_list
    })
def enter_salary_view(request, ma_nhan_vien):
    nhan_vien = get_object_or_404(NhanVien, ma_nhan_vien=ma_nhan_vien)

    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form, mặc định giá trị 0 nếu không nhập
            luong_co_ban = Decimal(request.POST.get('luong_co_ban', '0'))
            hesoluong = Decimal(request.POST.get('hesoluong', '1'))
            phu_cap = Decimal(request.POST.get('phu_cap', '0'))
            thuong = Decimal(request.POST.get('thuong', '0'))
            khau_tru = Decimal(request.POST.get('khau_tru', '0'))
            bao_hiem_xa_hoi = Decimal(request.POST.get('bao_hiem_xa_hoi', '0'))
            bao_hiem_y_te = Decimal(request.POST.get('bao_hiem_y_te', '0'))
            bao_hiem_that_nghiep = Decimal(request.POST.get('bao_hiem_that_nghiep', '0'))
            thue_thu_nhap_ca_nhan = Decimal(request.POST.get('thue_thu_nhap_ca_nhan', '0'))
            tien_tang_ca = Decimal(request.POST.get('tien_tang_ca', '0'))
            ngay_tra_luong = request.POST.get('ngay_tra_luong')
            ghi_chu = request.POST.get('ghi_chu', '')

            # Kiểm tra trường bắt buộc
            if not ngay_tra_luong or luong_co_ban <= 0:
                raise ValueError("Lương cơ bản phải lớn hơn 0 và ngày trả lương không được để trống.")

            # Tạo và lưu đối tượng Luong
            luong = Luong(
                nhan_vien=nhan_vien,
                luong_co_ban=luong_co_ban,
                hesoluong=hesoluong,
                phu_cap=phu_cap,
                thuong=thuong,
                khau_tru=khau_tru,
                bao_hiem_xa_hoi=bao_hiem_xa_hoi,
                bao_hiem_y_te=bao_hiem_y_te,
                bao_hiem_that_nghiep=bao_hiem_that_nghiep,
                thue_thu_nhap_ca_nhan=thue_thu_nhap_ca_nhan,
                tien_tang_ca=tien_tang_ca,
                ngay_tra_luong=ngay_tra_luong,
                ghi_chu=ghi_chu
            )
            luong.tinh_luong_thuc_nhan()
            luong.save()

            # Thông báo thành công
            #messages.success(request, f"Lương của nhân viên {nhan_vien.ho_ten} đã được lưu thành công.")
            return redirect('view_salary', ma_nhan_vien=ma_nhan_vien)

        except ValueError as e:
            # Thông báo lỗi cho người dùng
            messages.error(request, f"Lỗi: {e}")
        except Exception:
            messages.error(request, "Có lỗi xảy ra khi lưu lương. Vui lòng thử lại.")

    # Hiển thị lại form với thông báo lỗi
    return render(request, 'enter_salary.html', {'nhan_vien': nhan_vien})
def export_excel(request):
    # Lấy mã nhân viên từ GET
    ma_nhan_vien = request.GET.get('ma_nhan_vien')

    # Lấy danh sách lương theo mã nhân viên
    if ma_nhan_vien:
        salary_details = Luong.objects.filter(nhan_vien__ma_nhan_vien__icontains=ma_nhan_vien)
    else:
        salary_details = Luong.objects.all()

    # Tính lương thực nhận nếu chưa được tính
    for detail in salary_details:
        detail.tinh_luong_thuc_nhan()

    # Tạo DataFrame từ dữ liệu
    data = {
        'Mã Nhân Viên': [detail.nhan_vien.ma_nhan_vien for detail in salary_details],
        'Tên Nhân Viên': [detail.nhan_vien.ho_ten for detail in salary_details],
        'Lương Cơ Bản': [detail.luong_co_ban for detail in salary_details],
        'Hệ số lương': [detail.hesoluong for detail in salary_details],
        'Phụ Cấp': [detail.phu_cap for detail in salary_details],
        'Thưởng': [detail.thuong for detail in salary_details],
        'Khấu Trừ': [detail.khau_tru for detail in salary_details],
        'Bảo Hiểm Xã Hội': [detail.bao_hiem_xa_hoi for detail in salary_details],
        'Bảo Hiểm Y Tế': [detail.bao_hiem_y_te for detail in salary_details],
        'Bảo Hiểm Thất Nghiệp': [detail.bao_hiem_that_nghiep for detail in salary_details],
        'Thuế Thu Nhập Cá Nhân': [detail.thue_thu_nhap_ca_nhan for detail in salary_details],
        'Tiền Tăng Ca': [detail.tien_tang_ca for detail in salary_details],
        'Lương Thực Nhận': [detail.luong_thuc_nhan for detail in salary_details],
        'Ngày Trả Lương': [detail.ngay_tra_luong.strftime('%Y-%m-%d') for detail in salary_details],
        'Ghi Chú': [detail.ghi_chu for detail in salary_details],
    }

    df = pd.DataFrame(data)

    # Tạo HttpResponse để trả về file Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=salary_details.xlsx'

    # Xuất dữ liệu ra Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Bảng Lương')

    return response
# def employee(request):
#      if request.method == 'GET':
#         ma_nhan_vien = request.GET.get('ma_nhan_vien')
#         if ma_nhan_vien:
#             employees = NhanVien.objects.filter(ma_nhan_vien=ma_nhan_vien)
#         else:
#             employees = NhanVien.objects.all()
#         return render(request, 'employee.html', {'employees': employees})
def employee(request):
    if request.method == 'GET':
        ma_nhan_vien = request.GET.get('ma_nhan_vien')
        # Lọc các nhân viên có chức vụ "Nhân viên"
        chuc_vu_nhan_vien = ChucVuNhanVien.objects.filter(ten_chuc_vu="Nhân viên").first()
        if chuc_vu_nhan_vien:
            if ma_nhan_vien:
                employees = NhanVien.objects.filter(
                    ma_nhan_vien=ma_nhan_vien,
                    ma_chuc_vu_nv=chuc_vu_nhan_vien
                )
            else:
                employees = NhanVien.objects.filter(ma_chuc_vu_nv=chuc_vu_nhan_vien)
        else:
            # Nếu không tìm thấy chức vụ "Nhân viên", trả về danh sách rỗng
            employees = NhanVien.objects.none()
            
        return render(request, 'employee.html', {'employees': employees})

def add_nhanvien_view(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ma_chuc_vu_nv_id = request.POST['ma_chuc_vu_nv']
        ma_phong_ban_id = request.POST['ma_phong_ban']
        ma_hop_dong_id = request.POST['ma_hop_dong']
        ma_chuyen_nganh_id = request.POST['ma_chuyen_nganh']
        ma_trinh_do_hoc_van_id = request.POST['ma_trinh_do_hoc_van']

        # Kiểm tra xem các ID có tồn tại hay không và lấy đối tượng tương ứng
        try:
            chuc_vu_nv = ChucVuNhanVien.objects.get(ma_chuc_vu_nv=ma_chuc_vu_nv_id)
            phong_ban = PhongBan.objects.get(ma_phong_ban=ma_phong_ban_id)
            hop_dong = HopDong.objects.get(ma_hop_dong=ma_hop_dong_id)
            chuyen_nganh = ChuyenNganh.objects.get(ma_chuyen_nganh=ma_chuyen_nganh_id)
            trinh_do_hoc_van = TrinhDoHocVan.objects.get(ma_trinh_do_hoc_van=ma_trinh_do_hoc_van_id)
        except ChucVuNhanVien.DoesNotExist:
            return render(request, 'add_nhanvien.html', {'error': 'Chức vụ không hợp lệ.'})
        except PhongBan.DoesNotExist:
            return render(request, 'add_nhanvien.html', {'error': 'Phòng ban không hợp lệ.'})
        except HopDong.DoesNotExist:
            return render(request, 'add_nhanvien.html', {'error': 'Hợp đồng không hợp lệ.'})
        except ChuyenNganh.DoesNotExist:
            return render(request, 'add_nhanvien.html', {'error': 'Chuyên ngành không hợp lệ.'})
        except TrinhDoHocVan.DoesNotExist:
            return render(request, 'add_nhanvien.html', {'error': 'Trình độ học vấn không hợp lệ.'})

        # Tạo đối tượng nhân viên
        nhan_vien = NhanVien(
            ma_nhan_vien=request.POST['ma_nhan_vien'],
            mat_khau=request.POST['mat_khau'],
            ho_ten=request.POST['ho_ten'],
            ngay_sinh=request.POST['ngay_sinh'],
            que_quan=request.POST['que_quan'],
            hinh_anh=request.FILES['hinh_anh'],
            gioi_tinh=request.POST['gioi_tinh'],
            dan_toc=request.POST['dan_toc'],
            sdt_nhan_vien=request.POST['sdt_nhan_vien'],
            ma_chuc_vu_nv=chuc_vu_nv,  # Thay đổi ở đây
            trang_thai=request.POST['trang_thai'] == 'True',  # Chuyển đổi chuỗi sang boolean
            ma_phong_ban=phong_ban,    # Thay đổi ở đây
            ma_hop_dong=hop_dong,      # Thay đổi ở đây
            ma_chuyen_nganh=chuyen_nganh,  # Thay đổi ở đây
            ma_trinh_do_hoc_van=trinh_do_hoc_van,  # Thay đổi ở đây
            cmdn=request.POST['cmdn'],
        )
        nhan_vien.save()
        return redirect('employee')

    else:
        # Lấy danh sách cho các dropdown
        context = {
            'chuc_vu_list': ChucVuNhanVien.objects.all(),
            'phong_ban_list': PhongBan.objects.all(),
            'hop_dong_list': HopDong.objects.all(),
            'chuyen_nganh_list': ChuyenNganh.objects.all(),
            'trinh_do_list': TrinhDoHocVan.objects.all(),
        }
        return render(request, 'add_nhanvien.html', context)
def delete_nhanvien_view(request, ma_nhan_vien):
    # Lấy nhân viên theo mã
    nhan_vien = get_object_or_404(NhanVien, ma_nhan_vien=ma_nhan_vien)

    if request.method == 'POST':
        # Xóa nhân viên
        nhan_vien.delete()
        return redirect('employee')  # Chuyển hướng về danh sách nhân viên

    return render(request, 'confirm_delete.html', {'nhan_vien': nhan_vien})# Chuyển hướng về trang danh sách nhân viên

def edit_nhanvien_view(request, ma_nhan_vien):
    # Lấy thông tin nhân viên theo mã
    nhan_vien = get_object_or_404(NhanVien, ma_nhan_vien=ma_nhan_vien)

    if request.method == 'POST':
        form = NhanVienForm(request.POST, request.FILES, instance=nhan_vien)
        if form.is_valid():
            form.save()
            return redirect('employee')  # Chuyển hướng về danh sách nhân viên
    else:
        form = NhanVienForm(instance=nhan_vien)

    return render(request, 'edit_nhanvien.html', {'form': form, 'nhan_vien': nhan_vien})


def attendance_view(request):
    search_date = request.GET.get('search_date')
    
    # Lấy dữ liệu chấm công theo ngày hoặc toàn bộ
    if search_date:
        cham_cong = ChamCong.objects.filter(ngay_cham_cong=search_date)
    else:
        cham_cong = ChamCong.objects.all()

    employees = NhanVien.objects.all()

    if request.method == 'POST':
        for employee in employees:
            ngay_cham_cong = request.POST.get(f'ngay_cham_cong_{employee.ma_nhan_vien}')
            gio_vao = request.POST.get(f'gio_vao_{employee.ma_nhan_vien}')
            gio_ra = request.POST.get(f'gio_ra_{employee.ma_nhan_vien}')
            ghi_chu = request.POST.get(f'ghi_chu_{employee.ma_nhan_vien}')

            # Kiểm tra các trường bắt buộc
            if not ngay_cham_cong or not gio_vao or not gio_ra:
                messages.error(request, f'Vui lòng nhập đầy đủ thông tin cho nhân viên {employee.ho_ten}')
                return redirect('attendance')  # Quay lại trang chấm công và hiển thị lỗi
            
            # Tạo hoặc cập nhật bản ghi chấm công
            ChamCong.objects.update_or_create(
                nhan_vien=employee,
                ngay_cham_cong=ngay_cham_cong,
                defaults={
                    'gio_vao': gio_vao,
                    'gio_ra': gio_ra,
                    'ghi_chu': ghi_chu,
                }
            )
        
        messages.success(request, 'Đã lưu thông tin chấm công thành công')
        return redirect('attendance')

    return render(request, 'attendance.html', {
        'cham_cong': cham_cong,
        'employees': employees,
        'search_date': search_date,
    })


# def attendance_view(request):
#     employees = NhanVien.objects.all()
    
#     if request.method == 'POST':
#         for employee in employees:
#             ngay_cham_cong = request.POST.get(f'ngay_cham_cong_{employee.ma_nhan_vien}')
#             gio_vao = request.POST.get(f'gio_vao_{employee.ma_nhan_vien}')
#             gio_ra = request.POST.get(f'gio_ra_{employee.ma_nhan_vien}')
#             ghi_chu = request.POST.get(f'ghi_chu_{employee.ma_nhan_vien}')
            
#             # Kiểm tra các trường bắt buộc
#             if not ngay_cham_cong or not gio_vao or not gio_ra:
#                 messages.error(request, f'Vui lòng nhập đầy đủ thông tin cho nhân viên {employee.ho_ten}')
#                 return redirect('attendance')  # Quay lại trang chấm công và hiển thị lỗi
            
#             # Tạo hoặc cập nhật bản ghi chấm công
#             ChamCong.objects.update_or_create(
#                 nhan_vien=employee,
#                 ngay_cham_cong=ngay_cham_cong,
#                 defaults={
#                     'gio_vao': gio_vao,
#                     'gio_ra': gio_ra,
#                     'ghi_chu': ghi_chu,
#                 }
#             )
        
#         messages.success(request, 'Đã lưu thông tin chấm công thành công')
#         return redirect('attendance')

    # Lấy dữ liệu chấm công cho hiển thị
    search_date = request.GET.get('search_date')
    if search_date:
        cham_cong = ChamCong.objects.filter(ngay_cham_cong=search_date)
    else:
        cham_cong = ChamCong.objects.all()

    return render(request, 'attendance.html', {
        'employees': employees,
        'cham_cong': cham_cong,
    })

def export_employees_to_excel(request):
    # Tạo workbook và worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Danh Sách Nhân Viên'

    # Thêm tiêu đề cột, có thể thêm tất cả các trường bạn muốn
    columns = [
        'Mã Nhân Viên', 
        'Họ Tên', 
        'Ngày Sinh', 
        'Giới Tính', 
        'Quê Quán', 
        'Hình Ảnh', 
        'Dân Tộc', 
        'SĐT Nhân Viên', 
        'Chức Vụ', 
        'Trạng Thái', 
        'Phòng Ban', 
        'Hợp Đồng', 
        'Chuyên Ngành', 
        'Trình Độ Học Vấn', 
        'CMDN'
    ]
    worksheet.append(columns)

    # Lấy dữ liệu nhân viên từ cơ sở dữ liệu
    employees = NhanVien.objects.all()
    for employee in employees:
        worksheet.append([
            employee.ma_nhan_vien,
            employee.ho_ten,
            employee.ngay_sinh,
            employee.get_gioi_tinh_display(),
            employee.que_quan,
            employee.hinh_anh.url if employee.hinh_anh else '',  # Kiểm tra xem có hình ảnh không
            employee.dan_toc,
            employee.sdt_nhan_vien,
            employee.ma_chuc_vu_nv.ten_chuc_vu if employee.ma_chuc_vu_nv else '',  # Kiểm tra xem có chức vụ không
            employee.trang_thai,
            employee.ma_phong_ban.ten_phong_ban if employee.ma_phong_ban else '',  # Kiểm tra xem có phòng ban không
            employee.ma_hop_dong.loai_hop_dong if employee.ma_hop_dong else '',  # Kiểm tra xem có hợp đồng không
            employee.ma_chuyen_nganh.ten_chuyen_nganh if employee.ma_chuyen_nganh else '',  # Kiểm tra xem có chuyên ngành không
            employee.ma_trinh_do_hoc_van.ten_trinh_do if employee.ma_trinh_do_hoc_van else '',  # Kiểm tra xem có trình độ học vấn không
            employee.cmdn,
        ])

    # Tạo response
    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="danh_sach_nhan_vien.xlsx"'
    return response


def profile_view(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = NhanVien.objects.get(ma_nhan_vien=user_id)
            return render(request, 'profile.html', {'user': user})
        except NhanVien.DoesNotExist:
            messages.error(request, "Người dùng không tồn tại.")
            return redirect('login')

    return redirect('login')  # Chuyển hướng đến trang đăng nhập nếu không có user_id

def update_info_view_ql(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = NhanVien.objects.get(ma_nhan_vien=user_id)

            if request.method == 'POST':
                user.ho_ten = request.POST.get('ho_ten', user.ho_ten)
                user.ngay_sinh = request.POST.get('ngay_sinh', user.ngay_sinh)
                user.que_quan = request.POST.get('que_quan', user.que_quan)
                user.sdt_nhan_vien = request.POST.get('sdt_nhan_vien', user.sdt_nhan_vien)
                user.dan_toc = request.POST.get('dan_toc', user.dan_toc)

                # Cập nhật hình ảnh nếu có
                if request.FILES.get('hinh_anh'):
                    user.hinh_anh = request.FILES['hinh_anh']

                user.save()
                messages.success(request, "Cập nhật thông tin thành công!")
                return redirect('profile')  # Chuyển hướng đến trang thông tin cá nhân

            return render(request, 'profile.html', {'user': user})

        except NhanVien.DoesNotExist:
            messages.error(request, "Người dùng không tồn tại.")
            return redirect('login')

    return redirect('login')
