import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import json
from plotly.subplots import make_subplots

st.set_page_config(
        page_title = "Vizionary's Beats from Bytes.",
        page_icon = "Active",
        layout = "wide",
        initial_sidebar_state='expanded'
    )

tab1, tab2, tab3, tab4 = st.tabs(["EDA", "Artists Collaboration", "Region Wise Song Popularity", "Genre wise popularity over Years"])

with tab1:
    # st.header("EDA")
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

    st.title("EDA for top songs given by Spotify for years 2000-22")

    genre_list = df_genre["genre"].values.tolist()

    artist_list = df_artists["artist"].values.tolist()

    columns_list = ['track_popularity', 'track_duration','danceability','energy','loudness', 'speechiness',	'acousticness',	'instrumentalness',	'liveness',	'valence',	'tempo']


    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df.index))
    col2.metric("Total Genres", len(df_genre.index))
    col3.metric("Total Artists", len(df_artists.index))

    def getCorr(columns):
        if columns:return df_eda[columns].corr()
        else: return df_eda.corr()

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
        figpx.update_layout(xaxis_title='Year', yaxis_title='Track Popularity')
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
        figpx.update_layout(xaxis_title='Year', yaxis_title=str(compare_top_songs_feature).capitalize())
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
        figpx.update_layout(xaxis_title='Genre', yaxis_title='Number of Tracks')
        st.plotly_chart(figpx)

    with col2:
        st.write("""#### Top 10 Artists with most songs """)
        figpx = px.bar(df_artists[:10], x = 'artist', y = 'track_count')
        figpx.update_layout(xaxis_title='Artist', yaxis_title='Number of Tracks')
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


    with st.container():
        st.write("""#### Parallel Coordinate Plot for the top 10 Songs""")
        df_eda_top10Tracks = df_eda.sort_values(by='track_popularity', ascending=False)

        fig2 = go.Figure(data=
        go.Parcoords(
            dimensions = list([
                dict(label = 'Danceability', values = df_eda_top10Tracks[:10]['danceability']),
                dict(label = 'Energy', values = df_eda_top10Tracks[:10]['energy']),
                dict(label = 'Loudness', values = df_eda_top10Tracks[:10]['loudness']),
                dict(label = 'Speechiness', values = df_eda_top10Tracks[:10]['speechiness']),
                dict(label = 'Acousticness', values = df_eda_top10Tracks[:10]['acousticness']),
                dict(label = 'Instrumentalness', values = df_eda_top10Tracks[:10]['instrumentalness']),
                dict(label = 'Liveness', values = df_eda_top10Tracks[:10]['liveness']),
                dict(label = 'Valence', values = df_eda_top10Tracks[:10]['valence']),
                dict(label = 'Tempo', values = df_eda_top10Tracks[:10]['tempo'])
            ]),
            unselected = dict(line = dict(color = 'green', opacity = 0.5))
            )
        )

        fig2.update_layout(
            plot_bgcolor = 'white',
            paper_bgcolor = 'white',
            width = 1200,
            height = 800
        )
        st.plotly_chart(fig2)

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

with tab2:
    st.header("Artists Collaboration")
    file = open('radarchart.json')

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    data = json.load(file)
    dropdown = tuple(data.keys())
    selected_artist_name = st.selectbox('Artist', dropdown, 6) 

    if len(data[selected_artist_name].keys()) > 0:
        # Sample data (replace this with your actual data)
        data = {
            'artistname': [x for x in sorted(data[selected_artist_name].keys())],
            'count': [data[selected_artist_name][x] for x in sorted(data[selected_artist_name].keys())],
        }

        df = pd.DataFrame(data)
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=df['count'],
            theta=df['artistname'],
            customdata=df[['count', 'artistname']],
            hovertemplate="Number of tracks: %{customdata[0]}<br>Artist Name: %{customdata[1]}<extra></extra>",
            fill='toself',
            fillcolor='rgba(173, 216, 230, 0.5)',  # Light blue fill color
            line=dict(color='rgb(30, 144, 255)', width=2),  # Dodger blue line color
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    showgrid=True,
                    tickmode='array',  # Use 'array' for manual tick placement
                    tickvals=list(range(0, max(df['count']))),  # Set tick values to whole numbers
                ),
                radialaxis_title_font=dict(size=50),  # Increase font size of theta labels
            ),
            showlegend=False,
            height=700,
            width=700,
        )

        # Display the radar chart
        st.plotly_chart(fig)
    else:
        st.text("No collaborations available with other artists.")


    file.close()

with tab3:
    result_df = pd.read_csv('top_songs_by_country.csv')
    result_df['Genres'] = result_df['Genres'].str.split(', ')

    df_bangladesh = result_df[result_df['country'] == 'Bangladesh']
    df_india = result_df[result_df['country'] == 'India']
    df_usa = result_df[result_df['country'] == 'Usa']

    # Get unique countries
    unique_countries = result_df['country'].unique()

    # # Get top 10 genres for each country
    # top_genres_bangladesh = df_bangladesh['Genres'].explode().value_counts().nlargest(10).index
    # top_genres_usa = df_usa['Genres'].explode().value_counts().nlargest(10).index
    # top_genres_india = df_india['Genres'].explode().value_counts().nlargest(10).index


    # # Create subplot
    # fig = go.Figure()

    # # Add initial bar chart
    # fig.add_trace(go.Bar(x=top_genres_bangladesh,
    #                     y=df_bangladesh['Genres'].explode().value_counts().nlargest(10).values,
    #                     name='Bangladesh',
    #                     marker_color='skyblue'))

    # # Add dropdown filter for country
    # country_dropdown_options = [{'label': country, 'method': 'update',
    #                             'args': [{'x': [top_genres_bangladesh if country == 'Bangladesh' else top_genres_usa if country == 'USA' else top_genres_india  ],
    #                                     'y': [df_bangladesh['Genres'].explode().value_counts().nlargest(10).values if country == 'Bangladesh' else df_usa['Genres'].explode().value_counts().nlargest(10).values if country == 'USA' else df_india['Genres'].explode().value_counts().nlargest(10).values ],
    #                                     'marker_color': 'skyblue'},
    #                                     {'title.text': f'Top 10 Genre Distribution for {country}'}]} for country in unique_countries]

    # # Update layout with dropdown
    # fig.update_layout(
    #     updatemenus=[
    #         dict(type='dropdown', x=0.35, y=1.28, buttons=country_dropdown_options, showactive=False)
    #     ],
    #     title_text='Top 10 Genre Distribution',
    #     xaxis_title='Genres',
    #     yaxis_title='Count',
    #     showlegend=False,
    #     width=1200,  # Adjust the width as needed
    #     height=500,  # Adjust the height as needed
    # )

    # Show the plot
    # fig.show()
    # st.write(fig)

    # result_df
    selected_country = st.selectbox("Select Country", unique_countries, 1)
    # selected_country
    df_selected = result_df[result_df['country'] == selected_country]
    # df_selected
    df_top_genres_selected = df_selected['Genres'].explode().value_counts().nlargest(10).index
    # df_top_genres_selected
    df_top_genres_selected_count = df_selected['Genres'].explode().value_counts().nlargest(10).values
    # df_top_genres_selected_count
    fig12 = px.bar(x=df_top_genres_selected.tolist(), y=df_top_genres_selected_count.tolist())
    fig12.update_layout(xaxis_title='Genres', yaxis_title='Count')
    st.plotly_chart(fig12)

with tab4:
    st.header("Genre-wise Popularity Over Years")
    df = pd.read_csv('spotifyFinal.csv')
    #st.title("Genre-wise Popularity Over Years")
    selected_genre = st.multiselect("Select Genre", df['Genre'].unique(), ["pop"])
    filtered_df = df[df['Genre'].isin(selected_genre)]
    genre_year_popularity = filtered_df.groupby(['Genre', 'Year']).agg({'Popularity': 'mean'}).reset_index()
    fig = px.line(genre_year_popularity, x='Year', y='Popularity', color='Genre', markers=True)
    fig.update_layout(xaxis_title='Release Years', yaxis_title='Average Popularity')
    st.plotly_chart(fig)

    selected_year = st.selectbox('Select Year', sorted(df['Year'].unique()), 2)
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
