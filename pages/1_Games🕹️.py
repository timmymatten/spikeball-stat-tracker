import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Past Games", page_icon="🕰️")

st.markdown("# Past Games")
st.sidebar.header("Games")
st.write(
    """
    Here we can take a look at past games and stats!
"""
)

if "all_games" in st.session_state and len(st.session_state["all_games"]) > 0:
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



