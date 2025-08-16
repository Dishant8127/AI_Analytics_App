# data_processor.py

import pandas as pd
import io
import os
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai

# The load_and_clean_data and generate_ai_summary functions are unchanged.
def load_and_clean_data(file_content):
    """Loads and cleans data from uploaded file content."""
    print("--- Starting Data Loading and Cleaning ---")
    try:
        df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
    except Exception as e:
        return None
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    return df

def generate_ai_summary(eda_summary_text, api_key):
    """Generates AI summary using the Gemini API."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        You are an expert data analyst. Based on the following summary statistics, provide a concise business insights report including:
        1. A high-level summary.
        2. Interesting patterns or outliers.
        3. Three actionable business recommendations.
        Keep the tone professional and easy for a manager to understand.
        ---
        {eda_summary_text}
        ---
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Could not generate AI summary. Please check your API key and internet connection."

# UPDATED FUNCTION
def perform_eda(df, numerical_col, categorical_col):
    """
    Performs EDA and saves multiple visualizations.
    """
    print("\n--- Starting Exploratory Data Analysis (EDA) ---")
    summary_stats = df.describe(include='all')
    sns.set_style("whitegrid")

    # a) Histogram for the selected numerical column
    if numerical_col:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[numerical_col], kde=True, bins=15)
        plt.title(f'Distribution of {numerical_col}')
        plt.savefig('dynamic_histogram.png')
        plt.close()

    # b) Bar Chart for the selected categorical column
    if categorical_col:
        plt.figure(figsize=(10, 6))
        sns.countplot(y=df[categorical_col])
        plt.title(f'Count of Items by {categorical_col}')
        plt.tight_layout()
        plt.savefig('dynamic_barchart.png')
        plt.close()

    # c) NEW: Box Plot to compare distributions
    if numerical_col and categorical_col:
        plt.figure(figsize=(12, 7))
        sns.boxplot(x=df[categorical_col], y=df[numerical_col])
        plt.title(f'{numerical_col} Distribution by {categorical_col}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('dynamic_boxplot.png')
        plt.close()

    # d) NEW: Correlation Heatmap for all numerical columns
    numerical_df = df.select_dtypes(include='number')
    if len(numerical_df.columns) > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(numerical_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('correlation_heatmap.png')
        plt.close()

    print("\n--- ✅ EDA Complete ---")
    return summary_stats.to_string()