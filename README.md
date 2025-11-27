██████╗  █████╗ ████████╗ █████╗ ███████╗ █████╗ ████████╗    ██╗  ██╗██╗   ██╗██████╗ 
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝    ██║  ██║██║   ██║██╔══██╗
██████╔╝███████║   ██║   ███████║█████╗  ███████║   ██║       ███████║██║   ██║██████╔╝
██╔══██╗██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██║   ██║       ██╔══██║██║   ██║██╔══██╗
██████╔╝██║  ██║   ██║   ██║  ██║███████╗██║  ██║   ██║       ██║  ██║╚██████╔╝██║  ██║
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
                     Multi-Format Converter API – DataFormat Hub

DESCRIPTION :
API professionnelle permettant de convertir, nettoyer et transformer des données : CSV, JSON,
Excel (.xlsx), XML, HTML (tables), et texte brut. Optimisée pour l'automatisation, l'ETL,
le scraping, la data science, les pipelines, les dashboards et les services backend.

URL DU SERVICE :
https://dataformat-hub-api.onrender.com

------------------------------------------------------------------------------------------
MODULES INCLUS
------------------------------------------------------------------------------------------
1. CSV → JSON                (POST /csv/to-json)
2. JSON → CSV                (POST /json/to-csv)
3. CSV → Excel (.xlsx)       (POST /csv/to-excel)
4. Excel (.xlsx) → CSV       (POST /excel/to-csv)
5. JSON Formatter            (POST /json/format)
6. XML → JSON                (POST /xml/to-json)
7. JSON → XML                (POST /json/to-xml)
8. HTML Table → JSON         (POST /html-table/to-json)
9. CSV URL → JSON            (POST /csv/url-to-json)
10. Text Cleaner             (POST /text/clean)

------------------------------------------------------------------------------------------
TEST RAPIDE
------------------------------------------------------------------------------------------
curl https://dataformat-hub-api.onrender.com/

Réponse attendue :
{
  "status": "ok",
  "message": "Multi-Format Converter API is running",
  "modules": [...]
}

------------------------------------------------------------------------------------------
EXEMPLES D’UTILISATION
------------------------------------------------------------------------------------------

[1] CSV → JSON
curl -X POST "https://dataformat-hub-api.onrender.com/csv/to-json" \
     -F "file=@test.csv" \
     -F "delimiter=," \
     -F "encoding=utf-8" \
     -F "has_header=true" \
     -F "pretty=false"

[2] JSON Formatter (valider / pretty print)
curl -X POST "https://dataformat-hub-api.onrender.com/json/format" \
     -F "file=@ugly.json" \
     -F "mode=pretty" \
     -F "validate=true"

[3] Text Cleaner
curl -X POST "https://dataformat-hub-api.onrender.com/text/clean" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"  Héllo   Wôrld \\n\"}"

------------------------------------------------------------------------------------------
LIMITES & RESTRICTIONS TECHNIQUES
------------------------------------------------------------------------------------------
- Taille JSON max :            1 MB
- Nombre max de lignes CSV :   100 000
- Encodage par défaut :        UTF-8
- Timeout URL → CSV :          10 s
- Sécurité XML :               profondeur + nombre de nœuds limités
- Erreur →                     code 400 + message clair

------------------------------------------------------------------------------------------
TECHNOLOGIES UTILISÉES
------------------------------------------------------------------------------------------
- FastAPI (backend ultrarapide)
- Uvicorn (serveur ASGI)
- openpyxl (Excel)
- BeautifulSoup4 (HTML)
- lxml (XML)
- httpx (client HTTP async)
- Python 3.x

------------------------------------------------------------------------------------------
LICENCE
------------------------------------------------------------------------------------------
Utilisation libre : personnelle ET commerciale.

© 2025 – DataFormat Hub – API Multi-Format
