import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Hóa Đơn Trà Sữa", page_icon="🧋", layout="centered")

# Khởi tạo giỏ hàng trong session_state nếu chưa có
if "gio_hang" not in st.session_state:
    st.session_state.gio_hang = []

st.image("quang-cao-tra-sua-phela.jpg")
st.title("🧋 Ứng Dụng Tính Hóa Đơn Trà Sữa")
st.write("Vui lòng chọn thông tin món và thêm vào giỏ hàng:")

# Danh sách menu trà sữa và giá (VND)
MENU_TRA_SUA = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa Ô long": 35000,
    "Trà sữa Trân châu đường đen": 40000,
    "Trà xanh Thái xanh / Thái đỏ": 32000,
    "Trà xoài kem cheese": 45000,
    "Trà sữa Lài (Jasmine Milk Tea)": 35000,
    "Trà sữa Matcha Latte": 42000,
    "Trà sữa Hạt dẻ nướng": 45000,
    "Trà sữa Khoai môn": 38000,
    "Trà hoa quả nhiệt đới": 40000,
    "Trà đào cam sả": 38000,
    "Sữa tươi trân châu đường đen": 45000,
}

# Danh sách topping và giá (VND)
MENU_TOPPING = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch pudding": 7000,
    "Kem cheese": 10000,
    "Sương sáo": 5000,
    "Trân châu hoàng kim": 7000,
    "Thạch dừa": 5000,
    "Thạch củ năng": 8000,
    "Bánh flan": 10000,
    "Kem macchiato": 10000,
}

st.divider()

# --- FORM NHẬP THÔNG TIN MÓN ---
st.subheader("📝 Chọn món")
col1, col2 = st.columns(2)

with col1:
    ten_mon = st.selectbox("1. Chọn loại trà sữa:", list(MENU_TRA_SUA.keys()))
    so_luong = st.number_input("2. Số lượng:", min_value=1, max_value=50, value=1, step=1)

with col2:
    muc_duong = st.radio("3. Mức độ đường:", ["100%", "70%", "50%", "0%"], horizontal=True)
    muc_da = st.radio("4. Mức độ đá:", ["100%", "70%", "50%", "0%"], horizontal=True)

toppings_chon = st.multiselect("5. Chọn thêm Topping (có thể chọn nhiều):", list(MENU_TOPPING.keys()))

# Tính toán giá từng món
gia_ly = MENU_TRA_SUA[ten_mon]
gia_toppings = sum(MENU_TOPPING[top] for top in toppings_chon)
don_gia_1_ly = gia_ly + gia_toppings
thanh_tien_mon = don_gia_1_ly * so_luong

# Nút Thêm vào giỏ hàng
if st.button("➕ Thêm vào giỏ hàng", type="secondary"):
    mon_moi = {
        "ten_mon": ten_mon,
        "gia_ly": gia_ly,
        "so_luong": so_luong,
        "muc_duong": muc_duong,
        "muc_da": muc_da,
        "toppings": toppings_chon,
        "gia_toppings": gia_toppings,
        "don_gia_1_ly": don_gia_1_ly,
        "thanh_tien": thanh_tien_mon
    }
    st.session_state.gio_hang.append(mon_moi)
    st.toast(f"Đã thêm **{so_luong}x {ten_mon}** vào giỏ hàng!", icon="✅")

st.divider()

# --- HIỂN THỊ GIỎ HÀNG / KẾT QUẢ ---
st.subheader("🛒 Giỏ hàng của bạn")

if not st.session_state.gio_hang:
    st.info("Chưa có món nào trong giỏ hàng. Vui lòng chọn món ở trên và bấm 'Thêm vào giỏ hàng'.")
else:
    tong_tien_hoa_don = 0
    chi_tiet_txt_list = []

    # Hiển thị danh sách các món đã order
    for idx, item in enumerate(st.session_state.gio_hang):
        chuoi_topping = ", ".join(item["toppings"]) if item["toppings"] else "Không chọn"
        
        col_info, col_del = st.columns([5, 1])
        with col_info:
            st.markdown(f"""
            **{idx + 1}. {item['ten_mon']}** x {item['so_luong']} ly  
            - *Đường:* {item['muc_duong']} | *Đá:* {item['muc_da']}  
            - *Topping:* {chuoi_topping} (+{item['gia_toppings']:,} VNĐ/ly)  
            - *Thành tiền:* **{item['thanh_tien']:,} VNĐ**
            """)
        with col_del:
            if st.button("❌ Xóa", key=f"del_{idx}"):
                st.session_state.gio_hang.pop(idx)
                st.rerun()

        st.write("---")
        
        tong_tien_hoa_don += item["thanh_tien"]

        # Chuẩn bị thông tin từng món cho file text
        chi_tiet_txt_list.append(
            f"{idx + 1}. {item['ten_mon']} x {item['so_luong']} ly\n"
            f"   - Tùy chọn : Đường {item['muc_duong']}, Đá {item['muc_da']}\n"
            f"   - Topping  : {chuoi_topping}\n"
            f"   - Thành tiền: {item['thanh_tien']:,} VNĐ\n"
        )

    # Hiển thị Tổng tiền
    st.markdown(f"### 💰 Tổng tiền cần thanh toán: :red[{tong_tien_hoa_don:,} VNĐ]")

    # --- TẠO NỘI DUNG FILE HÓA ĐƠN ĐỂ TẢI VỀ ---
    noi_dung_chi_tiet_txt = "\n".join(chi_tiet_txt_list)
    noi_dung_hoa_don = f"""===================================
        HÓA ĐƠN BÁN HÀNG
===================================
ĐANH SÁCH MÓN ĐẶT:

{noi_dung_chi_tiet_txt}
-----------------------------------
TỔNG CỘNG     : {tong_tien_hoa_don:,} VNĐ
===================================
 Cảm ơn quý khách và hẹn gặp lại!
"""

    # --- NÚT THANH TOÁN & XUẤT FILE ---
    st.write("")
    col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1.5, 1])

    with col_btn1:
        if st.button("💳 Xác nhận thanh toán", type="primary"):
            st.balloons()
            st.success("Thanh toán thành công! Bạn có thể tải hóa đơn bên cạnh.")

    with col_btn2:
        st.download_button(
            label="📥 Tải hóa đơn (.txt)",
            data=noi_dung_hoa_don,
            file_name="hoa_don_tra_sua.txt",
            mime="text/plain"
        )

    with col_btn3:
        if st.button("🗑️ Xóa hết"):
            st.session_state.gio_hang = []
            st.rerun()
