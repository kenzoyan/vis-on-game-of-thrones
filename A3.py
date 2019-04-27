import altair as alt
from vega_datasets import data
import pandas as pd
import numpy as np 

data=pd.read_csv("got_csv.csv")
dropindex=['Director','Writer','Original Air Date','Runtime (mins)','IMDB Description', 'IMDB votes']
minidata=data.drop(dropindex,axis=1)
minidata.head()   

selector=alt.selection_multi(empty='all', fields=['Season'])

base=alt.Chart(minidata).properties(
    width=600,
    height=600,
    title='Vis on Game of Thrones',
    ).add_selection(
        selector
    )


left=base.mark_point(filled=True,fillOpacity=0.9,size=400).encode(
    alt.X('US viewers (million):Q'),
    alt.Y('Notable Death Count:Q'),

    color=alt.condition(selector, 'Season:N', alt.value('lightgray')),
    shape='Season:N',
    tooltip=['US viewers (million)', 'Notable Death Count', 'Imdb Rating', 'Season']
    ).interactive()

line=base.mark_line(point=True,).encode(
    alt.X('Number in Season:Q'),
    alt.Y('Imdb Rating:Q',scale=alt.Scale(domain=(7.5, 10))),
    color=alt.Color('Season:N')
    ).transform_filter(
    selector
    )

left.configure_title(
    fontSize=20,
    font='Courier',
    anchor='start',
    color='gray'
)

all=left|line
all.save("index.html")
