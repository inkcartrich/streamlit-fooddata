# streamlit_app.py

import streamlit as st

# Initialize connection.
conn = st.connection("snowflake")

# Perform query.
df = conn.query("SELECT * from BRANDED_FOOD LIMIT 100;", ttl=600)

# Print results.
df
