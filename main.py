import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt

def make_donut(breaks_done, break_chances, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#12783D', '#27AE60']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [breaks_done, break_chances - breaks_done]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [break_chances - breaks_done, 0]
  })

  # Plot BG
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
    
  # Plot
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
  percentage = "{:.0f}".format(breaks_done*100/break_chances)
  text = plot.mark_text(align='center', color="#29b5e8", font="Inter", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{percentage} %'))

  return plot + plot_bg + text


st.title("One Tribe at Spring Tour Padova 2025")

# Players DataFrame
players_df = pd.read_csv('players.csv')

# Games DataFrame
games_df = pd.read_csv('games.csv')
games_df.rename(columns={"Won points started on offense (holds)": "Holds", "Won points started on defense (breaks)": "Breaks"}, inplace=True)


# Crea il grafico a ciambella
fig, ax = plt.subplots()

# Dati per il donut chart
colori = ['#4CAF50', '#E0E0E0']  # verde e grigio chiaro

# Pie chart con "hole" per renderlo una ciambella
wedges, _ = ax.pie([1,1],
                   colors=colori,
                   startangle=90,
                   wedgeprops=dict(width=0.3, edgecolor='white'))



# Rendi il grafico un cerchio perfetto
ax.set_aspect('equal')

# Rimuovi bordi e assi
plt.axis('off')

plt.show()


opponents_list = games_df['Opponent'].to_numpy()
if 'selected_games' not in st.session_state:
    st.session_state.selected_games = opponents_list

# Sidebar
with st.sidebar:
    st.title('Filter by match 🥏')
    for opponent in opponents_list:
        opponent_checkbox = st.checkbox(opponent, value=opponent in st.session_state.selected_games)


players_df.rename(columns={"Assists": "A1", "Secondary assists": "A2"}, inplace=True)
players_df['+/-'] = players_df['A1'] + players_df['A2'] / 2 + players_df['Goals'] + players_df['Defensive blocks'] - players_df['Turnovers']
players_df = players_df.set_index('Player')
players_df = players_df[['Touches', 'Goals', 'A1', 'A2', 'Defensive blocks', 'Thrower errors', 'Receiver errors', 'Turnovers', '+/-', 'Offense points played', 'Defense points played', 'Points played total']]



# Overall stats
total_breaks = games_df['Breaks'].sum()
total_defense_possession = games_df['Defense possessions'].sum()

fig, ax = plt.subplots()
#st.title(f"{row['Opponent']} Total Breaks out of Break Chances")
plt.pie([total_breaks, total_defense_possession-total_breaks])
break_circle = plt.Circle( (0,0), 0.7, color='white')
plot = plt.gcf()
plot.gca().add_artist(break_circle)
# Percentage at center
ax.text(0, 0.1, f"{(total_breaks*100/total_defense_possession):.0f}%", ha='center', va='center', fontsize=20, fontweight='bold')

# Text
ax.text(0, -0.2, f"{total_breaks} out of {total_defense_possession}", ha='center', va='center', fontsize=12)
plt.show()
st.pyplot(plot)

for index, row in games_df.iterrows():
    fig, ax = plt.subplots()
    st.title(f"{row['Opponent']} Total Breaks out of Break Chances")
    breaks_difference = row['Defense possessions'] - row['Breaks']
    plt.pie([row['Breaks'], breaks_difference])
    donut_chart_breaks = make_donut(row['Breaks'], row['Defense possessions'], 'Breaks', 'green')
    st.altair_chart(donut_chart_breaks)
    break_circle = plt.Circle( (0,0), 0.7, color='white')
    plot = plt.gcf()
    plot.gca().add_artist(break_circle)
    # Percentage at center
    ax.text(0, 0.1, f"{(row['Breaks']*100/row['Defense possessions']):.0f}%", ha='center', va='center', fontsize=20, fontweight='bold')

    # Text
    ax.text(0, -0.2, f"{row['Breaks']} out of {row['Defense possessions']}", ha='center', va='center', fontsize=12)
    plt.show()
    st.pyplot(plot)

st.title('Player Stats')
st.dataframe(players_df)

st.title('Game Stats')
st.dataframe(games_df)