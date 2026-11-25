
from flask import Flask, render_template, request
from data import (
    load_data, get_filter_options, filter_and_sort_data,
    get_insights, get_filterable_columns
)
from charts import createGraph
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "accidents.csv")


@app.route("/")
def index():
    df = load_data(CSV_PATH)

    search = request.args.get("search", "").strip()
    filter_column = request.args.get("filter_column", "")
    filter_value = request.args.get("filter_value", "")
    sort_column = request.args.get("sort_column", "")
    sort_order = request.args.get("sort_order", "asc")

    # Number of records shown in the table.
    try:
        per_page = int(request.args.get("per_page", 25))
    except (TypeError, ValueError):
        per_page = 25
    if per_page not in (10, 25, 50, 100):
        per_page = 25

    df_filtered = filter_and_sort_data(
        df, search, filter_column, filter_value, sort_column, sort_order
    )

    table_columns = list(df_filtered.columns[:8])
    rows = df_filtered[table_columns].head(per_page).fillna("").to_dict(orient="records")

    filter_columns = get_filterable_columns(df)
    filter_options = get_filter_options(df, filter_column)

    # The chart and insights use the filtered data so they respond to filters/search.
    chart_path = createGraph(df_filtered)
    insights = get_insights(df_filtered, df)

    return render_template(
        "index.html",
        total=len(df),
        filtered_total=len(df_filtered),
        columns=list(df.columns),
        table_columns=table_columns,
        rows=rows,
        search=search,
        filter_column=filter_column,
        filter_value=filter_value,
        filter_columns=filter_columns,
        filter_options=filter_options,
        sort_column=sort_column,
        sort_order=sort_order,
        per_page=per_page,
        insights=insights,
        chart_available=bool(chart_path)
    )


if __name__ == "__main__":
    app.run(debug=True)

