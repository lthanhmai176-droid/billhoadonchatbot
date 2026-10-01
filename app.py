import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Hóa Đơn Trà Sữa", page_icon="🧋", layout="centered")

# Khởi tạo giỏ hàng & lịch sử chat trong session_state
if "gio_hang" not in st.session_state:
    st.session_state.gio_hang = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào! Mình là chatbot tư vấn trà sữa 🧋. Bạn đang thèm vị gì (béo ngậy, thanh mát, ít ngọt, có kem cheese...) để mình gợi ý nhé?"}
    ]

st.image("quang-cao-tra-sua-phela.jpg")
st.title("🧋 Ứng Dụng Tính Hóa Đơn Trà Sữa")

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

# --- TẠO CÁC TAB CHỨC NĂNG (GỒM ORDER VÀ CHATBOT) ---
tab_order, tab_chatbot = st.tabs(["🛒 Đặt hàng", "🤖 Chatbot Tư Vấn"])

# ==================== TAB 1: ĐẶT HÀNG ====================
with tab_order:
    st.write("Vui lòng chọn thông tin món và thêm vào giỏ hàng:")
    
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

# ==================== TAB 2: CHATBOT TƯ VẤN ====================
with tab_chatbot:
    st.subheader("💬 Trợ lý Chatbot tư vấn trà sữa")
    st.write("Hỏi chatbot để nhận gợi ý món ngon hợp gu của bạn!")

    # Hàm xử lý logic tư vấn đơn giản dựa trên từ khóa
    def bot_phan_hoi(query):
        q = query.lower()
        if "béo" in q or "ngậy" in q or "béo ngậy" in q:
            return "Nếu bạn thích vị béo ngậy, bạn nên thử **Trà xoài kem cheese (45,000 VNĐ)** hoặc **Trà sữa Hạt dẻ nướng (45,000 VNĐ)** kết hợp thêm **Kem cheese** hoặc **Kem macchiato** nhé!"
        elif "thanh" in q or "mát" in q or "trái cây" in q or "hoa quả" in q:
            return "Để giải nhiệt và thanh mát, bạn thử **Trà hoa quả nhiệt đới (40,000 VNĐ)** hoặc **Trà đào cam sả (38,000 VNĐ)**, dùng kèm **Thạch dừa** hoặc **Thạch củ năng** rất giòn ngon!"
        elif "đắng" in q or "đậm trà" in q or "ô long" in q:
            return "Nếu chọn gu đậm trà thơm nồng, hãy thử **Trà sữa Ô long (35,000 VNĐ)** hoặc **Trà sữa Lài (35,000 VNĐ)**. Nhớ giảm đường xuống 50% hoặc 70% để cảm nhận chuẩn vị trà!"
        elif "ngọt" in q or "trân châu" in q:
            return "Gu ngọt ngào chuẩn bài là **Sữa tươi trân châu đường đen (45,000 VNĐ)** hoặc **Trà sữa Trân châu đường đen (40,000 VNĐ)** kết hợp thêm **Bánh flan** béo mịn!"
        elif "giá" in q or "rẻ" in q or "bao nhiêu" in q:
            return "Món có giá tiết kiệm nhất là **Trà sữa truyền thống (30,000 VNĐ)** và **Trà xanh Thái (32,000 VNĐ)**. Topping giá chỉ từ 5,000 VNĐ!"
        elif "topping" in q:
            return "Quán có 10 loại topping phong phú: Trân châu đen/trắng/hoàng kim, Thạch pudding, Sương sáo, Kem cheese, Thạch dừa, Thạch củ năng, Bánh flan, Kem macchiato. Bạn thích giòn hay béo mịn?"
        else:
            return "Bạn có thể thử món bán chạy nhất quán là **Trà sữa Ô long (35k)** thêm **Trân châu hoàng kim**! Bạn thích gu ngọt béo, thanh mát hay đậm trà để mình tư vấn kĩ hơn?"

    # Hiển thị lịch sử chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Nhận tin nhắn từ người dùng
    if user_input := st.chat_input("Hỏi chatbot (ví dụ: tư vấn món béo ngậy, ít ngọt, thanh mát...)..."):
        # Lưu tin nhắn người dùng
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Chatbot trả lời
        response = bot_phan_hoi(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
