import plotly.express as px
gapminder = px.data.gapminder()


# print(gapminder)


fig = px.scatter_geo(gapminder, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",
                     animation_frame="year",
                     projection="natural earth")
fig.show()