# streamlit_app.py

import streamlit as st
import pandas as pd
from string import capwords

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA FoodData Central")

st.subheader("Explore the USDA FoodData Central dataset!")

suggestions_query = f"""
SELECT DISTINCT BRAND_OWNER, BRAND_NAME from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) AND 
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND 
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 0 AND
    BRANDED_FOOD.BRAND_OWNER != BRANDED_FOOD.BRAND_NAME
"""

df_suggest = conn.query(suggestions_query, ttl=600)

df_suggest['concat'] = df_suggest['BRAND_OWNER'] + " - " + df_suggest['BRAND_NAME']

st.text("Searching " + str(len(df_suggest)) + " brand-name products.")

selection = st.keyup("Testing")