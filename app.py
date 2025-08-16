# app.py

import streamlit as st
import pandas as pd
import os
from data_processor import load_and_clean_data, perform_eda, generate_ai_summary

# --- Page Configuration ---
st.set_page_config(page_title="Automated Data Analytics App", page_icon="🤖", layout="wide")

# --- App Title and Description ---
st.title("🤖 AI-Powered Data Analytics and Visualization Tool")
st.write("Upload any CSV dataset for automated cleaning, analysis, and AI-powered insights.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("1. Configuration")
    api_key = st.text_input("Enter your Google API Key", type="password")
    st.markdown("[Get your Google API key](https://aistudio.google.com/)")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    cleaned_df = load_and_clean_data(uploaded_file.getvalue())
    if cleaned_df is not None:
        st.success("Data loaded and cleaned successfully!")
        st.subheader("📄 Cleaned Data Preview")
        st.dataframe(cleaned_df.head())

        with st.sidebar:
            st.header("2. Select Columns for Analysis")
            numerical_cols = cleaned_df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = cleaned_df.select_dtypes(include=['object', 'category']).columns.tolist()
            num_col_select = st.selectbox("Select numerical column:", options=numerical_cols)
            cat_col_select = st.selectbox("Select categorical column:", options=categorical_cols)

        if st.button("Analyze Data"):
            if not api_key:
                st.error("Please enter your Google API Key in the sidebar to proceed.")
            elif not num_col_select or not cat_col_select:
                st.warning("Please select columns for analysis from the sidebar.")
            else:
                with st.spinner('Performing analysis and contacting AI...'):
                    eda_summary = perform_eda(cleaned_df, num_col_select, cat_col_select)
                    ai_summary = generate_ai_summary(eda_summary, api_key)
                    st.success("Analysis Complete!")
                    st.header("📊 Analysis Results")
                    st.subheader("🤖 AI-Generated Insights")
                    st.markdown(ai_summary)

                    # --- UPDATED VISUALIZATIONS SECTION ---
                    st.subheader("📈 Visualizations")
                    
                    # Create a 2x2 grid for charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if os.path.exists('dynamic_histogram.png'):
                            st.image('dynamic_histogram.png', caption=f'Distribution of {num_col_select}')
                        if os.path.exists('dynamic_boxplot.png'):
                            st.image('dynamic_boxplot.png', caption=f'{num_col_select} by {cat_col_select}')
                    
                    with col2:
                        if os.path.exists('dynamic_barchart.png'):
                            st.image('dynamic_barchart.png', caption=f'Counts by {cat_col_select}')
                        if os.path.exists('correlation_heatmap.png'):
                            st.image('correlation_heatmap.png', caption='Correlation Heatmap')

    else:
        st.error("Failed to process the data. Please check the file format or contents.")