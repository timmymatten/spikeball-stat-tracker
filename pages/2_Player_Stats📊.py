import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from db import fetch_player_stats

st.set_page_config(page_title="Player Stats", page_icon="🤾")

st.markdown("# Player Stats ")
st.sidebar.header("Player Stats")
st.write(
    """
    Here we can take a look at player stats!
"""
)

# Load player stats from database
db_player_stats = fetch_player_stats()

if db_player_stats:
    # Create a DataFrame from database results
    player_data = []
    for player in db_player_stats:
        player_data.append({
            'player_name': player[1],
            'good_serves': player[2],
            'bad_serves': player[3],
            'successful_sets': player[4],
            'failed_sets': player[5],
            'successful_hits': player[6],
            'failed_hits': player[7]
        })
    
    player_df = pd.DataFrame(player_data)
    player_df.set_index('player_name', inplace=True)
    
    # Add calculated columns
    player_df['Good Serves'] = player_df['good_serves']
    player_df['Bad Serves'] = player_df['bad_serves']
    player_df['✅ set'] = player_df['successful_sets']
    player_df['❌ set'] = player_df['failed_sets']
    player_df['✅ hit'] = player_df['successful_hits']
    player_df['❌ hit'] = player_df['failed_hits']
    
    # Store in session state for compatibility with existing code
    st.session_state["player_table"] = player_df
    
    # Table of Players
    st.subheader("Player Stats")
    cols = st.columns(2)
    with cols[0]:
        player_for_chart = st.selectbox(
            "Select a player to analyze",
            player_df.index.tolist(),
            index=None,
            placeholder="Player...",
        )
    
    st.dataframe(player_df[['Good Serves', 'Bad Serves', '✅ set', '❌ set', '✅ hit', '❌ hit']])

    with cols[1]:
        if player_for_chart is None:
            st.write("No Preview For Empty Player Selection")
        else:
            if st.button("Good Serves"):
                # For good serves, we'll use a simple bar chart since we don't have the breakdown
                fig, ax = plt.subplots()
                ax.bar(['Good Serves'], [player_df.loc[player_for_chart, 'Good Serves']], color='green')
                ax.set_ylabel('Count')
                ax.set_title(f'Good Serves for {player_for_chart}')
                st.pyplot(fig)
                
            if st.button("Bad Serves"):
                # For bad serves, we'll use a simple bar chart since we don't have the breakdown
                fig, ax = plt.subplots()
                ax.bar(['Bad Serves'], [player_df.loc[player_for_chart, 'Bad Serves']], color='red')
                ax.set_ylabel('Count')
                ax.set_title(f'Bad Serves for {player_for_chart}')
                st.pyplot(fig)
elif "player_table" in st.session_state:
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
