'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

# Import top locations:
locations_df = pd.read_csv("cache/top_locations_mappable.csv")

# Set up initial map:
map = folium.Map(location = CUSE, zoom_start = ZOOM)
locations_gdf = gpd.GeoDataFrame(locations_df, geometry = gpd.points_from_xy(x = locations_df["lon"], y = locations_df["lat"]))
locations_map = locations_gdf.explore(locations_gdf["amount"], cmap = "magma", m = map,
                                      vmin = VMIN, vmax = VMAX, marker_type = "circle_marker",
                                      marker_kwds= {"fillbool":True})

# Setting up streamlit:
st.title("Map of Top Locations for Parking Tickets")
sf.st_folium(locations_map, height = 500, width = 500)
