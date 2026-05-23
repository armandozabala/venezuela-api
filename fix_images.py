import json
import urllib.request
import urllib.parse
import time

states_file = "data/states.json"
with open(states_file, "r", encoding="utf-8") as f:
    states = json.load(f)

images = []

def get_wiki_image(title):
    url = f"https://es.wikipedia.org/w/api.php?action=query&prop=pageimages&pithumbsize=1000&titles={urllib.parse.quote(title)}&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read()
        data = json.loads(res.decode('utf-8'))
        pages = data.get('query', {}).get('pages', {})
        for page_id in pages:
            if page_id != "-1":
                return pages[page_id].get('thumbnail', {}).get('source', '')
    except Exception as e:
        print(f"Error fetching image for {title}: {e}")
    return ""

for s in states:
    state_name = s["name"]
    capital = s.get("capital", "")
    
    # Intenta buscar la foto de la capital primero
    search_term = capital if capital and capital != "Capital por definir" else f"Estado {state_name}"
    
    # Algunas excepciones para que devuelva fotos buenas
    if state_name == "Distrito Capital":
        search_term = "Caracas"
    elif state_name == "Vargas" or state_name == "La Guaira":
        search_term = "La Guaira"
        
    print(f"Fetching image for {search_term}...")
    time.sleep(2) # Evitar 429
    url = get_wiki_image(search_term)
    
    # Fallback si no encuentra
    if not url:
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Collage_Caracas.jpg/960px-Collage_Caracas.jpg"
        
    images.append({
        "state": state_name,
        "url": url
    })

# Guardar en images.json
images_file = "data/images.json"
with open(images_file, "w", encoding="utf-8") as f:
    json.dump(images, f, ensure_ascii=False, indent=2)

print("Imágenes en formato JPG descargadas desde Wikipedia con éxito.")
