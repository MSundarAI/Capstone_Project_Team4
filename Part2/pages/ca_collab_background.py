import streamlit as st
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

st.set_page_config(page_title="background", page_icon="🎹", layout="wide")
st.image('./Part2/images/logo.png', width=100,caption = None)



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
    return plt.show()

def chart_aafi(df, artist, color):
  df_artist = df[df['artist'].str.contains(artist, na=False)]
  return chart_afi(df_chart = df_artist, color_chart=color, artist_name = artist)


st.title("Audio Features Analysis")

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
st.pyplot(fig)