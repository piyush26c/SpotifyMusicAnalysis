# %%
import config as c
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

df = pd.read_csv('spotifyFinal.csv')
#st.title("Genre-wise Popularity Over Years")
selected_genre = st.sidebar.multiselect("Select Genre", df['Genre'].unique())
filtered_df = df[df['Genre'].isin(selected_genre)]
genre_year_popularity = filtered_df.groupby(['Genre', 'Year']).agg({'Popularity': 'mean'}).reset_index()
fig = px.line(genre_year_popularity, x='Year', y='Popularity', color='Genre', markers=True, title='Genre-wise Popularity Over Years')
fig.update_layout(xaxis_title='Release Years', yaxis_title='Average Popularity')
st.plotly_chart(fig)


selected_year = st.sidebar.selectbox('Select Year', sorted(df['Year'].unique()))
yeardf = df[df['Year'] == selected_year]
#artist_popularity = yeardf.groupby('Artist')['Popularity'].mean().sort_values(ascending=False)
artist_popularity = yeardf.groupby(['TrackName']).agg({'Popularity': 'mean'}).sort_values(by='Popularity',ascending=False).reset_index()
artist_popularity = artist_popularity[:10]
artist_popularity = pd.merge(artist_popularity, df[['TrackName','Popularity', 'Artist']], on=['TrackName','Popularity'], how='left')
artist_popularity = artist_popularity.drop_duplicates(subset=['TrackName', 'Popularity', 'Artist'])
artist_popularity = artist_popularity.groupby(['TrackName', 'Popularity'])['Artist'].agg(', '.join).reset_index()
custom_colors = ["red", "green", "blue", "goldenrod", "magenta", "cyan", "purple", "orange", "pink", "brown"]
#custom_colors = ["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a", "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6"]
barfig = px.bar(artist_popularity, x=artist_popularity['Popularity'], y=artist_popularity['TrackName'], title=f'Top 10 Track Name in {selected_year}', labels={'Popularity': 'Average Popularity'},orientation='h',hover_data=['Artist','Popularity'],color_discrete_sequence=custom_colors)
barfig.update_layout(yaxis_categoryorder='total ascending')
st.plotly_chart(barfig)