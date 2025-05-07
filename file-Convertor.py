import streamlit as st  # This is the magic tool to create our website
import pandas as pd     # This helps us work with tables (data)
from io import BytesIO  # This helps us save files for download

st.set_page_config(page_title="File Convertor", layout="wide")  # Give our page a title and layout
st.title("File Convertor & Cleaner")  # This shows the big title at the top of the page
st.write("Upload csv or excel files, clean data, and convert formats.")  # A little description

files = st.file_uploader("Upload CSV or Excel files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]  # Get the type of the file (CSV or Excel)

        # If it's a CSV file, we read it as a CSV, otherwise, we read it as an Excel file
        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.subheader(f"{file.name} - preview")  # Show the name of the file
        st.dataframe(df.head())  # Show the first few rows of the file (preview)

        # Checkbox for removing duplicates
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()  # Remove any rows that are exactly the same
            st.success("Duplicates Removed")  # Show a message saying the duplicates are gone
            st.dataframe(df.head())  # Show the cleaned data

        # Checkbox for filling missing values
        if st.checkbox(f"Fill Missing values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)  # Fill missing values with the average
            st.success("Missing values filled with mean")  # Show a message that missing values are filled
            st.dataframe(df.head())  # Show the updated data

            # Column selection for the user
            selected_columns = st.multiselect(f"Select columns -{file.name}", df.columns.tolist(), default=df.columns.tolist())
            df = df[selected_columns]  # Keep only the columns the user selected
            st.dataframe(df.head())  # Show the updated data with the selected columns

        # Checkbox for showing charts
        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include=["number"]).empty:
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])  # Show a chart for the numeric columns

        # File format conversion choice
        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)  # Choose file format

        # Download button for converted file
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()  # Prepare a space to save the file
            
            # If the user wants CSV, save the file as CSV
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, ".csv")
            else:  # If the user wants Excel, save the file as Excel
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, ".xlsx")
            
            output.seek(0)  # Move to the beginning of the file
            st.download_button(label=f"Download {new_name}", data=output, mime=mime)  # Allow the user to download the file
            
            st.success("Process completed successfully!")  # Show a success message at the end.
