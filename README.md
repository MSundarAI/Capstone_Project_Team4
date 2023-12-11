# Welcome to CA Collaboration
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://team-ca-collab.streamlit.app/)

## Getting Started Guide

#### Clone Repository

To get a copy of our project running on your local machine, simply run the git clone command

```
git clone https://github.com/MSundarAI/Capstone_Project_Team4.git
cd Part2
```

#### Install Requirements

Before trying to run anything be sure to run requirements.txt and install all dependencies

```
pip install -r requirements.txt
```

#### The Data and API services 
For part 1 and part 2 there is intermediate csv files that will help with running the notebooks. However, there is still some situations where API access is needed

The 4 APIs we utilized are Spotify API, Billboard API, ChatGPT 3.5. And HuggingFace. Spotify API, Billboard API and HuggingFace are free. 
Spotify API requires your own client_ID and client_secret applied to run the API. Both Spotify API and Billboard API have specific frequency and request limits due to the nature of the free offering. We did need to pay for ChatGPT 3.5 with API key.

Spotify API: https://developer.spotify.com/documentation/web-api
Billboard API: https://github.com/guoguo12/billboard-charts

### Get an OpenAI API key

To run the streamlit app, you can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

#### Run the App

To run our version of the Streamlit app, click [here](https://team-ca-collab.streamlit.app/)

If you want to run your own local version, run command

```
streamlit run music_collab.py
```

And if you want to deploy your own version, follow these [instructions](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)


###Run Intermediate Notebooks

You can go through folders Part1 and Part2 and look under Notebooks to find Juypter notebook files to run. As mentioned earlier, you would need api keys for Spotify, Billboard and ChatGPT to run these notebooks successfully 