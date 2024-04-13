import streamlit as st
from pathlib import Path
import streamlit as st
from csv_reader import load_dataset, calc_zipcode_stats

DATASET_PATH = Path('PropertyAssessmentData.csv')

@st.cache_resource
def cache_variables():
    print("Loading Dataset into a dataframe")
    st.session_state.df = load_dataset(DATASET_PATH)
    st.session_state.zipcode_stats = calc_zipcode_stats(st.session_state.df)

    

def launch_gui(dataset_df, zipcode_stats: dict):
    #Create title and search_box elements
    with st.empty(): 
        title = st.title(":violet[Temp Title]:sunglasses:", anchor=False)
    with st.empty():
        search_zipcode = st.text_input("Search ZipCode", 
                                     placeholder="Type in a Zipcode and click on search", 
                                     label_visibility="hidden").lower()
    search_button = st.button("Search")
    if search_button:
        if search_zipcode.isdigit() is False:
            st.write("Invalid ZipCode, please enter a valid number")
        else:
            # Continue with the searching feature
            search_zipcode = int(search_zipcode)
            if search_zipcode not in zipcode_stats:
                st.write("This ZipCode does not exist in our dataset, please try again.")
            else:
                st.write('It worked')

if __name__ == "__main__":
    # Load stuff from dataset and launch_gui
    cache_variables()
    launch_gui(st.session_state.df, st.session_state.zipcode_stats)

