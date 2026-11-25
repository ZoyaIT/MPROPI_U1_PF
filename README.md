# Tauler d'accidents de trànsit a Barcelona

Un projecte desenvolupat amb Flask, Jinja, Pandas i Matplotlib.

## 1. Conjunt de dades

Descarregueu un fitxer CSV amb els accidents gestionats per la Guàrdia Urbana des del
Portal de Dades Obertes de l'Ajuntament de Barcelona:

https://opendata-ajuntament.barcelona.cat/data/es/dataset/accidents-gu-bcn

Trieu un fitxer CSV anual i deseu-lo com a:

`data/accidents.csv`

## 2. Instal·lació

Obriu el Terminal a la carpeta d'aquest projecte i executeu:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Executar

```bash
python app.py
```

Obre aquesta adreça al teu navegador:

http://127.0.0.1:5000

## 4. Estructura del projecte

- `app.py`: rutes i pàgines de Flask.
- `data.py`: llegeix, filtra i ordena dades en format CSV.
- `charts.py`: crea el gràfic amb Matplotlib.
- `data/accidents.csv`: conjunt de dades públic descarregat.
- `templates/index.html`: pàgina Jinja.
- `static/css/style.css`: estils de la pàgina.
- `static/img/`: gràfic generat.

El tauler de control cerca en totes les columnes, filtra per una columna seleccionada,
ordena els registres i mostra fins a 100 files alhora.
