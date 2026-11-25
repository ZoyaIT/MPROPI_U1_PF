import pandas as pd

def load_data(csv_path):
    """Carregueu el CSV utilitzant codificacions habituals i detecció automàtica del separador."""
    try:
        return pd.read_csv(csv_path, encoding="utf-8-sig", sep=None, engine="python")
    except UnicodeDecodeError:
        return pd.read_csv(csv_path, encoding="latin-1", sep=None, engine="python")


def get_filterable_columns(df):
    """Retorna les columnes amb un nombre manejable de valors distints."""
    result = []
    for column in df.columns:
        count = df[column].nunique(dropna=True)
        if 2 <= count <= 100:
            result.append(column)
    return result


def get_filter_options(df, filter_column):
    if filter_column not in df.columns:
        return []
    values = df[filter_column].dropna().astype(str).unique().tolist()
    return sorted(values, key=str.casefold)[:500]


def filter_and_sort_data(df, search="", filter_column="", filter_value="",
                         sort_column="", sort_order="asc"):
    result = df.copy()

    if search:
        mask = result.astype(str).apply(
            lambda column: column.str.contains(search, case=False, na=False, regex=False)
        ).any(axis=1)
        result = result[mask]

    if filter_column in result.columns and filter_value:
        result = result[result[filter_column].astype(str) == filter_value]

    if sort_column in result.columns:
        result = result.sort_values(
            by=sort_column,
            ascending=(sort_order != "desc"),
            kind="stable",
            na_position="last"
        )

    return result


def _find_column(columns, keywords):
    for column in columns:
        name = str(column).lower()
        if any(word in name for word in keywords):
            return column
    return None


def get_insights(filtered_df, full_df):
    """Formuleu observacions prudents basades en dades, sense inventar estadístiques."""
    if filtered_df.empty:
        return [
            {"title": "No s'han trobat registres", "value": "0", "description": "Prova de canviar o esborrar la cerca i els filtres."}
        ]

    insights = [
        {
            "title": "Registres al conjunt de dades",
            "value": f"{len(full_df):,}",
            "description": "Total de files carregades des del CSV original."
        },
        {
            "title": "Registres després del filtratge",
            "value": f"{len(filtered_df):,}",
            "description": "Files que actualment coincideixen amb la vostra cerca i les seleccions de filtre."
        }
    ]

    district_col = _find_column(filtered_df.columns, ["district", "districte", "barrio", "barri"])
    type_col = _find_column(filtered_df.columns, ["tipus_accident", "tipus de vehicle", "type", "causa", "descripcio", "descripción"])
    date_col = _find_column(filtered_df.columns, ["data", "fecha", "date"])

    for column, title, description in [
        (district_col, "Districte més representat", "Districte amb el nombre més elevat de files en la selecció actual."),
        (type_col, "Categoria més freqüent", "Valor més comú en aquesta columna de categoria dins la selecció actual.")
    ]:
        if column is not None:
            counts = filtered_df[column].dropna().astype(str).value_counts()
            if not counts.empty:
                insights.append({
                    "title": title,
                    "value": counts.index[0],
                    "description": f"{int(counts.iloc[0]):,} registres a “{column}”."
                })

    if date_col is not None:
        dates = pd.to_datetime(filtered_df[date_col], errors="coerce", dayfirst=True).dropna()
        if not dates.empty:
            insights.append({
                "title": "Cobertura de dates",
                "value": f"{dates.min().date()} – {dates.max().date()}",
                "description": f"Interval de dates detectat a “{date_col}” per a la selecció actual."
            })

    return insights[:5]
