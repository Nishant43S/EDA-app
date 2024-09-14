### importing libraries  ###
import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
import base64
from streamlit_option_menu import option_menu
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.colored_header import colored_header
import seaborn as sbn
import random


######  functions

@st.cache_data
def insert_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


def read_csv(file_path):
    return pd.read_csv(file_path)


def File_name(file)->str:
    if file is not None:
        return file.name[:-4]

# Function to generate download link for HTML file
def generate_download_link(html_content, filename):
    b64 = base64.b64encode(html_content.encode()).decode()  # Encode the HTML to base64
    href = f"""
            <a href="data:file/html;base64,{b64}" style="text-decoration: none;" download="{filename}">
                <button class="neon-button">Download report</button>
            </a>
            """
    return href


def Eda_data(file):
    
    if file is not None:
        # Read the CSV file
        df = read_csv(file)
        try:
            colored_header(
                label="Dataset Explorer 📑",
                description="Explore your dataset",
                color_name="violet-70"
            )
            Data_Explorer = dataframe_explorer(df)
            st.dataframe(Data_Explorer,use_container_width=True)
            Download_df = Data_Explorer.to_csv().encode("utf-8")
            st.download_button(
                label="Download filtered file",data=Download_df,
                file_name=f"{File_name(file)}.csv",
                mime="text/csv"
            )
            st.text("")
        except Exception as err:
            st.warning(f"Error...\n\n",err)
        

        try:
            ###3 Generate the profile report
            profile = ProfileReport(df, explorative=True)
            if st.button(label="Generate report"):
                colored_header(
                    label=f"EDA Report📈 - {File_name(file)}",
                    description="Detailed analysis of data",
                    color_name="violet-70"
                )

                with st.spinner("Generating profile report..."):
                    st_profile_report(profile)
                
                ###%%# Download button
                    st.text("")
                    profile_html = profile.to_html()
                    download_link = generate_download_link(profile_html, f"{File_name(file)}.html")
                    st.markdown(download_link, unsafe_allow_html=True)
                    st.text("")
                    st.text("")
                    st.text("")
                    st.markdown("<p style='text-align: center;'>Created by Nishant Maity</p>",unsafe_allow_html=True)

        except Exception as er:
            st.warning(f"Error...\n\n",er)

        
    else:
        st.info("Upload csv file")
        def demo_data_report():  ############# generating demo reports
            try:
                demo_datasets = ["iris","penguins","planets","healthexp","titanic"]
                random_dataset = random.choice(demo_datasets)
                random_df = sbn.load_dataset(random_dataset)
                
                demo_profile_report = ProfileReport(random_df,explorative=True)
                with st.spinner("Generating demo report..."):
                    colored_header(
                        label=f"Demo Report📈 - {random_dataset}",
                        description="Detailed analysis of data",
                        color_name="violet-70"
                    )
                    st_profile_report(demo_profile_report)
                    st.text("")
                    st.text("")
                    st.text("")
                    st.markdown("<p style='text-align: center;'>Created by Nishant Maity</p>",unsafe_allow_html=True)
            except Exception as err:
                st.error(f"Error...\n\n{err}")

        
        if st.button("Generate Demo report"):
            
            if __name__=="__main__":
                demo_data_report()



st.set_page_config(  ##### settig page layout
    page_title="DataScience App",
    page_icon="📑",
    layout="wide" ,
    initial_sidebar_state="collapsed",
)

App_sidebar = st.sidebar

with App_sidebar:

    st.header("Data Science📑 App")
    st.text("")
    st.text("")
    st.text("")
    ### menu
    Main_menu = option_menu(
        menu_title="",
        options=("Dataset EDA","About App"),
        icons=["file-earmark-bar-graph","person-circle"]
    )

    ######  file uploadar

    uploaded_file = st.file_uploader(
        label="Upload CSV file", 
        type=["csv"]
    )
    
#### eda report of dataset
if Main_menu == "Dataset EDA":

    col1 , app_section , col2 = st.columns([1,8,1],gap="small")
    with col1:
        st.text("")
    with col2:
        st.text("")
    
    with app_section:
        st.header("Dataset EDA")
        if __name__=="__main__":
            Eda_data(uploaded_file)

        
    
if Main_menu == "About App":
    about_col1 , about_section , about_col2 = st.columns([1,8,1],gap="small")
    with about_col1:
        st.text("")
    with about_col2:
        st.text("")
    with about_section:
        @st.cache_data
        def insert_html(html_file):
            with open(html_file) as f:
                st.markdown(f.read(),unsafe_allow_html=True)

        if __name__=="__main__":
            insert_html("about_app.html")


    
    
if __name__=="__main__":
    insert_css("external_file.css")
