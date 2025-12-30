import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Academic Performance Analytics", layout="wide")

# --- LOAD CUSTOM CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- DATA PROCESSING ---
@st.cache_data
def load_data():
    # Loading real-world secondary school student data
    df = pd.read_csv("student-mat.csv", sep=";")
    # Normalizing grades to 100% scale
    df['Grade_Percentage'] = (df['G3'] / 20) * 100
    return df

try:
    df = load_data()

    # --- SIDEBAR CONTROLS ---
    st.sidebar.title("Dashboard Filters")
    st.sidebar.markdown("Adjust parameters to filter student records.")
    
    selected_school = st.sidebar.selectbox("School Code", ["All", "GP", "MS"])
    min_study_time = st.sidebar.slider("Min Weekly Study Time (Units)", 1, 4, 1)
    
    # Filter Logic
    filtered_df = df.copy()
    if selected_school != "All":
        filtered_df = filtered_df[filtered_df['school'] == selected_school]
    filtered_df = filtered_df[filtered_df['studytime'] >= min_study_time]

    # --- MAIN CONTENT ---
    st.title("🎓 Academic Performance Analytics")
    st.markdown("Exploring the correlation between socio-economic factors and student outcomes.")

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", len(filtered_df))
    col2.metric("Avg Score", f"{filtered_df['Grade_Percentage'].mean():.1f}%")
    col3.metric("Study Time Avg", f"{filtered_df['studytime'].mean():.1f}/4")
    col4.metric("Failure Rate", f"{(filtered_df['G3'] < 10).mean()*100:.1f}%")

    st.divider()

    # Interactive Visuals
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Score Distribution")
        fig1 = px.histogram(filtered_df, x="Grade_Percentage", 
                            nbins=15, 
                            color_discrete_sequence=['#58A6FF'],
                            template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("Attendance vs. Performance")
        fig2 = px.scatter(filtered_df, x="absences", y="Grade_Percentage", 
                          color="studytime",
                          size="G3",
                          hover_data=['age', 'health'],
                          template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    # Data Table View
    with st.expander("📝 View Detailed Dataset"):
        st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Ensure 'student-mat.csv' is in the root directory.")