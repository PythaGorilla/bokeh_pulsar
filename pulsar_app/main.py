import pandas
import sys
import os
import numpy as np
from numpy import mean
from copy import deepcopy
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HoverTool,TapTool,WheelZoomTool,PanTool,LassoSelectTool,ResetTool,HBox,VBox,VBoxForm,TextInput
from bokeh.models.widgets import Slider, Select
from bokeh.io import curdoc
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn


csv="H:/WareHouse/bokeh/pulsar_app/pulsar_data_test.csv"
pdata=pandas.read_csv(csv)
#pdata["colors"]=np.where(pdata["TOAs"] > 0, "orange", "grey")
new_col=["Pulsar","TOAs","Raw_Profiles","Period","Period_Derivative","DM","RMS","Binary"]
pdata.columns=new_col
pdata["x"]=""
pdata["y"]=""
global scope_count


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

axis_map = {
    "TOAs": "TOAs",
    "Raw_Profiles": "Raw_Profiles",
    "Period": "Period",
    "Period_Derivative": "Period_Derivative",
    "DM": "DM",
    "RMS": "RMS",
}


# Create Input controls
# sliders
TOAs = Slider(title="TOAs", value=0, start=min(pdata["TOAs"])*0, end=max(pdata["TOAs"])*1.1, step=10)
Raw_Profiles = Slider(title="Raw_Profiles",  value=0, start=min(pdata["Raw_Profiles"])*0, end=max(pdata["Raw_Profiles"])*1.1, step=10)
Period = Slider(title="Period",  value=0, start=min(pdata["Period"])*0, end=max(pdata["Period"])*1.1, step=0.000001)
Period_Derivative = Slider(title="Period_Derivative",  value=0, start=min(pdata["Period_Derivative"])*10e21*0, end=max(pdata["Period_Derivative"])*10e21*1.1,step=1)
DM = Slider(title="Dispersion Measure",  value=0, start=min(pdata["DM"])*0, end=max(pdata["DM"])*1.1, step=1)
RMS = Slider(title="Root-mean-square Residuals",  value=0, start=min(pdata["RMS"])*0, end=max(pdata["RMS"])*1.1, step=0.1)
Operate_on_Y=TextInput(title="Example:x*1e-3")
Operate_on_Y=TextInput(title="Example:x*1e-3")
# dropdowns
Binary = Select(title="Binary", options=["","Y","-"], value="")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Period")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="RMS")

hover = HoverTool(tooltips=[
    ("Pulsar","@Pulsar"),
    ("TOAs", "@TOAs"),
    ("RMS", "@RMS")
])
lasso = LassoSelectTool()
tap=TapTool()
zoom=WheelZoomTool()
pan=PanTool()
reset=ResetTool()
# Set up x & y axis
# plot.add_layout(LinearAxis(), 'below')
# yaxis = LinearAxis()
# plot.add_layout(yaxis, 'left')
# plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))



source = ColumnDataSource(dict(x=[],y=[],TOAs=[],Raw_Profiles=[],Period=[],
        Period_Derivative=[],
        DM=[],
        RMS=[],
    ))

plot = Figure(title="Pulsar_data", plot_width=800,toolbar_location="above",plot_height=300,tools=[pan,lasso,tap,zoom,reset,hover])
plot.circle(x="x", y="y",source=source, fill_color="#396285", size=7,line_color=None, fill_alpha=1)
data_table = DataTable(source=source, columns=columns, width=800, height=300,editable=True,selectable="checkbox",scroll_to_selection=True,fit_columns=True)


def select_pulsars():
    Binary_val = Binary.value
    selected = pdata[
        (pdata.TOAs >= TOAs.value) &
        (pdata.Raw_Profiles >= Raw_Profiles.value) &
        (pdata.Period >= Period.value) &
        (pdata.Period_Derivative >= Period_Derivative.value/10e21) &
        (pdata.DM >= DM.value) &
        (pdata.RMS >= RMS.value)
    ]
    if (Binary_val != ""):
        selected = selected[selected.Binary.str.contains(Binary_val)==True]
    return selected

def update(attrname, old, new):
    df = select_pulsars()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    plot.xaxis.axis_label = x_axis.value
    plot.yaxis.axis_label = y_axis.value
    try:
        sel_count=len(source.selected["1d"]["indices"])
        print "sel_count=",sel_count
    except:
        sel_count=0

    source.data = dict(
        x=df[x_name],
        y=df[y_name],
        Pulsar=df["Pulsar"],
        TOAs=df["TOAs"],
        Raw_Profiles=df["Raw_Profiles"],
        Period=df["Period"],
        Period_Derivative=df["Period_Derivative"],
        DM=df["DM"],
        RMS=df["RMS"],
        Binary=df["Binary"]
    )
    scope_count=len(df)
    plot.title ="%i Pulsar in Scope"%scope_count

    print "source=",source.data


controls = [TOAs, Raw_Profiles, Period, Period_Derivative, DM, RMS, Binary, x_axis, y_axis]
# for control in controls:
#     control.on_change('value', update)
#inputs_control=HBox(VBoxForm(*controls), width=300)
# Add Glyphs

for control in controls:
    control.on_change('value', update)

def update_title(attr,old,new):
    plot.title=str(len(source.selected["1d"]["indices"]))+" Pulsar selected"
source.on_change("selected",update_title)


#cty_glyph = Circle(x=x_axis.value, y=y_axis.value, fill_color="#396285", size=8, fill_alpha=0.5, line_alpha=0.5)

inputs = HBox(VBoxForm(*controls), width=300)

update(None, None, None) # initial load of the data
curdoc().add_root(HBox(inputs, VBox(plot,data_table,width=1000), width=1100))


