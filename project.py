import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from plotnine import *

st.set_page_config(layout="wide")
st.title("Exploring weekly Top10 on Netflix")
#get the data and convert column headers to lower case
raw_data =pd.read_csv('data/all-weeks-global.csv',encoding='latin1')
lowercase = lambda x: str(x).lower()
raw_data.rename(lowercase, axis='columns', inplace=True)

#use cache to improve speed
@st.cache(allow_output_mutation=True)
#define all the functions we need to call
def category_data():
    data = raw_data.groupby(['category'])['weekly_hours_viewed'].sum().reset_index(name='hours_viewed')
    data['percentage'] = ((data['hours_viewed']/data['hours_viewed'].sum())*100).round(2)
    data['percentage'] = data['percentage'].astype(str) + ('%')
    return data

def title_data():
    data = raw_data.groupby(['show_title'])['weekly_hours_viewed'].sum().reset_index(name='weekly_hours_viewed')
    data = data.sort_values(by=['weekly_hours_viewed'],ascending=False).reset_index(drop=True)
    data['index'] = data.index
    return data

def tf_data():
    data = raw_data.groupby(['show_title'])['show_title'].count().reset_index(name='NumberOfAppearances')
    data = data.sort_values(by=['NumberOfAppearances'],ascending=False).reset_index(drop=True)
    data['index'] = data.index
    return data

def genre_filter():
    data = raw_data['genre'].unique()
    data = np.array(data)
    return data

def category_filter():
    data = raw_data['category'].unique()
    data = np.array(data)
    return data

def genrebyhr_data():
    data = raw_data.groupby(['genre'])['weekly_hours_viewed'].sum().reset_index(name='hours_viewed')
    return data

def filtered_dataset(filtered_data):
    data =pd.DataFrame(filtered_data)
    data = data.groupby(['show_title','genre','category'])['weekly_hours_viewed'].sum().reset_index(name='weekly_hours_viewed')
    data = data.sort_values(by=['weekly_hours_viewed'],ascending=False).reset_index(drop=True)
    data['index'] = data.index
    return data
#setting some altair sliders to bind to our visualisation for filtering
list_slider = alt.binding_range(min=10, max=50, step=1)
slider_selection = alt.selection_single(bind=list_slider, fields=['index'], name="cutoff",init={'index':26})
genre_slider = alt.binding_range(min=5, max=20, step=1)
genre_slider_selection = alt.selection_single(bind=genre_slider, fields=['index'], name="cutoff",init={'index':10})

#we create two tabs, one for overview and another to allow the user to make further filtering
tab1, tab2 = st.tabs(['Overview','Breakdown'])
#Define visuals for each tab
with tab1:
    tab1.markdown('**Most watched titles on Netflix**')
    #we layout everything using columns
    col1, col2, col3 = st.columns((1,1,1), gap='small')
    with col1:
         col1.markdown('comparing hours viewed for each category')
         base=alt.Chart(category_data()).encode(
            theta=alt.Theta(field="hours_viewed", type="quantitative", stack=True),
            color=alt.Color(field="category", type="nominal", legend=None),
            tooltip=['category', 'percentage',alt.Tooltip('hours_viewed',title='hours viewed',format=',')])
         pie = base.mark_arc(radius=100,innerRadius=50)
         pietext = base.mark_text(radius=145, size=10).encode(text="category:N")
         piepercent = base.mark_text(radius=120, size=10, dx=3, dy=10).encode(text="percentage:N")
         pieChart = pie+pietext+piepercent
         st.altair_chart(pieChart, use_container_width=True)
        
    with col2:
        col2.markdown('Comparing top 50 Titles by Hours Viewed')
        viewhours = alt.Chart(title_data()).transform_window(
            rank='rank(weekly_hours_viewed)',
            sort=[alt.SortField('weekly_hours_viewed', order='descending')]
            ).transform_filter(alt.datum.rank <= slider_selection.index
            ).mark_bar().encode(
            x=alt.X('show_title:N',sort='-y'),
            y=alt.Y('weekly_hours_viewed:Q'),
            tooltip=[alt.Tooltip('show_title',title='show title'),alt.Tooltip('weekly_hours_viewed',title='weekly hours viewed',format=',')],
            color=alt.Color('weekly_hours_viewed', legend=None)).add_selection(slider_selection)
        st.altair_chart(viewhours, use_container_width=True)
    with col3:
        col3.markdown('Comparing top 50 Titles by Number of Appearances in Top10 List')
        appearance = alt.Chart(tf_data()).transform_window(
            rank='rank(NumberOfAppearances)',
            sort=[alt.SortField('NumberOfAppearances', order='descending')]
            ).transform_filter(alt.datum.rank <= slider_selection.index
            ).mark_bar().encode(
            x=alt.X('show_title:N',sort='-y'),
            y=alt.Y('NumberOfAppearances:Q'),
            tooltip=[alt.Tooltip('show_title',title='show title'),alt.Tooltip('NumberOfAppearances',title='appearances in top10')],
            color=alt.Color('NumberOfAppearances', legend=None)).add_selection(slider_selection)
        st.altair_chart(appearance, use_container_width=True)
    
    col0, col4 = st.columns((0.2,3.8), gap='small')
    with col4:
        col4.markdown('Comparing the top 20 most popular Genres by hours viewed')
        genreChart = alt.Chart(genrebyhr_data()).transform_window(
            rank='rank(hours_viewed)',
            sort=[alt.SortField('hours_viewed', order='descending')]
            ).transform_filter(alt.datum.rank <= genre_slider_selection.index
            ).mark_bar().encode(
            x=alt.X('genre:N',sort='-y'),
            y=alt.Y('hours_viewed:Q'),
            tooltip=['genre',alt.Tooltip('hours_viewed',title='weekly hours viewed',format=',')],
            color=alt.Color('genre')).add_selection(genre_slider_selection)
        st.altair_chart(genreChart, use_container_width=True)

with tab2:
    filtered_data = raw_data
    col5, col6, col7 = st.columns((1,2,2), gap='small')
    with col5:
        col5.markdown('**Filter to see more detail**')
        selected_genre = st.multiselect("Select Mutiple genres to see your best movies", genre_filter())
        selected_category = st.multiselect("Filter by Mutiple categories", category_filter())
        if selected_genre:
            filtered_data = filtered_data[filtered_data['genre'].isin(selected_genre)]
           
        if selected_category:
            filtered_data = filtered_data[filtered_data['category'].isin(selected_category)]

    with col6:
        col6.markdown('**Genre of filtered top 50 movies by hours viewed**')
        chartbyGenre = alt.Chart(filtered_dataset(filtered_data)).transform_window(
            rank='rank(weekly_hours_viewed)',
            sort=[alt.SortField('weekly_hours_viewed', order='descending')]
            ).transform_filter(alt.datum.rank <= slider_selection.index
            ).mark_bar().encode(
            x=alt.X('show_title:N',sort='-y', axis=alt.Axis()),
            y=alt.Y('weekly_hours_viewed:Q'),
            tooltip=[alt.Tooltip('show_title',title='show title'),
            alt.Tooltip('weekly_hours_viewed',title='weekly hours viewed',format=','),'genre'],
            color=alt.Color('genre')).add_selection(slider_selection)
        st.altair_chart(chartbyGenre, use_container_width=True)

    with col7:
        col7.markdown('**Category of filtered top 50 movies by hours viewed**')
        chartbycategory = alt.Chart(filtered_dataset(filtered_data)).transform_window(
            rank='rank(weekly_hours_viewed)',
            sort=[alt.SortField('weekly_hours_viewed', order='descending')]
            ).transform_filter(alt.datum.rank <= slider_selection.index
            ).mark_bar().encode(
            x=alt.X('show_title:N',sort='-y'),
            y=alt.Y('weekly_hours_viewed:Q'),
            tooltip=[alt.Tooltip('show_title',title='show title'),
            alt.Tooltip('weekly_hours_viewed',title='weekly hours viewed',format=','),'category'],
            color=alt.Color('category')).add_selection(slider_selection)
        st.altair_chart(chartbycategory, use_container_width=True)
    
    col8, col9 = st.columns((1,4), gap='small')

    with col9:
        col9.markdown('**See full list for your selection ordered descending by hours viewed**')
        show = st.checkbox("show or hide list", value=False, key="show")
        data = filtered_dataset(filtered_data)
        data = data.drop(['index'], axis=1)
        data.loc[:, "weekly_hours_viewed"] = data['weekly_hours_viewed'].map('{:,d}'.format)
        if show:
            st.dataframe(data, use_container_width=True)