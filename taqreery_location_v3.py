
import streamlit as st
import pandas as pd
import plotly.express as px

# تحميل البيانات من Book2.xlsx
@st.cache_data
def load_data():
    df = pd.read_excel("Book2.xlsx", sheet_name="Sheet1")
    df.columns = df.columns.str.strip().str.upper()  # تنظيف أسماء الأعمدة
    return df

df = load_data()

st.set_page_config(layout="wide", page_title="تحليل المواقع والجنسية", page_icon="🌍")
st.title("📍 لوحة تحليل المواقع والجنسية")

if "LOCATION" not in df.columns:
    st.warning("⚠️ عمود LOCATION غير موجود.")
else:
    selected_location = st.selectbox("اختر الموقع", sorted(df["LOCATION"].dropna().unique()))
    location_df = df[df["LOCATION"] == selected_location]

    st.markdown(f"### 📌 إحصائيات الموقع: {selected_location}")
    total_employees = len(location_df)
    st.metric("عدد الموظفين الكلي", total_employees)

    if "NATIONALITY" in location_df.columns:
        nationality_summary = location_df["NATIONALITY"].value_counts().reset_index()
        nationality_summary.columns = ["الجنسية", "عدد الموظفين"]
        st.dataframe(nationality_summary, use_container_width=True)

        fig_nat = px.pie(nationality_summary, names="الجنسية", values="عدد الموظفين", title="توزيع الجنسيات")
        st.plotly_chart(fig_nat, use_container_width=True)

    if all(col in location_df.columns for col in ["SUN", "MON", "TUE", "WED", "THU"]):
        days = ["SUN", "MON", "TUE", "WED", "THU"]
        present_count = location_df[days].sum(axis=1).gt(0).sum()
        attendance_rate = (present_count / total_employees) * 100 if total_employees > 0 else 0
        st.metric("نسبة الحضور الأسبوعي", f"{attendance_rate:.2f}٪")

    if "POSITION" in location_df.columns:
        supervisor_count = location_df["POSITION"].str.contains("supervisor", case=False, na=False).sum()
        workers_count = total_employees - supervisor_count
        st.metric("عدد المشرفين", supervisor_count)
        st.metric("عدد العمال العاديين", workers_count)

    st.markdown("---")
    st.subheader("📋 جدول تفصيلي")
    st.dataframe(location_df, use_container_width=True)

# -----------------------
# تحليل حسب الجنسية عبر الأقسام
st.markdown("---")
st.subheader("🌍 تحليل الجنسيات عبر الأقسام")

if "NATIONALITY" in df.columns and "POSITION" in df.columns:
    nationality_filter = st.selectbox("اختر جنسية:", sorted(df["NATIONALITY"].dropna().unique()))
    nat_df = df[df["NATIONALITY"] == nationality_filter]

    if not nat_df.empty:
        dept_summary = nat_df["POSITION"].value_counts().reset_index()
        dept_summary.columns = ["المسمى الوظيفي", "عدد الموظفين"]
        st.dataframe(dept_summary, use_container_width=True)

        fig_dept = px.bar(dept_summary, x="المسمى الوظيفي", y="عدد الموظفين",
                          title=f"توزيع الجنسية ({nationality_filter}) حسب الوظيفة",
                          text="عدد الموظفين")
        st.plotly_chart(fig_dept, use_container_width=True)
    else:
        st.info("لا يوجد بيانات لهذه الجنسية.")
else:
    st.warning("⚠️ لم يتم العثور على أعمدة NATIONALITY أو POSITION.")
