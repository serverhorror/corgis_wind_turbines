#%%
def my_print(msg="Hello, interactive window!"):
    print(msg)


#%%
my_print()

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
def read_my_data(head=True):
    print("Reading tons of data", end="")
    if head == False:
        for i in range(10):
            print(".", end="")
            time.sleep(1)
        print("done!")
    df = pd.read_csv("wind_turbines.csv", header=0)
    if head:
        return df.head()
    return df


#%%
read_my_data()
#%%
read_my_data(False)


#%%
head = read_my_data(False).head()

#%%
SC = "Site.State"
TC = "Turbine.Capacity"
#%%
head

#%%
head[SC]  ## access by column
#%%
head.loc[1]  # get the first row

#%%
df2 = read_my_data(False)[[SC, TC]].groupby([SC]).mean()
#%%
df3 = pd.concat(
    [
        df2.nlargest(10, columns=TC),
        df2.nsmallest(10, columns=TC),
    ]
).sort_values(
    by=TC,
    ascending=False,
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
            log_y=True,  # represent bars with log scale
            # color_discrete_sequence=[cyclical.IceFire],  # color of histogram bars
            color=TC,
            # histfunc="avg",
        )
        fig.update_layout(bargap=0.1)
        return fig


#%%
get_plot(PlotType.PLOTLY, df2.sort_values(by=TC)).show()
#%%
get_plot(PlotType.MATPLOTLIB, df2.sort_values(by=TC)).show()

#%%


def _():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df2.index, y=df2[TC]))
    fig.update_layout(title="Hello Figure foo")
    fig.show()


_()
