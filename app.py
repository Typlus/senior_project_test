import streamlit as st
import pandas as pd
import math
import functions 
import reports
from pathlib import Path
st.title ("ImmersaVLM")
# grab what species of animal they want to filter from the database
    # this can be done by have a running dictionary of them and pull from that
    # place for more filters to be added 
    #Upload audio file
uploaded_audio = st.file_uploader("Upload an audio file", type=["wav", "flac", "ogg", "m4a"])
if uploaded_audio is not None:
    st.audio(uploaded_audio)
    st.success(f"Uploaded: {uploaded_audio.name}")

# Inference controls below the upload box
    inf_threshold = st.slider("Inference threshold (minimum confidence %)", min_value=0, max_value=100, value=20, step=5, format="%d%%")

    # Model selection: list .pth files in models/ or fall back to project root model
    models_dir = Path("models")
    try:
        model_files = sorted([p.name for p in models_dir.glob("*.pth")])
    except Exception:
        model_files = []

    if not model_files:
        # fallback to root model filename if present
        if Path("best_supervised_model.pth").exists():
            model_files = ["best_supervised_model.pth"]

    if model_files:
        model_choice = st.selectbox("Model to use:", options=model_files)
    else:
        model_choice = None
        st.error("No model (.pth) found in models/ and no best_supervised_model.pth in project root.")

user_selected_s = st.multiselect("species to filter by :",[ "Dolphin","Whale","Fish","Otter"])
user_selected_c = st.slider ("what is minumum confidance level:", min_value=00, max_value=100 , value=0 , step=10, format="%d%%")

# button to test data 
if st.button("test data"): functions.add_demo_data()
# button to generate test report using 1st record
# if st.button("test report"): reports.generate_report(1)

# deletes ALL data from the database. used for testing
# if st.button("reset"): functions.clear_database()

# create talbe header
st.subheader("table")

# If statment that activates based on the user's inputed filters. if none are chosen then ise get a;; results. if any are picked then use results by filter
if user_selected_s or user_selected_c > 0:  # add another or statment if another filter is added 
     results= functions.results_by_filter(user_selected_s, user_selected_c)
else:
     results = functions.get_all_results()

# create dataframe (visual for database)
tf = pd.DataFrame(
    results,
    columns=["ID","Species","Filename","Confidence"] # adds columns. if more features are taken from LM then add them here
)

ROWS_PER_PAGE = 15

total_pages = max(1, (len(tf) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE)

current_page = st.pagination(num_pages=total_pages)

start_idx = (current_page - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE

sliced_tf = tf.iloc[start_idx:end_idx]


# Table header
col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 1, 2])

col4.markdown(
    '<div style="white-space: nowrap;">Confidence</div>',
    unsafe_allow_html=True
)
col1.write("ID")
col2.write("Species")
col3.write("Filename")
# col4.write("Confidence")
col5.write("Report")


# Table rows
for _, row in sliced_tf.iterrows():

    col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 1, 2])

    col1.write(row["ID"])
    col2.write(row["Species"])
    col3.write(row["Filename"])
    col4.write(f"{row['Confidence']}%")

    if col5.button(
        "Generate Report",
        key=f"report_{row['ID']}"
    ):
        reports.generate_report(row["ID"])




##if user_selected_s or user_selected_c > 0:  
 #    results= functions.results_by_filter(user_selected_s, user_selected_c)
#else:
 #    results = functions.get_all_results()


