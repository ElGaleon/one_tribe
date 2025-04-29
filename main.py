import pandas as pd
import streamlit as st

st.title("One Tribe at Spring Tour Padova 2025")

df = pd.read_csv('players.csv')
df.rename(columns={"Assists": "A1", "Secondary assists": "A2"}, inplace=True)
df['+/-'] = df['A1'] + df['A2'] / 2 + df['Goals'] - df['Turnovers']
df = df.set_index('Player')
df = df[['Touches', 'Goals', 'A1', 'A2', 'Defensive blocks', 'Thrower errors', 'Receiver errors', 'Turnovers', '+/-', 'Offense points played', 'Defense points played', 'Points played total']]

st.dataframe(df)
