import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from charts import make_donut_chart


# Players DataFrame
players_df = pd.read_csv('players.csv')

# Games DataFrame
games_df = pd.read_csv('games.csv')
games_df.rename(columns={"Won points started on offense (holds)": "Holds", "Won points started on defense (breaks)": "Breaks"}, inplace=True)
games_df.reset_index()
games_df.set_index(keys='Opponent')

# drop columns with all zeros
games_df = games_df.loc[:, ~(games_df == 0).all()]


opponents_list = games_df['Opponent'].to_numpy()

players_df.rename(columns={"Assists": "A1", "Secondary assists": "A2"}, inplace=True)
players_df['+/-'] = players_df['A1'] + players_df['A2'] / 2 + players_df['Goals'] + players_df['Defensive blocks'] - players_df['Turnovers']
players_df = players_df.set_index('Player')
players_df = players_df[['Touches', 'Goals', 'A1', 'A2', 'Defensive blocks', 'Thrower errors', 'Receiver errors', 'Turnovers', '+/-', 'Offense points played', 'Defense points played', 'Points played total']]

# Title
st.title("Spring Tour Padova 2025 🥏")
st.subheader("One Tribe Stats")

# Opponent Filter
selection = st.pills("Games", opponents_list, selection_mode="multi", default=opponents_list)


# Games Stats
st.title('Game Stats')

filtered_games_df = games_df[games_df.iloc[:, 1].isin(selection)]
left_col, right_col = st.columns([3, 1])
left_col.dataframe(filtered_games_df)
st.dataframe(games_df)

break_container = right_col.container(border=True)
break_container.title('Breaks')
break_percentage = round((filtered_games_df['Breaks'].sum()*100/filtered_games_df['Defense possessions'].sum()),0)
donut_chart_breaks = make_donut_chart(break_percentage, 'Breaks')
break_container.altair_chart(donut_chart_breaks)

hold_container = right_col.container(border=True)
hold_container.title('Holds')
filtered_games_df = games_df[games_df.iloc[:, 1].isin(selection)]
hold_percentage = round((filtered_games_df['Holds'].sum()*100/filtered_games_df['Offense possessions'].sum()),0)
donut_chart_holds = make_donut_chart(hold_percentage, 'Holds')
hold_container.altair_chart(donut_chart_holds)


# Players Stats
st.title('Player Stats')
st.dataframe(players_df)