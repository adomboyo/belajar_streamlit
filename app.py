import streamlit as st

st.set_page_config(
    page_title="Belajar Streamlit",
    page_icon="🚀",
    layout="centered",
)

st.title("🚀 Belajar Streamlit")
st.subheader("Selamat datang di aplikasi Streamlit pertama saya!")

st.markdown("---")

# Interactive widgets
name = st.text_input("Siapa nama kamu?", placeholder="Ketik nama kamu di sini...")

if name:
    st.success(f"Halo, **{name}**! 👋 Selamat belajar Streamlit!")

# Simple counter
st.markdown("---")
st.subheader("🔢 Counter Sederhana")

col1, col2, col3 = st.columns(3)

if "count" not in st.session_state:
    st.session_state.count = 0

with col1:
    if st.button("➖ Kurangi"):
        st.session_state.count -= 1

with col2:
    st.metric(label="Nilai", value=st.session_state.count)

with col3:
    if st.button("➕ Tambah"):
        st.session_state.count += 1

# About section
st.markdown("---")
st.info("💡 Aplikasi ini dibuat untuk belajar Streamlit dan di-deploy ke Streamlit Community Cloud.")
