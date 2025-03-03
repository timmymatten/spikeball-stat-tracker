import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Player Stats", page_icon="🤾")

st.markdown("# Player Stats ")
st.sidebar.header("Player Stats")
st.write(
    """
    Here we can take a look at player stats!
"""
)

# Table of Players

if "player_table" in st.session_state:
    st.subheader("Player Stats")
    cols = st.columns(2)
    with cols[0]:
        player_for_chart = st.selectbox(
            "Select a player to analyze",
            st.session_state["player_table"].index.tolist(),
            index=None,
            placeholder="Player...",
        )
    
    st.dataframe(st.session_state["player_table"][['Good Serves', 'Bad Serves', '✅ set', '❌ set', '✅ hit', '❌ hit']])

    with cols[1]:
        if player_for_chart is None:
            st.write("No Preview For Empty Player Selection")
        else:
            

            if st.button("Good Serves"):
                labels = "Cut", "Drop", "Rev"
                sizes = st.session_state["player_table"].loc[player_for_chart][["Cut", "Drop", "Rev"]].fillna(0).values

                if sizes.sum() == 0:
                    st.warning(f"No data available for {player_for_chart}")
                else:
                    fig, ax = plt.subplots()
                    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
                    ax.axis("equal")
                    st.pyplot(fig)
            if st.button("Bad Serves"):
                labels = "High", "Side", "Rim"
                sizes = st.session_state["player_table"].loc[player_for_chart][["High", "Side", "Rim"]].fillna(0).values

                if sizes.sum() == 0:
                    st.warning(f"No data available for {player_for_chart}")
                else:
                    fig, ax = plt.subplots()
                    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
                    ax.axis("equal")
                    st.pyplot(fig)

else:
    st.warning("No players added yet!")
