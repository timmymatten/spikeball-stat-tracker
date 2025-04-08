import streamlit as st
import time
import numpy as np
import pandas as pd
import json
from db import fetch_games

st.set_page_config(page_title="Past Games", page_icon="🕰️")

st.markdown("# Past Games")
st.sidebar.header("Games")
st.write(
    """
    Here we can take a look at past games and stats!
"""
)

# Load games from database
db_games = fetch_games()

if db_games:
    for game in db_games:
        game_id = game[0]
        game_date = game[1]
        team1_score = game[2]
        team2_score = game[3]
        game_data = json.loads(game[4])
        
        # Convert game data to DataFrame
        game_df = pd.DataFrame.from_dict(game_data, orient='index')
        
        # Display game information
        if team1_score > team2_score:
            st.subheader(f"Game {game_id} ({game_date}): Team 1 {team1_score} - {team2_score} Team 2")
        else:
            st.subheader(f"Game {game_id} ({game_date}): Team 2 {team2_score} - {team1_score} Team 1")
        
        # Display game stats
        game_df = game_df.applymap(lambda x: round(x) if isinstance(x, (int, float)) else x)
        st.dataframe(game_df)
        st.divider()
elif "all_games" in st.session_state and len(st.session_state["all_games"]) > 0:
    for i, game in enumerate(st.session_state["all_games"]):
        if st.session_state['Team 1_score'] > st.session_state['Team 2_score']:
            st.subheader(f"Game {i + 1}: T1 {st.session_state['Team 1_score']} - {st.session_state['Team 2_score']}")
        else:
            st.subheader(f"Game {i + 1}: T2 {st.session_state['Team 2_score']} - {st.session_state['Team 1_score']}")
        st.session_state['Team 1_score'] = 0
        st.session_state['Team 2_score'] = 0

        game =  game.applymap(lambda x: round(x) if isinstance(x, (int, float)) else x)
        st.dataframe(game)
else:
    st.warning("No games added yet!")



