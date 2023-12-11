import streamlit as st
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

st.set_page_config(page_title="background", page_icon="🎹", layout="wide")
st.image('./Part2/images/logo.png', width=100,caption = None)

st.markdown(

"""
# Project
>"Music is changing so quickly, and the landscape of the music industry itself is changing so quickly, that everything new, like Spotify, all feels to me a bit like a grand experiment
(Taylor Swift))"

The trend of collaboration in the music industry caught our eyes from **10%**-20%** around 3 decades ago almost tripling to approaching **30%+** of the top music charts nowadays. 
We randomly take the 2023/7/28 Billboard Top 100, there are 40 songs out of 100 songs are collaborations. The **40%** landmark signals loudly the new trend in the music industry. It motivates us to create a “Collab Index/Score” dashboard concept to analyze how the artist is popular for collab success and how inter-related they are to audio features

""")



def chart_afi(df_chart, color_chart, artist_name=None):
    df = df_chart[['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                   'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
                   'time_signature', 'valence']]
    n_cols = 5
    n_rows = (df.shape[1] + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 3))

    # Get a colormap
    cmap = plt.get_cmap(color_chart)

    # Create a normalized range of colors for each feature
    norm = mcolors.Normalize(vmin=0, vmax=df.shape[1])

    # Plotting data
    for i, (col, ax) in enumerate(zip(df.columns, axes.flatten())):
        # Choose a color from the colormap based on normalized value
        color = cmap(norm(i))

        if col == 'key':
            value_counts = df[col].value_counts().sort_index()
            ax.bar(x=value_counts.index, height=value_counts.values, alpha=0.7, color=color, edgecolor='black')
            ax.set_xticks(value_counts.index)
            ax.set_xticklabels(value_counts.index.astype(int))
        elif col == 'mode':
            value_counts = df[col].value_counts()
            ax.bar(x=value_counts.index, height=value_counts.values, alpha=0.7, color=color, edgecolor='black')
            ax.set_xticks([0, 1])
        else:
            ax.hist(df[col], bins=12, alpha=0.7, color=color, edgecolor='black')

        ax.set_title(col)
        ax.set_ylabel('Frequency')

    # Hide any unused axes
    for j in range(i+1, n_rows * n_cols):
        axes.flatten()[j].set_visible(False)

    title_font_size = 20  # Adjust the font size as needed
    if artist_name:
        fig.suptitle(f"Audio Features Index for {artist_name}", fontsize=title_font_size)
    else:
        fig.suptitle("Full Dataset Audio Features Index", fontsize=title_font_size)

    plt.tight_layout()
    return fig

def chart_aafi(df, artist, color):
  df_artist = df[df['artist'].str.contains(artist, na=False)]
  return chart_afi(df_chart = df_artist, color_chart=color, artist_name = artist)


st.title("Audio Features Analysis")
st.markdown(
"""
The following chart below is a dynamic bar plot of top artists and the result of their audio features. 
""")

file_path = './Part2/data/artistfeatures.csv'
df_ac = pd.read_csv(file_path)

# Extract unique artist names for the dropdown
artist_names = df_ac['artist'].unique()
default_artist = 'Justin Bieber'
if default_artist in artist_names:
    default_index = int(np.where(artist_names == default_artist)[0][0])
else:
    default_index = 0 
# dropdown
selected_artist = st.selectbox("Select an Artist", options=artist_names, index=default_index)

# display plot
fig = chart_aafi(df=df_ac, artist=selected_artist, color='magma')
st.pyplot(fig,clear_figure=True)


st.markdown(

"""
These features were collected from Spotify, for further explainability, see below for brief definitions:
- **acousticness**: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic..
- **danceability**: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
- **duration_ms**: The duration of the track in milliseconds.
- **energy**: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
- **instrumentalness**: Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
- **liveness**: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
- **loudness**: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.
- **tempo**: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
""")


st.title("Radar Chart of Audio Features Index")
st.markdown(

"""
We derived a collaboration index with our final dataset to understand how likely an artist will be successful if they collaborate with another artist.
We can see in the radar charts below. If the Weeknd and Ariana Grande collaborated, their chances of success on collaborating with each other would be high
and desirable 
"""
)
st.image('./Part2/images/first_radar.png',caption = None)

st.image('./Part2/images/second_radar.png',caption = None)

st.image('./Part2/images/third_radar.png',caption = None)