import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# This represents the intial state of the game table
game_cols =  {
            "Cut": [],
            "Drop": [],
            "Rev": [],
            "High": [],
            "Side": [],
            "Rim": [],
            '✅ set': [], 
            '❌ set': [], 
            '✅ hit': [], 
            '❌ hit': []
}

# initiate the game table in session state
if "game_df" not in st.session_state:
        st.session_state["game_df"] = pd.DataFrame(game_cols)   

if "player_table" not in st.session_state:
        st.session_state["player_table"] = pd.DataFrame(game_cols)

# adds the player row with the given name to the given game table
@st.cache_data
def set_game_table_name(df, name):
    if name not in df.index:
        new_row = pd.DataFrame({
            "Cut": [0],
            "Drop": [0],
            "Rev": [0],
            "High": [0],
            "Side": [0],
            "Rim": [0],
            '✅ set': [0], 
            '❌ set': [0], 
            '✅ hit': [0], 
            '❌ hit': [0]}, 
            index=[name])
        df = pd.concat([df, new_row])
    return df

def scorebug(team_name):
    score_key = f"{team_name}_score"
    cols = st.columns(3)

    if score_key not in st.session_state:
        st.session_state[score_key] = 0
    
    cols[0].header(team_name)
    
    with cols[1]:
        if st.button("SCORE", type="primary", key=f"{team_name}_score_button"):
            st.session_state[score_key] += 1
    
    cols[2].write(st.session_state[score_key])

# sets the element in the given row and column to x in the given table
@st.cache_data
def set_element_df(df, column, row, x):
    df.at[row, column] = x

@st.cache_data
def add_element_df(df, column, row):
    df.at[row, column] += 1

# set page configuration
st.set_page_config(page_title="Add Game", page_icon="➕")

cols = st.columns(4)

# Date
cols[0].date_input("Game Date", format="MM/DD/YYYY")

# Function to handle player stats 
def player_stats(player_name, player_prefix):
    
    # adds the player row to the game table
    if player_name.strip() != "":
        st.session_state["game_df"] = set_game_table_name(st.session_state["game_df"], player_name)
        st.session_state["player_table"] = set_game_table_name(st.session_state["player_table"], player_name)

    # set the header of the player as the players name
    st.subheader(player_name)

    # makes the buttons for this player
    cols = st.columns(3)
    stats = ['cut', 'drop', 'rev']

    for i, stat in enumerate(stats):
        key = f"{player_prefix}_{stat}"
        if key not in st.session_state:
            st.session_state[key] = 0
        with cols[i]:
            if st.button(f"{player_prefix.capitalize()} {stat.capitalize()}"):
                st.session_state[key] += 1
                set_element_df(st.session_state["game_df"], stat.capitalize(), player_name, st.session_state[key])
                add_element_df(st.session_state["player_table"], stat.capitalize(), player_name)
                st.session_state["player_table"]["Good Serves"] = st.session_state["game_df"][["Cut", "Drop", "Rev"]].sum(axis=1)
                st.session_state["player_table"]["Bad Serves"] = st.session_state["game_df"][["High", "Side", "Rim"]].sum(axis=1)

            st.markdown(st.session_state[key])

    # makes the buttons for this players
    cols = st.columns(3)
    stats = ['high', 'side', 'rim']

    for i, stat in enumerate(stats):
        key = f"{player_prefix}_{stat}"
        if key not in st.session_state:
            st.session_state[key] = 0
        with cols[i]:
            if st.button(f"{player_prefix.capitalize()} {stat.capitalize()}"):
                st.session_state[key] += 1
                set_element_df(st.session_state["game_df"], stat.capitalize(), player_name, st.session_state[key])
                add_element_df(st.session_state["player_table"], stat.capitalize(), player_name)
                st.session_state["player_table"]["Good Serves"] = st.session_state["game_df"][["Cut", "Drop", "Rev"]].sum(axis=1)
                st.session_state["player_table"]["Bad Serves"] = st.session_state["game_df"][["High", "Side", "Rim"]].sum(axis=1)

            st.markdown(st.session_state[key])

    # makes the buttons for this players
    cols = st.columns(4)
    stats = ['✅ set', '❌ set', '✅ hit', '❌ hit']

    for i, stat in enumerate(stats):
        key = f"{player_prefix}_{stat}"
        if key not in st.session_state:
            st.session_state[key] = 0
        with cols[i]:
            if st.button(f"{player_prefix.capitalize()} {stat.capitalize()}"):
                st.session_state[key] += 1
                set_element_df(st.session_state["game_df"], stat, player_name, st.session_state[key])
                set_element_df(st.session_state["player_table"], stat, player_name, st.session_state[key])

            st.markdown(st.session_state[key])

# Team Layout Function
def team_layout(team_name, player1_label, player2_label, player1_prefix, player2_prefix):
    
    scorebug(team_name)

    cols = st.columns(2)
    player1_name = cols[0].text_input(player1_label)
    player2_name = cols[1].text_input(player2_label)
    
    player_stats(player1_name, player1_prefix)
    player_stats(player2_name, player2_prefix)

cols = st.columns(2)
with cols[0].container(border = True):
    team_layout("Team 1", "Player 1", "Player 2", "P1", "P2")
with cols[1].container(border = True):
    team_layout("Team 2", "Player 3", "Player 4", "P3", "P4")

if st.button("Add Game", type="primary"):
    if "all_games" not in st.session_state:
        st.session_state["all_games"] = []

    st.write("### Final Stats for this Game")

    st.dataframe(st.session_state["game_df"])

    st.session_state["all_games"].append(st.session_state["game_df"].copy())
    st.success(f"Game {len(st.session_state['all_games'])} Added!")

    st.session_state["game_df"] = pd.DataFrame(game_cols)

    for key in list(st.session_state.keys()):
        if key.startswith("P"):
            del st.session_state[key]

   

