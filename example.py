# %%
import enum
import time
from functools import lru_cache
from logging import root
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from plotly.colors import cyclical, sequential


#%%
@lru_cache(15)
def read_my_data():
    print("Reading tons of data", end="")
    for i in range(10):
        print(".", end="")
        time.sleep(1)
    print("done!")
    df = pd.read_csv("wind_turbines.csv", header=0)
    return df


#%%
read_my_data().head()


#%%
SC = "Site.County"
TC = "Turbine.Capacity"
head = read_my_data().head()
#%%
head

#%%
head[SC]  ## access by row
#%%
head.loc[1]  # get the first row

#%%
df2 = read_my_data()[[SC, TC]].groupby([SC]).mean()
#%%
df3 = pd.concat(
    [
        df2.nlargest(10, columns=TC),
        df2.nsmallest(10, columns=TC),
    ]
).sort_values(
    by=TC,
)
# %%


class PlotType(enum.Enum):
    MATPLOTLIB = enum.auto()
    PLOTLY = enum.auto()


def get_plot(plot_type: PlotType, df: pd.DataFrame) -> Any:
    if plot_type == PlotType.MATPLOTLIB:
        plt.plot()
        plt.bar(df.index, df[TC])
        # ax=plt.gca();ax.set_xticklabels(labels=df3.index,rotation=45)
        plt.xticks(rotation=90)
        return plt
    if plot_type == PlotType.PLOTLY:
        fig = px.bar(
            df,
            # y=df.index,
            y=TC,
            # nbins=7,
            opacity=0.8,
            # log_y=True,  # represent bars with log scale
            # color_discrete_sequence=[cyclical.Twilight],  # color of histogram bars
            color=TC,
            # histfunc="avg",
        )
        fig.update_layout(bargap=0.1)
        return fig


#%%
df = read_my_data()

#%%
get_plot(PlotType.MATPLOTLIB, df).show()
#%%
get_plot(PlotType.PLOTLY, df).show()

#%%


def _():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df2.index, y=df2[TC]))
    fig.update_layout(title="Hello Figure foo")
    fig.show()


_()
