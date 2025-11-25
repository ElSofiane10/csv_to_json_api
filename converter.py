from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# CSV -> JSON
# ---------------------------------------------------------------------------


def convert_csv_to_json(
    csv_path: str | Path,
    *,
    delimiter: str = ",",
    encoding: str = "utf-8",
    has_header: bool = True,
    pretty: bool = False,
) -> tuple[Path, int, str | None, list[dict[str, Any]]]:
    """
    Convertit un fichier CSV en JSON.

    - csv_path : chemin du fichier CSV
    - delimiter : séparateur CSV
    - encoding : encodage du CSV
    - has_header : True si la première ligne contient les noms de colonnes
    - pretty : True pour indenter le JSON

    Retourne (json_path, rows_count, warning, data_list)
    """
    csv_path = Path(csv_path)

    try:
        f = csv_path.open("r", encoding=encoding, newline="")
    except FileNotFoundError as e:
        raise ValueError(f"Fichier CSV introuvable : {csv_path}") from e

    with f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        raise ValueError("Le fichier CSV est vide.")

    warning: str | None = None
    data: list[dict[str, Any]] = []

    if has_header:
        header = rows[0]
        if not header:
            raise ValueError("La ligne d'en-tête du CSV est vide.")

        for idx, row in enumerate(rows[1:], start=2):
            if len(row) != len(header):
                warning = (
                    "Certaines lignes n'ont pas le même nombre de colonnes que l'en-tête. "
                    "Les valeurs manquantes sont complétées par des chaînes vides."
                )
            # Ajustement : tronquer ou compléter avec ""
            row = (row + [""] * len(header))[: len(header)]
            obj = {header[i]: row[i] for i in range(len(header))}
            data.append(obj)
    else:
        # Pas d'en-tête : on crée des noms de colonnes génériques
        max_len = max(len(r) for r in rows)
        header = [f"col_{i+1}" for i in range(max_len)]
        warning = (
            "CSV sans en-tête : des noms de colonnes génériques col_1, col_2, ... ont été utilisés."
        )
        for idx, row in enumerate(rows, start=1):
            row = (row + [""] * max_len)[:max_len]
            obj = {header[i]: row[i] for i in range(max_len)}
            data.append(obj)

    rows_count = len(data)

    # Écriture dans un fichier JSON temporaire
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=".json", mode="w", encoding="utf-8"
    )
    if pretty:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
    else:
        json.dump(data, tmp, ensure_ascii=False, separators=(",", ":"))
    tmp.close()

    return Path(tmp.name), rows_count, warning, data


# ---------------------------------------------------------------------------
# JSON -> CSV
# ---------------------------------------------------------------------------


def convert_json_to_csv(
    json_text: str,
    *,
    delimiter: str = ",",
    has_header: bool = True,
) -> tuple[Path, int, str | None]:
    """
    Convertit une liste JSON en CSV.

    - json_text doit représenter soit :
        * une liste d'objets : [{...}, {...}]
        * une liste de listes  : [[...], [...]]
    - delimiter : séparateur CSV ("," par défaut)
    - has_header : si True et liste d'objets -> écrit une ligne d'en-tête

    Retourne : (chemin_fichier_csv, rows_count, warning)
    """
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide : {e}") from e

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("Le JSON doit être une liste non vide (d'objets ou de tableaux).")

    warning: str | None = None
    rows_count = 0

    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=".csv", mode="w", newline="", encoding="utf-8"
    )
    writer = csv.writer(tmp, delimiter=delimiter)

    first = data[0]

    # Cas 1 : liste d'objets
    if isinstance(first, dict):
        # union de toutes les clés dans l'ordre d'apparition
        keys: list[str] = []
        seen = set()
        for obj in data:
            if not isinstance(obj, dict):
                raise ValueError("Tous les éléments doivent être des objets JSON (dict).")
            for k in obj.keys():
                if k not in seen:
                    seen.add(k)
                    keys.append(k)

        if has_header:
            writer.writerow(keys)

        for obj in data:
            row = [obj.get(k, "") for k in keys]
            writer.writerow(row)
            rows_count += 1

    # Cas 2 : liste de listes / tuples
    elif isinstance(first, (list, tuple)):
        if has_header:
            warning = "has_header=true est ignoré pour une liste de tableaux."
        for row in data:
            if not isinstance(row, (list, tuple)):
                raise ValueError(
                    "Tous les éléments doivent être des tableaux si le premier est un tableau."
                )
            writer.writerow(list(row))
            rows_count += 1
    else:
        raise ValueError(
            "Le JSON doit être une liste d'objets ({...}) ou une liste de tableaux ([...])."
        )

    tmp.close()
    return Path(tmp.name), rows_count, warning
