# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as pd
from string import capwords
from bing_image_urls import bing_image_urls

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA-FDC Explorer")
st.write("Query the USDA Fooddata Central dataset! This webapp is served on Streamlit Community Cloud and uses a Snowflake backend. The USDA-FDC dataset is available at https://fdc.nal.usda.gov/.")
st.caption("Tracking 1,947,155 records across 36,967 brands. USDA-FDC contains many duplicate vendors. For best results, search for popular brand name products.")

selector_query = f"""
SELECT DISTINCT BRAND_OWNER, BRAND_NAME
    FROM BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) > 0 AND
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 1 
"""

df_selector = conn.query(selector_query, ttl=600)

df_selector['concat'] = df_selector['BRAND_OWNER'] + ' - ' + df_selector['BRAND_NAME'] 

selection = st.selectbox(
    label="",
    options=df_selector['concat'],
    index=None,
    format_func=lambda x: capwords(x),
    placeholder="Select or search for a product..."
)

st.divider()

if selection == None:
    st.text("No product selected.")
else:
    with st.spinner('Getting details on product...'):

        df_selection = df_selector[df_selector['concat'] == selection]

        brand_owner = df_selection['BRAND_OWNER'].iloc[0]
        brand_name = df_selection['BRAND_NAME'].iloc[0]
        image_search_term = brand_name + " product photo transparent"
        url = bing_image_urls(image_search_term, limit=1)

        detail_query = f"""
        SELECT * FROM BRANDED_FOOD
            WHERE BRANDED_FOOD.BRAND_OWNER = $${brand_owner}$$ AND
            BRANDED_FOOD.BRAND_NAME = $${brand_name}$$ AND
            INGREDIENTS IS NOT NULL AND
            GTIN_UPC IS NOT NULL AND
            SERVING_SIZE IS NOT NULL AND
            SERVING_SIZE_UNIT IS NOT NULL AND
            BRANDED_FOOD_CATEGORY IS NOT NULL AND
            PACKAGE_WEIGHT IS NOT NULL
            LIMIT 1
        """

        df_detail = conn.query(detail_query, ttl=600)

        detail_dict = df_detail.loc[0].to_dict()

        st.write("#")

        st.image(url,
                caption="Image search provided by Microsoft Bing")

        st.markdown(f"""

        ## {detail_dict["BRAND_NAME"]} 

        {detail_dict["BRAND_OWNER"]}

        **Category:** {detail_dict["BRANDED_FOOD_CATEGORY"]} 

        **Serving size:** {detail_dict["SERVING_SIZE"]} {detail_dict["SERVING_SIZE_UNIT"]} 

        **Package weight:** {detail_dict["PACKAGE_WEIGHT"]}

        ##

        {detail_dict["SHORT_DESCRIPTION"]}

        **Ingredients:** {detail_dict["INGREDIENTS"]}

        ##

        **FDC_ID:** {detail_dict["FDC_ID"]}

        Data provided by {detail_dict["DATA_SOURCE"]} as of {detail_dict["AVAILABLE_DATE"]} (Last modified {detail_dict["MODIFIED_DATE"]})

        """
        )