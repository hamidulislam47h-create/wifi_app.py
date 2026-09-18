import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Excel Dashboard", layout="wide")

st.title("📊 Excel Data Viewer & Interactive Editor")

DEFAULT_FILE = "data.xlsx"
df = None

# ১. ফাইল লোড করা
if os.path.exists(DEFAULT_FILE):
    # header=0 দিয়ে নিশ্চিত করা হচ্ছে ১ম রো-ই কলামের নাম
    df = pd.read_excel(DEFAULT_FILE)
else:
    uploaded_file = st.file_uploader(
        "একটি Excel (.xlsx) ফাইল সিলেক্ট করুন", type=["xlsx", "xls"]
    )
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        with open(DEFAULT_FILE, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.rerun()

if df is not None:
    # 'Unnamed' কলাম বা সম্পূর্ণ ফাঁকা কলাম ও রো বাদ দিয়ে স্পষ্ট করা
    df = df.loc[:, ~df.columns.str.contains("^Unnamed", na=False)]
    df = df.dropna(how="all")  # সব ঘর ফাঁকা এমন রো মুছে ফেলা

    st.subheader("📌 ওভারভিউ")
    col1, col2 = st.columns(2)
    col1.metric("মোট রো (Rows)", len(df))
    col2.metric("মোট কলাম (Columns)", len(df.columns))

    st.markdown("---")
    st.subheader("📝 সরাসরি অ্যাপে ডেটা Edit করুন")
    st.caption(
        "নিচের টেবিলে যেকোনো তথ্য সরাসরি পরিবর্তন করতে পারবেন। নতুন রো যোগ করতে একদম নিচে টাইপ করুন।"
    )

    # ২. st.data_editor দিয়ে এডিটেবল টেবিল তৈরি
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # ৩. এডিট করার পর সেভ বাটন
    if st.button("💾 পরিবর্তনগুলো Excel ফাইলে সেভ করুন"):
        edited_df.to_excel(DEFAULT_FILE, index=False)
        st.success("সফলভাবে আপডেট করা তথ্য Excel ফাইলে সেভ হয়েছে!")
        st.rerun()

    st.markdown("---")
    st.subheader("📊 ইন্টারঅ্যাক্টিভ চার্ট")

    categorical_cols = edited_df.select_dtypes(
        include=["object"]
    ).columns.tolist()
    numeric_cols = edited_df.select_dtypes(
        include=["int64", "float64", "int32", "float32"]
    ).columns.tolist()

    if categorical_cols and numeric_cols:
        col_select1, col_select2 = st.columns(2)
        with col_select1:
            x_axis = st.selectbox("X-Axis (ক্যাটাগরি):", categorical_cols)
        with col_select2:
            y_axis = st.selectbox("Y-Axis (সংখ্যা/মান):", numeric_cols)

        fig_bar = px.bar(
            edited_df,
            x=x_axis,
            y=y_axis,
            color=x_axis,
            title=f"{x_axis} অনুযায়ী {y_axis}",
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("গ্রাফ তৈরি করতে টেক্সট এবং নম্বর সংবলিত কলাম প্রয়োজন।")
else:
    st.info("শুরু করতে উপরে আপনার Excel ফাইলটি আপলোড করুন।")
