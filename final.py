import streamlit as st
import plotly.graph_objects as go
import pandas as pd
# import plost
import json

file = open('radarchart.json')
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Data Visualization Course `project`')

st.sidebar.subheader('Analyze the artist collaboration')
data = json.load(file)
dropdown = tuple(data.keys())
selected_artist_name = st.sidebar.selectbox('Artist', dropdown) 

if len(data[selected_artist_name].keys()) > 0:
    # Sample data (replace this with your actual data)
    data = {
        'artistname': [x for x in sorted(data[selected_artist_name].keys())],
        'count': [data[selected_artist_name][x] for x in sorted(data[selected_artist_name].keys())],
    }

    df = pd.DataFrame(data)

    # Streamlit app
    st.title("Customized Radar Chart in Streamlit")

    # Display the sample data
    # st.write("Sample Data:")
    # st.write(df)

    # Create radar chart using Plotly Go with custom labels
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
                # tickfont=dict(size=50),
                # range=[0, max(df['count']) + 1]  # Adjust the range if needed
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