import os

import pandas
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, TapTool, WheelZoomTool, PanTool, LassoSelectTool, ResetTool, HBox, \
    VBox, VBoxForm, TextInput
from bokeh.models.widgets import DataTable, TableColumn, Button, Slider, Select
from bokeh.plotting import Figure

abspath = os.path.dirname(__file__)

# load data from csv
csv = abspath + "/pulsar_data_test.csv"
pdata = pandas.read_csv(csv)
new_col = ["Pulsar", "TOAs", "Raw_Profiles", "Period", "Period_Derivative", "DM", "RMS", "Binary"]
pdata.columns = new_col
pdata["x"] = ""
pdata["y"] = ""
scope_count = 0
record_source = ColumnDataSource(pdata)

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
    "Pulsar": "Pulsar",
    "TOAs": "TOAs",
    "Raw_Profiles": "Raw_Profiles",
    "Period": "Period",
    "Period_Derivative": "Period_Derivative",
    "DM": "DM",
    "RMS": "RMS",
}

# Create Input controls
# sliders
TOAs = Slider(title="TOAs", value=0, start=min(pdata["TOAs"]) * 0, end=max(pdata["TOAs"]) * 1.1, step=10)
Raw_Profiles = Slider(title="Raw Profiles", value=0, start=min(pdata["Raw_Profiles"]) * 0,
                      end=max(pdata["Raw_Profiles"]) * 1.1, step=10)
Period = Slider(title="Period", value=0, start=min(pdata["Period"]) * 0, end=max(pdata["Period"]) * 1.1, step=0.000001)
Period_Derivative = Slider(title="Period Derivative", value=0, start=min(pdata["Period_Derivative"]) * 10e21 * 0,
                           end=max(pdata["Period_Derivative"]) * 10e21 * 1.1, step=1)
DM = Slider(title="Dispersion Measure", value=0, start=min(pdata["DM"]) * 0, end=max(pdata["DM"]) * 1.1, step=1)
RMS = Slider(title="Root-mean-square Residuals", value=0, start=min(pdata["RMS"]) * 0, end=max(pdata["RMS"]) * 1.1,
             step=0.1)
Operate_on_X = TextInput(title="Operate on X", value="Example:x*1e3")
Operate_on_Y = TextInput(title="Operate on Y", value="Example:log(y)")
# dropdowns
Binary = Select(title="Binary", options=["", "Y", "-"], value="")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Pulsar")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Period")

# Input widigets
Input1 = TextInput(title="Pulsar")
Input2 = TextInput(title="TOAs")
Input3 = TextInput(title="Raw_Profiles")
Input4 = TextInput(title="Period")
Input5 = TextInput(title="Period_Derivative")
Input6 = TextInput(title="DM")
Input7 = TextInput(title="RMS")
Input8 = TextInput(title="Binary")

hover = HoverTool(tooltips=[
    ("Pulsar", "@Pulsar"),
    ("TOAs", "@TOAs"),
    ("Period", "@Period")
])
lasso = LassoSelectTool()
tap = TapTool()
zoom = WheelZoomTool()
pan = PanTool()
reset = ResetTool()

source = ColumnDataSource(dict(
    x=pdata["Pulsar"],
    y=pdata["Period"],
    Pulsar=pdata["Pulsar"],
    TOAs=pdata["TOAs"],
    Raw_Profiles=pdata["Raw_Profiles"],
    Period=pdata["Period"],
    Period_Derivative=pdata["Period_Derivative"],
    DM=pdata["DM"],
    RMS=pdata["RMS"],
    Binary=pdata["Binary"]
))

plot = Figure(title="Pulsar data", plot_width=1200, responsive=True, toolbar_location="above", plot_height=500,
              tools=[pan, lasso, tap, zoom, reset, hover])
plot.circle(x="x", y="y", source=source, fill_color="#396285", size=8, fill_alpha=0.6)
data_table = DataTable(source=source, columns=columns, width=1200, height=500, editable=False, sortable=False,
                       selectable="checkbox",
                       scroll_to_selection=True, fit_columns=True)


def onclick_del():
    sdf = source.to_df()
    rsdf = record_source.to_df()

    rows = source.selected["1d"]["indices"]
    pulsar_names = sdf.loc[rows]["Pulsar"]

    for p in pulsar_names:
        rsdf = rsdf[rsdf.Pulsar != p]
        sdf = sdf[sdf.Pulsar != p]

    source.data = dict(sdf)
    record_source.data = dict(rsdf)
    source.selected = record_source.selected  # clean selected



def onclick_add():
    # source data to panda format
    sdf = source.to_df()
    rsdf = record_source.to_df()
    new_row = pandas.DataFrame(dict(
        x=Input1.value,
        y=float(Input4.value),
        Pulsar=Input1.value,
        TOAs=float(Input2.value),
        Raw_Profiles=int(Input3.value),
        Period=float(Input4.value),
        Period_Derivative=float(Input5.value),
        DM=float(Input6.value),
        RMS=float(Input7.value),
        Binary=Input8.value
    ), index=[0])

    new_df = pandas.DataFrame(new_row)
    row_data = new_df.iloc[0]
    sdf.loc[sdf.shape[0] + 1] = row_data
    rsdf.loc[rsdf.shape[0] + 1] = row_data
    source.data = dict(sdf)
    record_source.data = dict(rsdf)


def onclick_reset():
    global record_source
    record_source = ColumnDataSource(pdata)
    global initilized
    initilized = False
    update_display(1, 1, 1)


# Buttons
del_btn = Button(label=" Delete Rows", type="success")
add_btn = Button(label="Add Row", type="success")
reset_btn = Button(label="Reload Data", type="success")

del_btn.on_click(onclick_del)
add_btn.on_click(onclick_add)
reset_btn.on_click(onclick_reset)


def select_pulsars():
    Binary_val = Binary.value
    tsource = record_source.to_df()
    selected = tsource[
        (tsource.TOAs >= TOAs.value) &
        (tsource.Raw_Profiles >= Raw_Profiles.value) &
        (tsource.Period >= Period.value) &
        (tsource.Period_Derivative >= Period_Derivative.value / 10e21) &
        (tsource.DM >= DM.value) &
        (tsource.RMS >= RMS.value)
        ]
    if (Binary_val != ""):
        selected = selected[selected.Binary.str.contains(Binary_val) == True]

    fx_str = "lambda x:" + Operate_on_X.value.strip()
    fy_str = "lambda y:" + Operate_on_Y.value.strip()
    try:
        # need some better function
        fnx = eval(fx_str)
        selected[x_axis.value] = map(fnx, selected[x_axis.value])
    except Exception as e:
        print("Error is ::::::::::" + str(e))
        print(fx_str)
    try:
        fny = eval(fy_str)
        selected[y_axis.value] = map(fny, selected[y_axis.value])
    except:
        pass
    return selected


def update_display(attrname, old, new):
    df = select_pulsars()

    x = df[axis_map[x_axis.value]] if axis_map[x_axis.value] <> "Pulsar" else df.index
    y = df[axis_map[y_axis.value]] if axis_map[y_axis.value] <> "Pulsar" else df.index

    plot.xaxis.axis_label = x_axis.value
    plot.yaxis.axis_label = y_axis.value
    try:
        sel_count = len(source.selected["1d"]["indices"])
    except:
        sel_count = 0

    source.data = dict(
        x=x,
        y=y,
        Pulsar=df["Pulsar"],
        TOAs=df["TOAs"],
        Raw_Profiles=df["Raw_Profiles"],
        Period=df["Period"],
        Period_Derivative=df["Period_Derivative"],
        DM=df["DM"],
        RMS=df["RMS"],
        Binary=df["Binary"]
    )
    scope_count = len(df)
    plot.title = "%i Pulsar in Scope" % scope_count+" %i selected"%sel_count
    print("source updated")


controls = [TOAs, Raw_Profiles, Period, Period_Derivative, DM, RMS, Binary, x_axis, y_axis, HBox(height=50),
            Operate_on_X, Operate_on_Y]

for control in controls:
    control.on_change('value', update_display)

input_controls = [Input1, Input2, Input3, Input4, Input5, Input6, Input7, Input8]


def update_title(attr, old, new):
    plot.title = str(len(source.selected["1d"]["indices"])) + " Pulsar selected"


source.on_change("selected", update_title)

input_controls_box = HBox(HBox(*input_controls))
del_btn_box = VBox(HBox(HBox(width=200), del_btn, height=80, width=200), height=100)
reset_btn_box = HBox(HBox(width=300), VBox(reset_btn, HBox(height=140), add_btn), height=80, width=100)
filters_box = HBox(VBox(VBoxForm(*controls[:-5]), del_btn_box), width=400)
plot_control_box = VBox(VBoxForm(*controls[-5:]), reset_btn_box, width=400)
update_display(None, None, None)  # initial load of the data
curdoc().add_root(
    HBox(filters_box, VBox(plot, input_controls_box, HBox(data_table), width=1200), plot_control_box, width=1800))
