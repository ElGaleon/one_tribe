import pandas as pd
import altair as alt

# Donut chart
def make_donut_chart(percentage, input_text):
  if percentage < 30:
    chart_color = ['#E74C3C', '#781F16']
  elif percentage < 70:
    chart_color = ['#F39C12', '#875A12']
  else:
    chart_color = ['#27AE60', '#12783D']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-percentage, percentage]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
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
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=24, fontWeight=700).encode(text=alt.value(f'{percentage} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text