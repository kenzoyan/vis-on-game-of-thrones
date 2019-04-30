import altair as alt
from vega_datasets import data
import pandas as pd
import numpy as np 

data=pd.read_csv("got_csv.csv")
dropindex=['Director','Writer','Original Air Date','Runtime (mins)','IMDB Description', 'IMDB votes']
minidata=data.drop(dropindex,axis=1)
minidata.head()   
minidata['L']=1

selector=alt.selection_multi(empty='all', fields=['Season'])
#input_dropdown = alt.binding_select(options=['1','2','3','4','5','6','7'])
#selector = alt.selection_single(fields=['Season'], bind=input_dropdown, name='Country of ')
base=alt.Chart(minidata).properties(
    width=600,
    height=600,
    ).add_selection(
        selector
    )


left=base.mark_point(filled=True,fillOpacity=0.9,size=400).encode(
    alt.X('US viewers (million):Q'),
    alt.Y('Notable Death Count:Q'),

    color=alt.condition(selector, 'Season:N', alt.value('lightgray')),
    shape='Season:N',
    tooltip=['US viewers (million)', 'Notable Death Count', 'Imdb Rating', 'Season']
    ).interactive().properties(
        title='Scatter--Vis on Game of Thrones',
    )

line=base.mark_line(point=True,).encode(
    alt.X('Number in Season:Q'),
    alt.Y('Imdb Rating:Q',scale=alt.Scale(domain=(7.5, 10))),
    color=alt.condition(selector, 'Season:N', alt.value('transparent')),
    #color=alt.Color('Season:N')
    ).add_selection(
    selector
    ).properties(
        title='Line--Vis on Game of Thrones',
    )

label=alt.Chart(minidata).mark_circle(size=200,filled=True).encode(
    alt.X('L:N'),
    alt.Y('Season:N'),
    color=alt.condition(selector, 'Season:N', alt.value('lightgray')),
    ).add_selection(
    selector
    ).properties(
    title="Control Bar"
    )

base.configure_title(
    fontSize=20,
    font='Courier',
    anchor='start',
    color='gray'
)

all=left|label|line
all.save("index.html")
