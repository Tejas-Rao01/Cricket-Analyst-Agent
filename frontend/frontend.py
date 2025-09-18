import streamlit as st
import sqlite3
import pandas as pd
import requests

# Set page title and layout
st.set_page_config(page_title="Cricket Stats App", layout="wide")

# Backend API endpoint URL
BACKEND_URL = "http://localhost:8001/generate_sql"

# Main application layout
st.title("Cricket Stats App (test)")
st.write("Enter a query about a stat in cricket and I will provide you the answer")
st.markdown("---")

# User input
user_query = st.text_input("Your Query", placeholder="e.g., 'What are the to total number of matches played'")

# Button to trigger the process
if st.button("Get answer"):
    if not user_query:
        st.warning("Please enter a query.")
    else:
        try:
            # Step 1: Send the user's query to the backend API to get the SQL
            with st.spinner("Fetching answer...."):
                # This line correctly sends the "question" key
                response = requests.post(BACKEND_URL, json={"question": user_query})
                response.raise_for_status() # Raise an exception for bad status codes
                
                # This line is corrected to get the "sql_query" key from the backend
                sql_query = response.json().get("answer")
                
            if not sql_query:
                st.error("The backend did not return a valid SQL query.")
            else:
                st.success("Got a response!!")
                st.code(sql_query, language='sql')
                
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend server. Please make sure `backend.py` is running. Error: {e}")
        except Exception as e:
            st.error(f"An error occurred while processing the query. Error: {e}")

st.markdown("---")
