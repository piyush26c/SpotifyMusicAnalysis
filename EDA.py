import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

main_dataset = "songs_dataset2.csv"
eda_dataset = "eda_dataset.csv"
genre_dataset = "Genre_Analysis.csv"
Artists_dataset = "Artists_Analysis.csv"

df = pd.read_csv(main_dataset)
df = df.drop(columns=['Unnamed: 0'])
df_eda = pd.read_csv(eda_dataset)
df_eda = df_eda.drop(columns=['Unnamed: 0'])
df_genre = pd.read_csv(genre_dataset)
df_genre = df_genre.drop(columns=['Unnamed: 0'])
df_genre = df_genre.sort_values(by='track_count', ascending=False)
df_artists = pd.read_csv(Artists_dataset)
df_artists = df_artists.drop(columns=['Unnamed: 0'])
df_artists = df_artists.sort_values(by='track_count', ascending=False)

st.set_page_config(
    page_title = "Vizionary's Beats from Bytes.",
    page_icon = "Active",
    layout = "wide",
)

# eda_type = st.radio(
#     "Select the EDA dataset",
#     ["Complete", "Genre", "Artist"], horizontal=True)

st.title("EDA for top songs given by Spotify for years 2000-22")

genre_list = df_genre["genre"].values.tolist()

artist_list = df_artists["artist"].values.tolist()

columns_list = ['track_popularity', 'track_duration','danceability','energy','loudness', 'speechiness',	'acousticness',	'instrumentalness',	'liveness',	'valence',	'tempo']
# with st.sidebar:
#     eda_type = st.radio(
#     "Select the EDA dataset",
#     ["Complete", "Genre", "Artist"], horizontal=True)
#     if eda_type == "Complete":
#         st.write("Select the year range")
#         #create a slider to hold user scores
#         year_range = st.slider(label = "Choose the range:",
#                                     min_value = 2000,
#                                     max_value = 2022,
#                                     value = (2000,2022))

#         columns_selected = st.multiselect('Choose Columns for Correlation:',
#                                                 columns_list, columns_list)
#         compare_top_songs_feature = st.selectbox('Choose a feature to compare top songs year by year',
#             columns_list, 3)                                                        

#         # #create a multiselect widget to display genre
#         # new_genre_list = st.multiselect('Choose Genres:',
#         #                                         genre_list)
#         # #create a selectbox option that holds all unique years
#         # artist = st.selectbox('Choose an Artist',
#         #     artist_list)
#     elif eda_type == "Genre":
#         new_genre_list = st.multiselect('Choose Genres:',
#                                                 genre_list)
#     else:
#         artist = st.selectbox('Choose an Artist',
#             artist_list)


col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df.index))
col2.metric("Total Genres", len(df_genre.index))
col3.metric("Total Artists", len(df_artists.index))

def getCorr(columns):
  if columns:return df_eda[columns].corr()
  else: return df_eda.corr()

# # def buildCorrHeatMap(columns=None):
# #   corr = getCorr(columns)
# #   sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")

# col1, col2 = st.columns([2,3])
# with col1:
#     st.write("""#### Correlation of track popularity with track features """)
#     fig, ax = plt.subplots()
#     corr = getCorr(columns_selected)
#     sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
#     st.write(fig)


# with col2:
#     st.write("""#### Popular songs year by year """)
#     rating_count_year = df[df['top_year'].between(*year_range)]\
#     .groupby('top_year')['track_popularity', 'track'].max()
#     rating_count_year = rating_count_year.reset_index()
#     figpx = px.line(rating_count_year, x = 'top_year', y = 'track_popularity', hover_data={'track':True})
#     figpx.update_traces(mode="markers+lines")
#     st.plotly_chart(figpx)

# col1, col2 = st.columns([2,3])
# with col1:
#     st.write("""#### Popular songs year by year """)
#     rating_count_year = df[df['top_year'].between(*year_range)]\
#     .groupby('top_year').max()
#     rating_count_year = rating_count_year.reset_index()
#     figpx = px.line(rating_count_year, x = 'top_year', y = compare_top_songs_feature, hover_data={'track':True})
#     figpx.update_traces(mode="markers+lines")
#     st.plotly_chart(figpx)


# with col2:
#     st.write("""#### Popular songs year by year """)
#     rating_count_year = df[df['top_year'].between(*year_range)]\
#     .groupby('top_year').max()
#     rating_count_year = rating_count_year.reset_index()
#     figpx = px.line(rating_count_year, x = 'top_year', y = 'track_popularity', hover_data={'track':True})
#     figpx.update_traces(mode="markers+lines")
#     st.plotly_chart(figpx)

col1, col2 = st.columns([1,4])

with col1:
    st.write("""#### """)
    year_range = st.slider(label = "Choose the range:",
                                    min_value = 2000,
                                    max_value = 2022,
                                    value = (2000,2022))

with col2:
    st.write("""#### Popular songs year by year """)
    rating_count_year = df[df['top_year'].between(*year_range)]\
    .groupby('top_year')['track_popularity', 'track'].max()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'top_year', y = 'track_popularity', hover_data={'track':True})
    figpx.update_traces(mode="markers+lines")
    st.plotly_chart(figpx)

col1, col2 = st.columns([1,4])

with col1:
    st.write("""#### """)
    compare_top_songs_feature = st.selectbox('Choose a feature to compare top songs year by year',
            columns_list, 3) 

with col2:
    st.write("""#### Track Feature year by year """)
    rating_count_year = df[df['top_year'].between(*year_range)]\
    .groupby('top_year').max()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'top_year', y = compare_top_songs_feature, hover_data={'track':True})
    figpx.update_traces(mode="markers+lines")
    st.plotly_chart(figpx)

col1, col2 = st.columns([1,4])

with col1:
    st.write("""#### """)
    genre_selected = st.selectbox('Choose Genres:', genre_list,0)

with col2:
    # print(genre_selected)
    df_genre_selected = df_genre[df_genre["genre"] == str(genre_selected)]
    # print(df_genre_selected)
    ccol1, ccol2, ccol3 = st.columns(3)
    ccol1.metric("Selected Genre", df_genre_selected["genre"].values[0])
    ccol2.metric("Total Songs with this genre", df_genre_selected.track_count.values[0])
    ccol3.metric("Average Track Popularity", "{:.2f}".format(df_genre_selected["track_popularity"].values[0]))

    col4, col5, col6, col7 = st.columns(4)
    col4.metric("Danceability",  "{:.2f}".format(df_genre_selected["danceability"].values[0]))
    col5.metric("Energy",  "{:.2f}".format(df_genre_selected["energy"].values[0]))
    col6.metric("Instrumentalness",  "{:.2f}".format(df_genre_selected["instrumentalness"].values[0]))
    col7.metric("Liveness",  "{:.2f}".format(df_genre_selected["liveness"].values[0]))

    col8, col9, col10, col11 = st.columns(4)
    col8.metric("Speechiness", "{:.2f}".format(df_genre_selected["speechiness"].values[0]))
    col9.metric("Loudness", "{:.2f}".format(df_genre_selected["loudness"].values[0]))
    col10.metric("Tempo", "{:.2f}".format(df_genre_selected["tempo"].values[0]))
    col11.metric("Valence", "{:.2f}".format(df_genre_selected["valence"].values[0]))

col1, col2 = st.columns([2,2])
with col1:
    st.write("""#### Top 10 genres with most songs """)
    figpx = px.bar(df_genre[:10], x = 'genre', y = 'track_count')
    st.plotly_chart(figpx)

with col2:
    st.write("""#### Top 10 Artists with most songs """)
    figpx = px.bar(df_artists[:10], x = 'artist', y = 'track_count')
    st.plotly_chart(figpx)


col1, col2 = st.columns([1,4])

with col1:
    st.write("""#### """)
    artist = st.selectbox('Choose an Artist',artist_list, 0)

with col2:
    df_artist_selected = df_artists[df_artists["artist"] == str(artist)]
    ccol1, ccol2, ccol3 = st.columns(3)
    ccol1.metric("Selected Artist", df_artist_selected["artist"].values[0])
    ccol2.metric("Total Songs by this artist", df_artist_selected.track_count.values[0])
    ccol3.metric("Average Track Popularity", "{:.2f}".format(df_artist_selected["track_popularity"].values[0]))

    col4, col5, col6, col7 = st.columns(4)
    col4.metric("Danceability",  "{:.2f}".format(df_artist_selected["danceability"].values[0]))
    col5.metric("Energy",  "{:.2f}".format(df_artist_selected["energy"].values[0]))
    col6.metric("Instrumentalness",  "{:.2f}".format(df_artist_selected["instrumentalness"].values[0]))
    col7.metric("Liveness",  "{:.2f}".format(df_artist_selected["liveness"].values[0]))

    col8, col9, col10, col11 = st.columns(4)
    col8.metric("Speechiness", "{:.2f}".format(df_artist_selected["speechiness"].values[0]))
    col9.metric("Loudness", "{:.2f}".format(df_artist_selected["loudness"].values[0]))
    col10.metric("Tempo", "{:.2f}".format(df_artist_selected["tempo"].values[0]))
    col11.metric("Valence", "{:.2f}".format(df_artist_selected["valence"].values[0]))


df_eda_top10Tracks = df_eda.sort_values(by='track_popularity', ascending=False)
fig = px.parallel_coordinates(df_eda_top10Tracks[:10],
                                dimensions=['danceability','energy','loudness', 'speechiness',	'acousticness',	'instrumentalness',	'liveness',	'valence',	'tempo'],
                                width=1200, height=600)
st.plotly_chart(fig)


col1, col2 = st.columns([1,4])

with col1:
    st.write("""#### """)
    columns_selected = st.multiselect('Choose Columns for Correlation:',
                                               columns_list, columns_list)

with col2:
    st.write("""#### Correlation of track popularity with track features """)
    fig, ax = plt.subplots()
    corr = getCorr(columns_selected)
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.write(fig)