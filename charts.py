
import os
from matplotlib.figure import Figure


def createGraph(data):
    """Create a pie chart from the most suitable categorical column."""
    if data is None or data.empty:
        return None

    columns = list(data.columns)
    category = None

    # Prefer columns that are meaningful for an accident dashboard.
    preferred_words = [
        "districte", "district", "barri", "barrio",
        "tipus", "tipo", "causa", "nacionalitat", "nacionalidad"
    ]
    for word in preferred_words:
        for column in columns:
            if word in str(column).lower():
                unique_count = data[column].nunique(dropna=True)
                if 2 <= unique_count <= 20:
                    category = column
                    break
        if category is not None:
            break

    # Otherwise use the first suitable categorical column.
    if category is None:
        for column in columns:
            unique_count = data[column].nunique(dropna=True)
            if 2 <= unique_count <= 20:
                category = column
                break

    if category is None:
        return None

    counts = data[category].dropna().astype(str).value_counts().head(10)
    if counts.empty:
        return None

    figure = Figure(figsize=(9, 6))
    axes = figure.subplots()
    axes.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=[
            "#a1c9f4", "#ffb482", "#8de5a1", "#ff9f9b", "#d0bbff",
            "#debb9b", "#fab0e4", "#cfcfcf", "#fffea3", "#b9f2f0"
        ]
    )
    axes.set_title(f"Top categories: {category}", fontsize=15, fontweight="bold")
    axes.axis("equal")

    project_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(project_dir, "static", "img", "grafica.png")
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    figure.savefig(image_path, format="png", bbox_inches="tight")
    return image_path

