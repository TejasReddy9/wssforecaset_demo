from flask import Flask 
import dash
import os, math
import dash_core_components as dcc 
import dash_html_components as html 
import plotly
import plotly.graph_objs as go 
import pandas as pd 

#############
# Define app 
#############
server = Flask(__name__)
app = dash.Dash(__name__, server = server)


##############################
# Determine dropdown options
##############################
pwd = os.getcwd()
path = os.path.join(pwd, "train.csv")
df = pd.read_csv(path)

dept_stores = {} 
for dept in df.Dept.unique():
	dept_stores[dept] = list(df[df.Dept == dept].Store.unique())

depts = list(dept_stores.keys())
stores = dept_stores[depts[0]]

##############################
# Front-end display contents
##############################
app.layout = html.Div([
		dcc.Markdown('''
# Walmart Sales Data Visualization
#### In total, there are 45 stores. Each having it's own set of departments.
#### Navigate for their weekly sales data.
'''),
		html.Div([
			dcc.Dropdown(id = "dept-dropdown", options = [{ "label": dept, "value": dept} for dept in depts], value = depts[0])
			]),
		html.Div([
			dcc.Dropdown(id = "store-dropdown")
			]),
		html.Hr(),
		html.Div([
			dcc.Graph(id = "graphs")
			])
	])


#######################################
# Back-end functions to induce change
#######################################
@app.callback(
	dash.dependencies.Output("store-dropdown", "options"),
	[dash.dependencies.Input("dept-dropdown", "value")]
)
def update_store_dropdown(dept):
	return [{ "label": i, "value": i } for i in dept_stores[dept]]


@app.callback(dash.dependencies.Output("graphs", "figure"),
			[dash.dependencies.Input("dept-dropdown", "value"), dash.dependencies.Input("store-dropdown","value")])
def update_graph(dept, store):

	dfx = df[df.Dept == dept]
	dfx = dfx[dfx.Store == store].Weekly_Sales
	dfx = dfx.apply(lambda x: math.log(x,10))
	dfx = dfx.to_frame(name = "log(Weekly_Sales)")
	dfx.reset_index(inplace=True)

	X = dfx["index"]
	Y = dfx["log(Weekly_Sales)"]

	data = go.Scatter(x = list(X), 
						y = list(Y),
						name = "Scatter plot",
						mode = "lines+markers")

	return { "data": [data], "layout": {"title": "Dept "+str(dept)+"-"+"Store "+str(store)}}



##############
# Run server
##############
if __name__ == "__main__":
	app.run_server(debug=True, threaded=True)






