import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Code Analyzer", page_icon="📊")

st.title(" Code Analyzer and Excel Generator")

# Load Mapping File
mapping_df = pd.read_excel("mapping.xlsx")

code_mapping = dict(
    zip(mapping_df["Code"], mapping_df["Sentence"])
)

uploaded_file = st.file_uploader(
    "Upload a text file containing codes",
    type=["txt"]
)

if uploaded_file is not None:

    # Read text file
    content = uploaded_file.read().decode("utf-8")

    codes = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    results = []

    for code in codes:
        sentence = code_mapping.get(
            code,
            "Code Not Found"
        )

        results.append({
            "Code": code,
            "Sentence": sentence
        })

    result_df = pd.DataFrame(results)

    st.success("Analysis Completed")

    st.subheader("Preview")

    st.dataframe(result_df)

    # Excel Creation
    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        result_df.to_excel(
            writer,
            index=False,
            sheet_name="Analysis"
        )

    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download Excel Report",
        data=excel_data,
        file_name="Code_Analysis_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )