import json
import urllib.request
import urllib.parse
import os
import time

# Datos enriquecidos (aproximados a 2023)
extra_data = {
    "Amazonas": {"population": 200000, "surface": 177617, "region": "Región Guayana", "phone_prefix": "0248"},
    "Anzoátegui": {"population": 1754000, "surface": 43300, "region": "Región Nor-Oriental", "phone_prefix": "0281"},
    "Apure": {"population": 650000, "surface": 76500, "region": "Región de los Llanos", "phone_prefix": "0247"},
    "Aragua": {"population": 1850000, "surface": 7014, "region": "Región Central", "phone_prefix": "0243"},
    "Barinas": {"population": 950000, "surface": 35200, "region": "Región de los Andes", "phone_prefix": "0273"},
    "Bolívar": {"population": 1850000, "surface": 240528, "region": "Región Guayana", "phone_prefix": "0285"},
    "Carabobo": {"population": 2500000, "surface": 4650, "region": "Región Central", "phone_prefix": "0241"},
    "Cojedes": {"population": 370000, "surface": 14800, "region": "Región Central", "phone_prefix": "0258"},
    "Delta Amacuro": {"population": 200000, "surface": 40200, "region": "Región Guayana", "phone_prefix": "0287"},
    "Falcón": {"population": 1100000, "surface": 24800, "region": "Región Centro Occidental", "phone_prefix": "0268"},
    "Guárico": {"population": 950000, "surface": 64986, "region": "Región de los Llanos", "phone_prefix": "0246"},
    "Lara": {"population": 2050000, "surface": 19800, "region": "Región Centro Occidental", "phone_prefix": "0251"},
    "Mérida": {"population": 1050000, "surface": 11300, "region": "Región de los Andes", "phone_prefix": "0274"},
    "Miranda": {"population": 3300000, "surface": 7950, "region": "Región Capital", "phone_prefix": "0212"},
    "Monagas": {"population": 1050000, "surface": 28900, "region": "Región Nor-Oriental", "phone_prefix": "0291"},
    "Nueva Esparta": {"population": 600000, "surface": 1150, "region": "Región Insular", "phone_prefix": "0295"},
    "Portuguesa": {"population": 1050000, "surface": 15200, "region": "Región Centro Occidental", "phone_prefix": "0255"},
    "Sucre": {"population": 1100000, "surface": 11800, "region": "Región Nor-Oriental", "phone_prefix": "0293"},
    "Táchira": {"population": 1300000, "surface": 11100, "region": "Región de los Andes", "phone_prefix": "0276"},
    "Trujillo": {"population": 870000, "surface": 7400, "region": "Región de los Andes", "phone_prefix": "0271"},
    "La Guaira": {"population": 380000, "surface": 1496, "region": "Región Capital", "phone_prefix": "0212"},
    "Yaracuy": {"population": 750000, "surface": 7100, "region": "Región Centro Occidental", "phone_prefix": "0254"},
    "Zulia": {"population": 4300000, "surface": 63100, "region": "Región Zuliana", "phone_prefix": "0261"},
    "Distrito Capital": {"population": 2100000, "surface": 433, "region": "Región Capital", "phone_prefix": "0212"}
}

def get_wikipedia_summary(state_name):
    # Formatear término de búsqueda
    search_term = f"Estado {state_name}"
    if state_name == "Distrito Capital":
        search_term = "Distrito Capital (Venezuela)"
    elif state_name == "Amazonas":
        search_term = "Estado Amazonas (Venezuela)"
        
    url = f"https://es.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles={urllib.parse.quote(search_term)}&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read()
        data = json.loads(res.decode('utf-8'))
        pages = data['query']['pages']
        for page_id in pages:
            if page_id != "-1":
                return pages[page_id].get('extract', '')
    except Exception as e:
        print(f"Error fetching {state_name}: {e}")
    return ""

states_file = "data/states.json"
with open(states_file, "r", encoding="utf-8") as f:
    states = json.load(f)

for s in states:
    name = s["name"]
    # Fallback to La Guaira if Vargas
    lookup_name = name if name != "Vargas" else "La Guaira"
    
    if lookup_name in extra_data:
        s["population"] = extra_data[lookup_name]["population"]
        s["surface"] = extra_data[lookup_name]["surface"]
        s["region"] = extra_data[lookup_name]["region"]
        s["phone_prefix"] = extra_data[lookup_name]["phone_prefix"]
    
    print(f"Fetching Wikipedia for {lookup_name}...")
    if not s.get("description"):  # Solo buscar si no tiene descripción
        time.sleep(1) # Pausa para evitar error 429
        desc = get_wikipedia_summary(lookup_name)
        s["description"] = desc

with open(states_file, "w", encoding="utf-8") as f:
    json.dump(states, f, ensure_ascii=False, indent=2)

print("¡Estados enriquecidos con éxito!")
