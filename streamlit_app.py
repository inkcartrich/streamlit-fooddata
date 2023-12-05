# streamlit_app.py

import streamlit as st
import pandas as pd

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA FoodData Central")

st.subheader("Explore the USDA FoodData Central dataset!")

suggestions_query = f"""
SELECT DISTINCT BRAND_OWNER, BRAND_NAME from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_NAME IS NOT NULL AND LENGTH(BRANDED_FOOD.BRAND_NAME) > 0
    LIMIT 100;
"""

df_suggest = conn.query(suggestions_query, ttl=600)

df_suggest['concat'] = df_suggest['BRAND_OWNER'] + " - " + df_suggest['BRAND_NAME']

st.text("Suggestions preview:")
st.dataframe(df_suggest,
            hide_index = True)

search_brand_name = st.selectbox(
    "Select or search for a brand name",
    df_suggest['concat'],
    None,
    format_func=lambda x: x.title()
)

st.text("Selected product:")

df_selection = df_suggest[df_suggest['concat'] == search_brand_name][['BRAND_OWNER', 'BRAND_NAME']]

st.dataframe(df_selection,
            hide_index = True)

st.write(df_selection[['BRAND_NAME']].iloc[0].to_string(index=False))

query_detailed_string = f"""
SELECT * from BRANDED_FOOD 
    WHERE BRAND_NAME = UPPER('{df_selection[['BRAND_NAME']]}')
    LIMIT 100;
"""

# Perform query.
df_raw = conn.query(query_detailed_string, ttl=600)

df_display = df_raw[['BRAND_OWNER', 'BRAND_NAME', 'GTIN_UPC', 'INGREDIENTS']]

# Print results.
st.dataframe(df_display,
            hide_index=True)
