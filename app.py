
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. CẤU HÌNH TRANG WEB
# ==========================================

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# ==========================================
# 2. TẠO DATAFRAME
# ==========================================

data = {
    "Họ và Tên": [
        "Nguyễn Văn An",
        "Trần Thị Bính",
        "Lê Hoàng Cường",
        "Phạm Thị Dung",
        "Hoàng Minh Đức",
        "Võ Ngọc Hà",
        "Đặng Quốc Huy",
        "Bùi Thị Lan",
        "Đỗ Thành Nam",
        "Nguyễn Thu Trang"
    ],
    "Điểm chuyên cần": [
        9.0, 8.5, 7.5, 9.5, 8.0,
        10.0, 7.0, 8.5, 9.0, 8.0
    ],
    "Điểm giữa kỳ": [
        8.0, 7.5, 6.5, 9.0, 7.0,
        8.5, 6.0, 8.0, 7.5, 9.0
    ],
    "Điểm cuối kỳ": [
        8.5, 8.0, 7.0, 9.5, 7.5,
        9.0, 6.5, 8.5, 8.0, 9.5
    ]
}

df = pd.DataFrame(data)

# ==========================================
# 3. TÍNH ĐIỂM TỔNG KẾT
# ==========================================

df["Tổng kết"] = (
    0.2 * df["Điểm chuyên cần"]
    + 0.3 * df["Điểm giữa kỳ"]
    + 0.5 * df["Điểm cuối kỳ"]
)

# ==========================================
# 4. XẾP LOẠI
# ==========================================

def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# ==========================================
# 5. HIỂN THỊ BẢNG ĐIỂM
# ==========================================

st.subheader("📋 Bảng điểm sinh viên")

bang_diem = df.rename(columns={
    "Ho_va_ten": "Họ và Tên",
    "Diem_chuyen_can": "Chuyên cần",
    "Diem_giua_ky": "Giữa kỳ",
    "Diem_cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(
    bang_diem,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Chuyên cần": st.column_config.NumberColumn(
            format="%.2f"
        ),
        "Giữa kỳ": st.column_config.NumberColumn(
            format="%.2f"
        ),
        "Cuối kỳ": st.column_config.NumberColumn(
            format="%.2f"
        ),
        "Tổng kết": st.column_config.NumberColumn(
            format="%.2f"
        )
    }
)

# ==========================================
# 6. THỐNG KÊ ĐIỂM
# ==========================================

st.subheader("📊 Thống kê kết quả học tập")

diem_tb = df["Tổng kết"].mean()
sv_cao_nhat = df.loc[df["Tổng kết"].idxmax()]
sv_thap_nhat = df.loc[df["Tổng kết"].idxmin()]
so_sv_dat = int((df["Tổng kết"] >= 5).sum())

cot1, cot2, cot3, cot4 = st.columns(4)

cot1.metric(
    "Điểm trung bình lớp",
    f"{diem_tb:.2f}"
)

cot2.metric(
    "Điểm cao nhất",
    f"{sv_cao_nhat['Tổng kết']:.2f}",
    help=sv_cao_nhat["Họ và Tên"]
)

cot3.metric(
    "Điểm thấp nhất",
    f"{sv_thap_nhat['Tổng kết']:.2f}",
    help=sv_thap_nhat["Họ và Tên"]
)

cot4.metric(
    "Số sinh viên đạt",
    f"{so_sv_dat}/{len(df)}"
)

st.info(
    f"Sinh viên cao nhất: {sv_cao_nhat['Họ và Tên']} "
    f"({sv_cao_nhat['Tổng kết']:.2f} điểm)"
)

st.info(
    f"Sinh viên thấp nhất: {sv_thap_nhat['Họ và Tên']} "
    f"({sv_thap_nhat['Tổng kết']:.2f} điểm)"
)

# ==========================================
# 7. SELECTBOX CHỌN SINH VIÊN
# ==========================================

st.subheader("🔎 Tra cứu điểm sinh viên")

ten_sv = st.selectbox(
    "Chọn sinh viên:",
    df["Họ và Tên"].tolist()
)

sv = df[df["Họ và Tên"] == ten_sv].iloc[0]

st.markdown(f"### Thông tin: {ten_sv}")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Chuyên cần", f"{sv['Điểm chuyên cần']:.2f}")
c2.metric("Giữa kỳ", f"{sv['Điểm giữa kỳ']:.2f}")
c3.metric("Cuối kỳ", f"{sv['Điểm cuối kỳ']:.2f}")
c4.metric("Tổng kết", f"{sv['Tổng kết']:.2f}")
c5.metric("Xếp loại", sv["Xếp loại"])

# ==========================================
# 8. BIỂU ĐỒ CỘT NGANG
# ==========================================

st.subheader("📈 Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(10, 5))

ax.barh(
    df["Họ và Tên"],
    df["Tổng kết"],
    color="cornflowerblue"
)

ax.invert_yaxis()
ax.set_xlim(0, 10)
ax.set_xticks([0, 2.5, 5, 7.5, 10])

ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Họ và Tên")

ax.grid(axis="x", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

# Hiển thị số điểm ở cuối mỗi cột
for i, diem in enumerate(df["Tổng kết"]):
    ax.text(
        diem + 0.08,
        i,
        f"{diem:.2f}",
        va="center",
        fontsize=9
    )

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ==========================================
# 9. THÔNG TIN NGƯỜI TẠO ỨNG DỤNG
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align: center; color: gray;
                font-size: 12px;">
        Người tạo: [MAI THỊ PHƯƠNG] |
        MSSV: [038308021738]
    </div>
    """,
    unsafe_allow_html=True
)
