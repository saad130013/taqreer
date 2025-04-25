import streamlit as st
import pandas as pd
import plotly.express as px

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_excel("DUTY ROSTER MAR 2025.V.2.xlsx")
    return df

df = load_data()

st.set_page_config(layout="wide", page_title="تقريري", page_icon="📋")
st.title("📋 لوحة متابعة العمالة - تقريري")

# ملخص عام
total_projects = df["Project"].nunique()
total_departments = df["Dept."].nunique()
total_employees = df["Actual on Site"].sum()

if "Vacation Percentage %" in df.columns:
    avg_vacation_rate = df["Vacation Percentage %"].mean()
else:
    avg_vacation_rate = 0

# عرض الكروت
col1, col2, col3, col4 = st.columns(4)
col1.metric("📍 عدد المشاريع", total_projects)
col2.metric("🏢 عدد الأقسام", total_departments)
col3.metric("👥 إجمالي الموظفين", int(total_employees))
col4.metric("📅 متوسط نسبة الإجازات", f"{avg_vacation_rate:.2f}%")

st.markdown("---")

# رسم بياني توزيع الموظفين حسب المشاريع
st.subheader("📊 توزيع الموظفين حسب المشاريع")
proj_summary = df.groupby("Project")["Actual on Site"].sum().reset_index()
fig_proj = px.pie(proj_summary, names="Project", values="Actual on Site", title="نسبة توزيع الموظفين")
st.plotly_chart(fig_proj, use_container_width=True)

# رسم بياني توزيع الموظفين حسب الأقسام
st.subheader("📊 توزيع الموظفين حسب الأقسام")
dept_summary = df.groupby("Dept.")["Actual on Site"].sum().reset_index()
fig_dept = px.bar(dept_summary, x="Dept.", y="Actual on Site", text="Actual on Site", title="عدد الموظفين لكل قسم")
st.plotly_chart(fig_dept, use_container_width=True)

# جدول تفصيلي حسب الفلترة
st.subheader("🔎 ابحث عن مشروع أو قسم محدد")
selected_project = st.selectbox("اختر مشروع", options=["كل المشاريع"] + list(df["Project"].unique()))
selected_dept = st.selectbox("اختر قسم", options=["كل الأقسام"] + list(df["Dept."].unique()))

filtered_df = df.copy()

if selected_project != "كل المشاريع":
    filtered_df = filtered_df[filtered_df["Project"] == selected_project]

if selected_dept != "كل الأقسام":
    filtered_df = filtered_df[filtered_df["Dept."] == selected_dept]

st.dataframe(filtered_df.style.set_properties(**{
    'background-color': '#f0f2f6',
    'color': 'black',
    'border-color': 'gray'
}), use_container_width=True)


# تحليل تفصيلي حسب الموقع
st.markdown("---")
st.subheader("📍 تحليل تفصيلي لموقع محدد")

if "LOCATION" in df.columns:
    selected_location = st.selectbox("اختر الموقع", options=sorted(df["LOCATION"].dropna().unique()))
    location_df = df[df["LOCATION"] == selected_location]

    st.write(f"📌 عدد الموظفين في هذا الموقع: **{location_df['Actual on Site'].sum()}**")

    if "NATIONALITY" in location_df.columns:
        nationality_summary = location_df["NATIONALITY"].value_counts().reset_index()
        nationality_summary.columns = ["الجنسية", "عدد الموظفين"]

        st.subheader("🌍 توزيع الجنسيات في هذا الموقع")
        st.dataframe(nationality_summary, use_container_width=True)

        fig_nat = px.pie(nationality_summary, names="الجنسية", values="عدد الموظفين", title="نسبة الجنسيات")
        st.plotly_chart(fig_nat, use_container_width=True)

    st.subheader("📄 جدول تفصيلي للموظفين في هذا الموقع")
    st.dataframe(location_df, use_container_width=True)
else:
    st.warning("لم يتم العثور على عمود LOCATION في الملف.")
