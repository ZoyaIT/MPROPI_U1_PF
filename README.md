# Barcelona Traffic Accidents Dashboard

A student project built using Flask, Jinja, Pandas, and Matplotlib.

## 1. Dataset

Download a CSV file of accidents handled by the Guàrdia Urbana from the
Barcelona City Council Open Data Portal:

https://opendata-ajuntament.barcelona.cat/data/es/dataset/accidents-gu-bcn

Choose a yearly CSV file and save it as:

`data/accidents.csv`

## 2. Install

Open Terminal in this project folder and run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Run

```bash
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

## 4. Project structure

- `app.py`: Flask routes and pages.
- `data.py`: reads, filters and sorts CSV data.
- `charts.py`: creates the graph with Matplotlib.
- `data/accidents.csv`: downloaded public dataset.
- `templates/index.html`: Jinja page.
- `static/css/style.css`: page styles.
- `static/img/`: generated chart.

The dashboard searches across all columns, filters by a selected column,
sorts records and displays up to 100 rows at a time.
