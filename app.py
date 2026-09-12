import pandas as pd
import streamlit as st

st.set_page_config(page_title="Teacher Portal", layout="wide")

st.title("🍎 Teacher Data Cleaning & Marks Portal")

# File Uploader for Teachers
uploaded_file = st.file_uploader("Upload raw Excel marksheet", type=["xlsx", "xls"])

if uploaded_file is not None:
    # 1. Automatic Cleaning Pipeline
    df = pd.read_excel(uploaded_file)
    df = df.drop_duplicates(subset=["Student ID"])

    subjects = [
        "Bahasa Melayu",
        "English Language",
        "Mathematics",
        "History (Sejarah)",
        "Islamic Education",
        "Additional Mathematics",
        "Physics",
        "Chemistry",
    ]

    for sub in subjects:
        if sub in df.columns:
            df[sub] = pd.to_numeric(df[sub], errors="coerce").fillna(0)
            df[sub] = df[sub].clip(0, 100).round(1)

    df["Average Score"] = df[subjects].mean(axis=1).round(2)
    df["Status"] = df["Average Score"].apply(
        lambda x: "Pass" if x >= 50 else "Fail"
    )

    st.success("Data successfully cleaned!")

    # 2. Interactive Data Editor
    st.subheader("Edit Student Scores")
    edited_df = st.data_editor(df, num_rows="dynamic")

    # 3. Download Clean Data
    csv_data = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Cleaned CSV",
        data=csv_data,
        file_name="Cleaned_Student_Data.csv",
        mime="text/csv",
    )