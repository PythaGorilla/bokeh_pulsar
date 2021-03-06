from __future__ import print_function

from bokeh.models import (
    Range1d, WMTSTileSource, ColumnDataSource, HoverTool,
)
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.airports import data as airports

title = "US Airports: Field Elevation > 1500m"
output_file("airports_map.html", title=title)

points_source = ColumnDataSource(airports)

# create tile source
tile_options = {}
tile_options['url'] = 'http://otile2.mqcdn.com/tiles/1.0.0/sat/{Z}/{X}/{Y}.png'
tile_source = WMTSTileSource(**tile_options)

# set to roughly extent of points
x_range = Range1d(start=airports['x'].min() - 10000, end=airports['x'].max() + 10000, bounds=None)
y_range = Range1d(start=airports['y'].min() - 10000, end=airports['y'].max() + 10000, bounds=None)

# create plot and add tools
p = figure(tools='wheel_zoom,pan', x_range=x_range, y_range=y_range, title=title)
p.axis.visible = False
hover_tool = HoverTool(tooltips=[("Name", "@name"), ("Elevation", "@elevation (m)")])
p.add_tools(hover_tool)
p.add_tile(tile_source)

# create point glyphs
p.circle(x='x', y='y', size=9, fill_color="#60ACA1", line_color="#D2C4C1", line_width=1.5, source=points_source)

show(p)
