from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.openapi.docs import get_swagger_ui_html
from pathlib import Path
import tempfile

from converter import convert_csv_to_json, convert_json_to_csv

# App FastAPI avec docs custom
app = FastAPI(
    title="CSV & JSON Converter API",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
)


# --- Root & Docs -------------------------------------------------------------


@app.get("/")
async def root():
    return {"status": "ok", "message": "CSV & JSON API is running"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="CSV & JSON Converter API - Docs",
    )


# --- CSV -> JSON ------------------------------------------------------------


@app.post("/convert", summary="Convert CSV to JSON")
async def convert_csv_endpoint(
    file: UploadFile = File(..., description="Fichier CSV à convertir"),
    delimiter: str = Query(",", max_length=1, description="Séparateur CSV (1 caractère)"),
    encoding: str = Query("utf-8", description="Encodage du fichier CSV"),
    has_header: bool = Query(
        True,
        description="Le CSV contient-il une ligne d'en-tête ?",
    ),
    pretty: bool = Query(
        False,
        description="Retourner le JSON indenté (lisible) plutôt que compact",
    ),
):
    """
    Convertit un fichier **CSV** en **JSON**.

    Retourne :
    - `filename` : nom du fichier JSON généré
    - `rows_count` : nombre de lignes de données
    - `warning` : éventuel message d'avertissement
    - `data` : liste d'objets (parsed JSON)
    - `data_string` : JSON sérialisé (string)
    """
    # 1. Sauvegarde temporaire du fichier CSV uploadé
    suffix = Path(file.filename or "").suffix or ".csv"
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_input.write(await file.read())
    temp_input.close()

    # 2. Conversion CSV -> JSON
    try:
        out_path, rows_count, warning, data = convert_csv_to_json(
            temp_input.name,
            delimiter=delimiter,
            encoding=encoding,
            has_header=has_header,
            pretty=pretty,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 3. Lecture du JSON généré en texte
    json_text = out_path.read_text(encoding="utf-8")

    return {
        "filename": out_path.name,
        "rows_count": rows_count,
        "warning": warning,
        "data": data,
        "data_string": json_text,
    }


# --- JSON -> CSV ------------------------------------------------------------


@app.post("/json-to-csv", summary="Convert JSON to CSV")
async def json_to_csv_endpoint(
    file: UploadFile = File(..., description="Fichier JSON à convertir"),
    delimiter: str = Query(",", max_length=1, description="Séparateur CSV (1 caractère)"),
    encoding: str = Query("utf-8", description="Encodage du fichier JSON"),
    has_header: bool = Query(
        True,
        description="Si JSON = liste d'objets, écrire une ligne d'en-tête",
    ),
):
    """
    Convertit un fichier **JSON** en **CSV**.

    Le JSON doit être :
    - soit une liste d'objets : `[{"a": 1, "b": 2}, ...]`
    - soit une liste de tableaux : `[[1, 2], [3, 4]]`
    """
    # 1. Lecture + décodage
    raw_bytes = await file.read()
    try:
        json_text = raw_bytes.decode(encoding)
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail=f"Impossible de décoder le fichier avec l'encodage '{encoding}'.",
        )

    # 2. Conversion JSON -> CSV
    try:
        out_path, rows_count, warning = convert_json_to_csv(
            json_text=json_text,
            delimiter=delimiter,
            has_header=has_header,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 3. Lecture du CSV généré
    csv_text = out_path.read_text(encoding="utf-8")

    return {
        "filename": out_path.name,
        "rows_count": rows_count,
        "warning": warning,
        "csv": csv_text,
    }
