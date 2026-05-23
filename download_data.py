import os
import json
import urllib.request

# 1. Descargar la data base de zokeber
url = "https://raw.githubusercontent.com/zokeber/venezuela-json/master/venezuela.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
data = json.loads(response.read().decode('utf-8'))

states = []
municipalities = []
cities = []
parishes = []

state_id = 1
muni_id = 1
city_id = 1
parish_id = 1

for s in data:
    s_name = s.get("estado")
    iso = s.get("iso_31662", "")
    states.append({"id": state_id, "name": s_name, "capital": "Capital por definir", "iso_31662": iso}) # Add a generic capital for now if missing
    
    for c_name in s.get("ciudades", []):
        cities.append({"id": city_id, "state_id": state_id, "name": c_name})
        city_id += 1
        
    for m in s.get("municipios", []):
        m_name = m.get("municipio")
        municipalities.append({"id": muni_id, "state_id": state_id, "name": m_name})
        
        for p_name in m.get("parroquias", []):
            parishes.append({"id": parish_id, "municipality_id": muni_id, "name": p_name})
            parish_id += 1
            
        muni_id += 1
        
    state_id += 1

# 2. URLs de imágenes representativas (Banderas en Wikimedia Commons)
images = [
    {"state": "Amazonas", "url": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Amazonas_State.svg"},
    {"state": "Anzoátegui", "url": "https://upload.wikimedia.org/wikipedia/commons/8/87/Flag_of_Anzo%C3%A1tegui_State.svg"},
    {"state": "Apure", "url": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Flag_of_Apure_State.svg"},
    {"state": "Aragua", "url": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_of_Aragua_State.svg"},
    {"state": "Barinas", "url": "https://upload.wikimedia.org/wikipedia/commons/e/ed/Flag_of_Barinas_State.svg"},
    {"state": "Bolívar", "url": "https://upload.wikimedia.org/wikipedia/commons/2/28/Flag_of_Bol%C3%ADvar_State.svg"},
    {"state": "Carabobo", "url": "https://upload.wikimedia.org/wikipedia/commons/5/52/Flag_of_Carabobo_State.svg"},
    {"state": "Cojedes", "url": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Flag_of_Cojedes_State.svg"},
    {"state": "Delta Amacuro", "url": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Flag_of_Delta_Amacuro_State.svg"},
    {"state": "Falcón", "url": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Flag_of_Falc%C3%B3n_State.svg"},
    {"state": "Guárico", "url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Flag_of_Gu%C3%A1rico_State.svg"},
    {"state": "Lara", "url": "https://upload.wikimedia.org/wikipedia/commons/6/69/Flag_of_Lara_State.svg"},
    {"state": "Mérida", "url": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Flag_of_M%C3%A9rida_State.svg"},
    {"state": "Miranda", "url": "https://upload.wikimedia.org/wikipedia/commons/2/23/Flag_of_Miranda_state.svg"},
    {"state": "Monagas", "url": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Flag_of_Monagas_State.svg"},
    {"state": "Nueva Esparta", "url": "https://upload.wikimedia.org/wikipedia/commons/8/88/Flag_of_Nueva_Esparta.svg"},
    {"state": "Portuguesa", "url": "https://upload.wikimedia.org/wikipedia/commons/1/17/Flag_of_Portuguesa.svg"},
    {"state": "Sucre", "url": "https://upload.wikimedia.org/wikipedia/commons/1/14/Flag_of_Sucre_State.svg"},
    {"state": "Táchira", "url": "https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_T%C3%A1chira.svg"},
    {"state": "Trujillo", "url": "https://upload.wikimedia.org/wikipedia/commons/0/07/Flag_of_Trujillo_State.svg"},
    {"state": "La Guaira", "url": "https://upload.wikimedia.org/wikipedia/commons/6/60/Flag_of_Vargas_State.svg"},
    {"state": "Yaracuy", "url": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Flag_of_Yaracuy_State.svg"},
    {"state": "Zulia", "url": "https://upload.wikimedia.org/wikipedia/commons/1/10/Flag_of_Zulia_State.svg"},
    {"state": "Distrito Capital", "url": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Flag_of_Caracas.svg"}
]

# 3. Crear directorio y archivos
output_dir = "/Users/armandozabala/Documents/proyectos/venezuela-api/data/"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "states.json"), "w", encoding="utf-8") as f:
    json.dump(states, f, ensure_ascii=False, indent=2)
    
with open(os.path.join(output_dir, "municipalities.json"), "w", encoding="utf-8") as f:
    json.dump(municipalities, f, ensure_ascii=False, indent=2)
    
with open(os.path.join(output_dir, "cities.json"), "w", encoding="utf-8") as f:
    json.dump(cities, f, ensure_ascii=False, indent=2)
    
with open(os.path.join(output_dir, "parishes.json"), "w", encoding="utf-8") as f:
    json.dump(parishes, f, ensure_ascii=False, indent=2)

with open(os.path.join(output_dir, "images.json"), "w", encoding="utf-8") as f:
    json.dump(images, f, ensure_ascii=False, indent=2)

print(f"Archivos JSON estructurados generados en: {output_dir}")
