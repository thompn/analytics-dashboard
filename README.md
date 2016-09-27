# Analytics Dashboard

A graph based dashboard served with flask, plotly.js and pandas in the back-end.

  - Pulls information from MySQL database;
  - Uses the Pandas library to analyse and rework data
  - Pushes the graph JSON to plotly.js to render in web page

Based on [plotly.js-flask](https://github.com/plotly/plotlyjs-flask-example) by [chriddyp](https://github.com/chriddyp) from plot.ly

### Requirements
The dashboard requires:
* Python 3
* Flask
* Pandas
* Plotly 

### Usage

Whilst this dashboard is bespoke, the backend computation script can be adopted to any data source and series of dataframes in pandas.

*Development dataset was generated from a telegram group chat, via a telegram bot*

Ensure requirments are fulfilled, and run the app:
```sh
$ cd analytics-dashboard
$ python app.py
$ * Running on http://0.0.0.0:9999/ (Press CTRL+C to quit)
```
Navigate to localhost:9999 to see web output, or push to a web server (be sure to disable debugging).

![](https://github.com/thompn/analytics-dashboard/blob/master/static/images/screenshot.png?raw=true)
