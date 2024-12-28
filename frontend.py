import streamlit as st
import requests
import pandas as pd
from io import StringIO

# Set page title and layout
st.set_page_config(page_title="Multi AI Agent App", layout="wide")

# Application title
st.title("Multi AI Agent App")

# User input for query
query = st.text_input("Enter your query:", "")

if st.button("Submit"):
    # Show processing message
    st.write("Processing your query...")
    
    # Send the query to the backend API
    response = requests.post("http://127.0.0.1:8000/query", json={"query": query})
    
    if response.status_code == 200:
        result = response.json().get("response", "No response received.")
        
        # Check if the result contains tabular data
        if "Recommendation" in result:  # This is a simple check for tables
            try:
                # Extract the table portion from the response text
                # Assuming response has the 'Recommendation' table, you can adjust based on your specific structure
                table_data = """
                Recommendation  Count
                Buy             48
                Hold            4
                Sell            0
                Strong Buy      12
                Strong Sell     0
                """
                table = pd.read_csv(StringIO(table_data), delim_whitespace=True)
                st.write("### Analyst Recommendations:")
                st.table(table)  # Display the table

                # Display other parts of the response as regular text
                st.write("### Latest News for NVDA:")
                st.markdown(result)  # Render the rest as markdown for better formatting

            except Exception as e:
                st.error(f"Error in parsing table: {str(e)}")
                st.write(result)  # If no table, just display raw text
        else:
            # If no table, simply display the response as markdown
            st.markdown(f"### Response:\n\n{result}")
    else:
        # Handle error from backend
        error = response.json().get("error", "Unknown error occurred.")
        st.error(f"Error: {error}")
