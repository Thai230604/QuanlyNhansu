# hr/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),  # Đường dẫn cho trang đăng nhập
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),      # Đường dẫn cho trang home (quản lý)
    path('home_nhanvien/', home_nhanvien_view, name='home_nhanvien'),  
    path('update_info/', update_info_view, name='update_info'),
    path('insurance/', insurance, name='insurance'),
    path('contract/', contract, name='contract'),
    path('leave/', leave, name='leave'),
    path('reward_punishment/', reward_punishment, name='reward_punishment'),
    # path('deduction/', deduction, name='deduction'),
    path('deduction/edit/<str:ma_phong_ban>/', edit_phong_ban, name='edit_phong_ban'),
    path('deduction/delete/<str:ma_phong_ban>/', delete_phong_ban, name='delete_phong_ban'),
    path('deduction/', deduction_view, name='deduction'),
    path('attendance/', attendance_view, name='attendance'),
    path('employee/', employee, name='employee'),
    path('add-nhan-vien/', add_nhanvien_view, name='add_nhanvien'),
    path('delete-nhan-vien/<str:ma_nhan_vien>/', delete_nhanvien_view, name='delete_nhanvien'),  # URL xóa
    path('edit-nhan-vien/<str:ma_nhan_vien>/', edit_nhanvien_view, name='edit_nhanvien'),
    path('export-employees/', export_employees_to_excel, name='export_employees'),
    path('salary/', salary_view, name='salary'),
    path('salary/<str:ma_nhan_vien>/', enter_salary_view, name='enter_salary'),
    path('view_salary/<str:ma_nhan_vien>/', view_salary_view, name='view_salary'),
    path('export_excel/', export_excel, name='export_excel'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_info_view_ql, name='update_profile'),
    path('view_salary_nhanvien/<str:ma_nhan_vien>/', view_salary_nhanvien, name='view_salary_nhanvien'),
    # path('salary/chart/', chart_view, name='salary_chart'),
 # Đường dẫn cho biểu đồ
]
