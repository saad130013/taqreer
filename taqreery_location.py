import streamlit as st
import pandas as pd
import plotly.express as px

# تحميل كل الشيتات
@st.cache_data
def load_all_sheets():
    excel_file = "DUTY ROSTER MAR 2025.V.2.xlsx"
    xls = pd.ExcelFile(excel_file)
    df_all = pd.concat([xls.parse(sheet) for sheet in xls.sheet_names], ignore_index=True)
    return df_all

df = load_all_sheets()

st.set_page_config(layout="wide", page_title="تقريري - المواقع", page_icon="📍")
st.title("📍 تقريري - تحليل حسب المواقع LOCATION")

# التحقق من وجود العمود
if "LOCATION" not in df.columns:
    st.warning("⚠️ عمود LOCATION غير موجود في أي شيت.")
else:
    selected_location = st.selectbox("اختر موقع", sorted(df["LOCATION"].dropna().unique()))

    location_df = df[df["LOCATION"] == selected_location]

    st.markdown("---")
    st.subheader(f"📊 الإحصائيات العامة للموقع: {selected_location}")
    total = len(location_df)
    st.metric("عدد الموظفين", total)

    if "NATIONALITY" in location_df.columns:
        nationality_summary = location_df["NATIONALITY"].value_counts().reset_index()
        nationality_summary.columns = ["الجنسية", "عدد الموظفين"]
        st.dataframe(nationality_summary, use_container_width=True)

        fig_nat = px.pie(nationality_summary, names="الجنسية", values="عدد الموظفين", title="نسبة توزيع الجنسيات")
        st.plotly_chart(fig_nat, use_container_width=True)

    st.subheader("📄 جدول تفصيلي:")
    st.dataframe(location_df, use_container_width=True)
