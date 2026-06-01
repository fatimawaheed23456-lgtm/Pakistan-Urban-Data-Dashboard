import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Title
st.title("Pakistan Urban Data Dashboard")
st.write("Analysis by SAP ID: 70177415")

# 2. THE LOADING SECTION (Add your line here!)
try:
    # This is the specific line you asked about:
    gdf = gpd.read_file('gis_osm_pois_free_1.shp') 
    
    # We convert the map shapes into a table so we can make charts
    # We extract the X and Y coordinates to get Latitude and Longitude
    gdf['latitude'] = gdf.geometry.y
    gdf['longitude'] = gdf.geometry.x
    df = pd.DataFrame(gdf.drop(columns='geometry'))
    
    st.success("Successfully loaded Pakistan OSM data!")

    # 3. Create a Filter in the Sidebar
    # 'fclass' is the standard column name in OSM files for categories like 'hospital' or 'school'
    st.sidebar.header("Filter Options")
    if 'fclass' in df.columns:
        options = df['fclass'].unique()
        selected = st.sidebar.multiselect("Select Categories", options, default=options[:5])
        filtered_df = df[df['fclass'].isin(selected)]
    else:
        filtered_df = df

    # 4. Display the Visuals
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category Distribution")
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, y='fclass' if 'fclass' in df.columns else df.columns[0])
        st.pyplot(fig)

    with col2:
        st.subheader("Interactive Map")
        map_data = filtered_df[['latitude', 'longitude']].rename(columns={'latitude': 'lat', 'longitude': 'lon'})
        st.map(map_data)

except Exception as e:
    st.error(f"Error: {e}")
    st.info("Check if the folder is named 'pakistan' and contains the .shp file.")
    st.markdown("---")
st.subheader("Raw Data Preview")
st.write("This table shows the specific locations currently filtered on the map.")
st.dataframe(filtered_df[['name', 'fclass', 'latitude', 'longitude']].head(20))