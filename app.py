import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Hóa Đơn Trà Sữa", page_icon="🧋", layout="centered")
st.image("quang-cao-tra-sua-phela.jpg")
st.title("🧋 Ứng Dụng Tính Hóa Đơn Trà Sữa")
st.write("Vui lòng chọn thông tin đơn hàng bên dưới:")

# Danh sách menu trà sữa và giá (VND)
MENU_TRA_SUA = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa Ô long": 35000,
    "Trà sữa Trân châu đường đen": 40000,
    "Trà xanh Thái xanh / Thái đỏ": 32000,
    "Trà xoài kem cheese": 45000,
}

# Danh sách topping và giá (VND)
MENU_TOPPING = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch pudding": 7000,
    "Kem cheese": 10000,
    "Sương sáo": 5000,
}

st.divider()

# --- FORM NHẬP THÔNG TIN ---
col1, col2 = st.columns(2)

with col1:
    ten_mon = st.selectbox("1. Chọn loại trà sữa:", list(MENU_TRA_SUA.keys()))
    so_luong = st.number_input("2. Số lượng:", min_value=1, max_value=50, value=1, step=1)

with col2:
    muc_duong = st.radio("3. Mức độ đường:", ["100%", "70%", "0%"], horizontal=True)
    muc_da = st.radio("4. Mức độ đá:", ["100%", "70%", "0%"], horizontal=True)

toppings_chon = st.multiselect("5. Chọn thêm Topping (có thể chọn nhiều):", list(MENU_TOPPING.keys()))

st.divider()

# --- TÍNH TOÁN CÁC CHI PHÍ ---
gia_ly = MENU_TRA_SUA[ten_mon]
gia_toppings = sum(MENU_TOPPING[top] for top in toppings_chon)
don_gia_1_ly = gia_ly + gia_toppings
tong_tien = don_gia_1_ly * so_luong

# --- HIỂN THỊ KẾT QUẢ / XEM TRƯỚC HÓA ĐƠN ---
st.subheader("🧾 Chi tiết hóa đơn")

# Tạo nội dung hiển thị hóa đơn
chuoi_topping = ", ".join(toppings_chon) if toppings_chon else "Không chọn"

# Trình bày dạng bảng chi tiết
st.markdown(f"""
* **Sản phẩm:** {ten_mon} (_{gia_ly:,} VNĐ_)
* **Số lượng:** {so_luong} ly
* **Mức đường:** {muc_duong}
* **Mức đá:** {muc_da}
* **Topping kèm theo:** {chuoi_topping} (_{gia_toppings:,} VNĐ/ly_)
* **Đơn giá 1 ly (gồm topping):** **{don_gia_1_ly:,} VNĐ**
---
### 💰 Tổng tiền cần thanh toán: :red[{tong_tien:,} VNĐ]
""")

# --- TẠO NỘI DUNG FILE HÓA ĐƠN ĐỂ TẢI VỀ ---
noi_dung_hoa_don = f"""===================================
        HÓA ĐƠN BÁN HÀNG
===================================
Sản phẩm      : {ten_mon}
Đơn giá gốc   : {gia_ly:,} VNĐ
Số lượng      : {so_luong}

Tùy chọn:
- Đường       : {muc_duong}
- Đá          : {muc_da}
- Topping     : {chuoi_topping} (+{gia_toppings:,} VNĐ/ly)

-----------------------------------
Đơn giá 1 ly  : {don_gia_1_ly:,} VNĐ
TỔNG CỘNG     : {tong_tien:,} VNĐ
===================================
 Cảm ơn quý khách và hẹn gặp lại!
"""

# --- NÚT THANH TOÁN & XUẤT FILE ---
st.write("")
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    if st.button("💳 Xác nhận thanh toán", type="primary"):
        st.balloons()
        st.success("Thanh toán thành công! Bạn có thể tải hóa đơn ở nút bên cạnh.")

with col_btn2:
    st.download_button(
        label="📥 Tải hóa đơn (.txt)",
        data=noi_dung_hoa_don,
        file_name=f"hoa_don_{ten_mon.replace(' ', '_')}.txt",
        mime="text/plain"
    )
