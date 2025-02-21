
# IMPORTS
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the app
st.set_page_config(page_title="📀DataSweeper", layout="wide")
st.title("📀Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# Upload files
uploaded_files = st.file_uploader(
    "Upload your files (CSV or Excel):", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)  # Corrected CSV reading
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")  # Corrected XLSX reading
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display info about the file
        st.write(f'**File Name:** {file.name}')
        file_size_kb = len(file.getvalue()) / 1024  # Corrected file size calculation
        st.write(f'**File Size:** {file_size_kb:.2f} KB')

        # Show 5 rows of the dataframe
        st.write("🔍Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("🛠️Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values For {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns  # Fixed 'numbers' to 'number'
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Have Been Filled!")


        #choose specific columns to keep or convert
        st.subheader("🎯Select columns to converts")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        #create some visulaization
        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

            #convert the file csv to excel
            st.subheader("🔄Conversion Options")
            conversion_type = st.radio(f"Convert {file.name} to:",["CSV" , "Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer,index=False)
                    file_Name = file.name.replace(file_ext,".xlxs")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)

                    #download Button
                    st.download_button(
                        label=f"⬇️Download{file.name} as {conversion_type}",
                        data=buffer,
                        filename=file_Name,
                        mime= mime_type
                    )
                    st.success("🎉All files processed!")