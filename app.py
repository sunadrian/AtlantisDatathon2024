import streamlit as st
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from csv_reader import load_dataset, calc_zipcode_stats, fiveclosest


DATASET_PATH = Path('PropertyAssessmentData.csv')

@st.cache_resource
def cache_variables():
    print("Loading Dataset into a dataframe")
    st.session_state.df = load_dataset(DATASET_PATH)
    st.session_state.zipcode_stats_dict = calc_zipcode_stats(st.session_state.df)

    st.session_state.zipcode_stats = pd.DataFrame.from_dict(
                                    st.session_state.zipcode_stats_dict, 
                                    orient='index')

    with open('ca_california_zip_codes_geo.min.json') as repsonse:
       st.session_state.geojson_data = json.load(repsonse)
    st.session_state.zipcode_stats.columns = ['Max Value', 'Min Value', 
                                               'Avg Value', 'ZipCode Lat', 'ZipCode Long']
    

def launch_gui(dataset_df, zipcode_stats, geojson_data):
    
    
    #Create title and interactive map
    with st.empty(): 
        title = st.title(":violet[Best Building Buyer] 💸", anchor=False)

    figure_container = st.empty()
    fig = px.choropleth_mapbox(zipcode_stats, geojson=geojson_data, color=zipcode_stats['Avg Value'],
                            locations=zipcode_stats.index, featureidkey="properties.ZCTA5CE10",
                            mapbox_style="carto-positron", hover_data=zipcode_stats.columns,
                            hover_name=zipcode_stats.index,
                            zoom=8, center={"lat": 33.710924, "lon": -117.791848},
                            opacity=0.5, color_continuous_scale="plasma",
                            labels={'Mean GDP':'Mean Total Assessed Value'})
    # Customize the layout
    fig.update_geos(fitbounds="locations",visible=False)
    figure_container.plotly_chart(fig)

    # Set up Search features and handle search
    with st.empty():
        search_zipcode = st.text_input("Search ZipCode", 
                                     placeholder="Enter a ZipCode to search for properties in desired location", 
                                     label_visibility="hidden").lower()
    with st.empty():
        max_budget = st.text_input("Max Budget", 
                                     placeholder="Enter a max budget (e.g 100000)", 
                                     label_visibility="hidden").lower()
    
    with st.empty():
        checkbox_value = st.checkbox(label="Toggle to Search for Outside budget", key="checkbox")
    
    search_button = st.button("Search")

    if search_button:
        if max_budget == '':
            max_budget = (2 ** 31)  - 1

        if search_zipcode.isdigit() is False:
            st.write("Invalid ZipCode, please enter a valid number")

        elif type(max_budget) is str and max_budget.isdigit() is False:
            st.write("Invalid Budget Value, please enter a value budget")

        else:
            # Continue with the searching feature
            search_zipcode = int(search_zipcode)
            max_budget = int(max_budget)
            if search_zipcode in zipcode_stats.index:
                res = fiveclosest(dataset_df, max_budget, search_zipcode, checkbox_value)
                for r in res:
                    st.text_area(f'Address: {r.address}:',value=f'Total Cost: ${r.totalcost}\nNumber of Rooms:{r.rooms}\nHas Fireplace: {r.fireplace}\nHas Security Alarms: {r.security}\nHas Sprinklers: {r.sprinklers}', 
                                 height=150, disabled=True)
                
                cur_row = zipcode_stats.loc[search_zipcode]
                new_lat = cur_row['ZipCode Lat']
                new_long = cur_row['ZipCode Long']
                fig.update_layout(mapbox_center={"lat": new_lat, "lon": new_long}, mapbox_zoom=13)
                figure_container.plotly_chart(fig)
            else:
                st.write("This ZipCode does not exist in our dataset, please try again.")


if __name__ == "__main__":
    # Load stuff from dataset and launch_gui
    cache_variables()
    launch_gui(st.session_state.df, st.session_state.zipcode_stats,
               st.session_state.geojson_data)

