import pandas
import sys
import os
import numpy as np
from numpy import mean
from bokeh.plotting import hplot, Figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, HBox,VBox, VBoxForm,Plot,DataRange1d,LinearAxis,Circle,Grid
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Callback,CustomJS
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform,vplot

output_file("pulsar.html")

csv="H:/WareHouse/bokeh/pulsar_app/pulsar_data_test.csv"
df=pandas.read_csv(csv)
#df["colors"]=np.where(df["TOAs"] > 0, "orange", "grey")
new_col=["Pulsar","TOAs","Raw_Profiles","Period","Period_Derivative","DM","RMS","Binary"]
df.columns=new_col
data1=dict(Pulsar=df["Pulsar"],Period=df["Period"],title="")
source1 = ColumnDataSource(df)

print [i for i in df.index]
columns = [
        TableColumn(field="Pulsar", title="Pulsar"),
        TableColumn(field="TOAs", title="TOAs"),
        TableColumn(field="Raw_Profiles", title="Raw_Profiles"),
        TableColumn(field="Period", title="Period"),
        TableColumn(field="Period_Derivative", title="Period_Derivative"),
        TableColumn(field="DM", title="DM"),
        TableColumn(field="RMS", title="RMS"),
        TableColumn(field="Binary", title="Binary"),
    ]

data_table = DataTable(source=source1, columns=columns, width=800, height=300,editable=True,selectable="checkbox",scroll_to_selection=False,fit_columns=True)


axis_map = {
    "TOAs": "TOAs",
    "Raw_Profiles": "Raw_Profiles",
    "Period": "Reviews",
    "Period_Derivative": "Period_Derivative",
    "DM": "DM",
    "RMS": "RMS",
}


# Create Input controls
TOAs = Slider(title="TOAs", value=80, start=min(df["TOAs"])*1.2, end=max(df["TOAs"])*1.2, step=10)
Raw_Profiles = Slider(title="Raw_Profiles",  value=mean(df["TOAs"]), start=min(df["TOAs"])*1.2, end=max(df["TOAs"])*1.2, step=10)
Period = Slider(title="Period",  value=mean(df["Period"]), start=min(df["Period"])*1.2, end=max(df["Period"])*1.2, step=0.000001)
Period_Derivative = Slider(title="Period_Derivative",  value=mean(df["Period_Derivative"]), start=min(df["Period_Derivative"])*1.2, end=max(df["Period_Derivative"])*1.2,step=0.1e-21)
DM = Slider(title="Dispersion Measure",  value=mean(df["DM"]), start=min(df["DM"])*1.2, end=max(df["DM"])*1.2, step=1)
RMS = Slider(title="Root-mean-square Residuals",  value=mean(df["RMS"]), start=min(df["RMS"])*1.2, end=max(df["RMS"])*1.2, step=0.1)

Binary = Select(title="Binary", options=["Y","-"], value="")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Period")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="RMS")


plot = Plot(title="Pulsar_data", x_range= DataRange1d(), y_range=DataRange1d(), plot_width=1000, plot_height=300)

# Set up x & y axis
plot.add_layout(LinearAxis(), 'below')
yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

controls = [TOAs, Raw_Profiles, Period, Period_Derivative, DM, RMS, Binary, x_axis, x_axis, y_axis]
# for control in controls:
#     control.on_change('value', update)
inputs_control=HBox(VBoxForm(*controls), width=300)
# Add Glyphs
cty_glyph = Circle(x="TOAs", y="Period", fill_color="#396285", size=8, fill_alpha=0.5, line_alpha=0.5)
cty = plot.add_glyph(source1, cty_glyph)


show(hplot(inputs_control,vplot(plot, data_table)))



# def select_rows():
#     print data_table.value
#     return data_table.value
#
# def update(attrname, old, new):
#     p1.title=data_table.value
#
# # source1.callback = CustomJS(args=dict(source=source1), code="""
# #     var title=source.get('title')
# #     title = cb_obj.get('selected')['1d'].indices;
# #
# #     source.trigger('change');
# #     cb_obj.trigger('change');
# #
# #     """)
#
# #show(vform(data_table))
# layout = hplot(vform(data_table),p1)
# controls = [data_table]
# for control in controls:
#     control.on_change('value', update)
#
# inputs = HBox(VBoxForm(*controls), width=300)
#
# update(None, None, None) # initial load of the data
#
# curdoc().add_root(HBox(inputs, p1, width=1100))
