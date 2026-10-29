import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client (optional use later)
client = genai.Client(api_key=api_key)

st.title("🤖 AI-Powered Data Cleaning Agent")
st.write("Upload your dataset to scan for specific row and column errors.")

# 1. File Uploader
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    # 2. Scanning Logic with Row & Column Tracking
    if st.button("Scan Data for Issues"):
        with st.spinner("Scanning rows and columns..."):
            
            # Track missing value coordinates -> {col_name: [row_indices]}
            missing_details = {}
            for col in df.columns:
                null_rows = df[df[col].isnull()].index.tolist()
                if null_rows:
                    missing_details[col] = null_rows

            # Track type mismatch coordinates (text in numeric columns) -> {col_name: [row_indices]}
            type_issue_details = {}
            for col in df.select_dtypes(include=['number']).columns:
                # Find rows where data is not null, but fails numeric conversion
                non_numeric_mask = pd.to_numeric(df[col], errors='coerce').isnull() & df[col].notnull()
                mismatch_rows = df[non_numeric_mask].index.tolist()
                if mismatch_rows:
                    type_issue_details[col] = mismatch_rows

            # Store findings in session state
            st.session_state['missing_details'] = missing_details
            st.session_state['type_issue_details'] = type_issue_details
            st.session_state['df'] = df
            st.success("Scan complete!")

    # 3. Display Findings with Exact Row/Column Locations
    if 'missing_details' in st.session_state:
        st.markdown("---")
        st.subheader("🔍 Detailed Scan Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📭 Missing Values (NaN/Null)")
            miss_dict = st.session_state['missing_details']
            if miss_dict:
                for col, rows in miss_dict.items():
                    st.write(f"- **Column:** `{col}`")
                    st.write(f"  - **Empty Count:** {len(rows)}")
                    st.write(f"  - **Row Index(es):** {rows}")
            else:
                st.write("No missing values found! 🎉")
                
        with col2:
            st.markdown("### ⚠️ Type Mismatches (Text in Numeric or vice versa)")
            type_dict = st.session_state['type_issue_details']
            if type_dict:
                for col, rows in type_dict.items():
                    st.write(f"- **Column:** `{col}`")
                    st.write(f"  - **Invalid Count:** {len(rows)}")
                    st.write(f"  - **Row Index(es):** {rows}")
            else:
                st.write("No type mismatches found! 🎉")

        # 4. Action Prompt (Clean or Keep)
        st.markdown("---")
        st.subheader("🛠️ Action Required")
        cleaning_choice = st.radio(
            "How would you like to handle these anomalies?",
            ("Keep data as it is", "Clean data automatically (Coerce types & Fill missing values)")
        )

        if cleaning_choice == "Clean data automatically (Coerce types & Fill missing values)":
            if st.button("Apply Cleaning"):
                cleaned_df = st.session_state['df'].copy()
                
                # Automated cleaning implementation
                for col in cleaned_df.select_dtypes(include=['number']).columns:
                    cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
                
                for col in cleaned_df.select_dtypes(include=['object']).columns:
                    cleaned_df[col] = cleaned_df[col].fillna("Unknown")
                
                st.session_state['cleaned_df'] = cleaned_df
                st.success("Data cleaned successfully!")
                
                # Show preview and download button
                st.dataframe(cleaned_df.head())
                st.download_button(
                    label="Download Cleaned CSV",
                    data=cleaned_df.to_csv(index=False).encode('utf-8'),
                    file_name="cleaned_dataset.csv",
                    mime="text/csv",
                )