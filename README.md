# Venezuela API 🇻🇪

Una API REST abierta y colaborativa que proporciona información geográfica detallada de Venezuela.

🌐 **Documentación en vivo:** [https://venezuela-api-two.vercel.app](https://venezuela-api-two.vercel.app)

[![Live](https://img.shields.io/badge/🟢%20API-En%20l%C3%ADnea-brightgreen)](https://venezuela-api-two.vercel.app)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)](https://venezuela-api-two.vercel.app)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/armandozabala/venezuela-api)
[![License](https://img.shields.io/badge/license-ISC-green)](./LICENSE)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red)](https://github.com/armandozabala/venezuela-api)

🔗 **Base URL:** `https://venezuela-api-two.vercel.app`

---

## 📦 Contenido de la base de datos

- 24 Estados (23 + Distrito Capital)
- 335 Municipios
- 1136 Parroquias
- Ciudades y Capitales
- Imágenes representativas (banderas, escudos, locaciones)

## 🛠️ Tecnologías

- **Runtime:** Node.js & TypeScript
- **Framework:** Fastify
- **ORM:** Prisma
- **Base de datos:** MySQL (Aiven Cloud)
- **Deploy:** Vercel

---

## 📖 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Documentación de la API |
| `GET` | `/health` | Estado de la API |
| `GET` | `/api/states` | Todos los estados |
| `GET` | `/api/states/:id` | Un estado específico |
| `GET` | `/api/cities` | Primeras 50 ciudades |
| `GET` | `/api/cities/:id` | Una ciudad específica |
| `GET` | `/api/search?q=texto` | Buscador de estados y ciudades |

---

## 🚀 Ejemplos de uso

### `GET /api/states` — Listar todos los estados

**cURL:**
```bash
curl https://venezuela-api-two.vercel.app/api/states
```

**JavaScript (fetch):**
```js
const response = await fetch('https://venezuela-api-two.vercel.app/api/states');
const states = await response.json();
console.log(states);
```

**JavaScript (axios):**
```js
import axios from 'axios';

const { data } = await axios.get('https://venezuela-api-two.vercel.app/api/states');
console.log(data);
```

**Python (requests):**
```python
import requests

response = requests.get('https://venezuela-api-two.vercel.app/api/states')
states = response.json()
print(states)
```

**Respuesta esperada:**
```json
[
  {
    "id": 1,
    "name": "Amazonas",
    "capital": "Puerto Ayacucho",
    "description": "Estado ubicado al sur de Venezuela...",
    "surface": 180145.0,
    "population": 180000,
    "phone_prefix": "0248",
    "region": "Sur",
    "cover_image_url": "https://...",
    "images": []
  }
]
```

---

### `GET /api/states/:id` — Obtener un estado específico

**cURL:**
```bash
curl https://venezuela-api-two.vercel.app/api/states/1
```

**JavaScript (fetch):**
```js
const id = 1;
const response = await fetch(`https://venezuela-api-two.vercel.app/api/states/${id}`);
const state = await response.json();
console.log(state);
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "name": "Amazonas",
  "capital": "Puerto Ayacucho",
  "region": "Sur",
  "cities": [
    { "id": 5, "name": "Puerto Ayacucho", "is_capital": true }
  ],
  "municipalities": [
    { "id": 12, "name": "Atures" }
  ],
  "images": []
}
```

---

### `GET /api/cities` — Listar ciudades

**cURL:**
```bash
curl https://venezuela-api-two.vercel.app/api/cities
```

**JavaScript (fetch):**
```js
const response = await fetch('https://venezuela-api-two.vercel.app/api/cities');
const cities = await response.json();
console.log(cities);
```

**Respuesta esperada:**
```json
[
  {
    "id": 1,
    "name": "Caracas",
    "is_capital": true,
    "population": 2900000,
    "state": {
      "id": 9,
      "name": "Distrito Capital"
    }
  }
]
```

---

### `GET /api/search?q=texto` — Buscador

**cURL:**
```bash
curl "https://venezuela-api-two.vercel.app/api/search?q=Caracas"
```

**JavaScript (fetch):**
```js
const query = 'Caracas';
const response = await fetch(`https://venezuela-api-two.vercel.app/api/search?q=${query}`);
const results = await response.json();
console.log(results);
```

**Python (requests):**
```python
import requests

response = requests.get(
    'https://venezuela-api-two.vercel.app/api/search',
    params={'q': 'Caracas'}
)
results = response.json()
print(results)
```

**Respuesta esperada:**
```json
{
  "states": [],
  "cities": [
    {
      "id": 1,
      "name": "Caracas",
      "is_capital": true
    }
  ]
}
```

---

## 💻 Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/armandozabala/venezuela-api.git
cd venezuela-api

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
# Crea un archivo .env con tu conexión de MySQL
echo 'DATABASE_URL="mysql://root:@localhost:3306/venezuela_api"' > .env

# 4. Aplicar esquema de base de datos
npx prisma db push

# 5. Poblar la base de datos
npx prisma db seed

# 6. Iniciar en modo desarrollo
npm run dev
```

El servidor correrá en `http://localhost:3000`.

---

## ❤️ ¿Cómo contribuir? (Open Source)

La base de datos se alimenta directamente de los archivos JSON alojados en la carpeta `data/`.
Si deseas agregar una foto, actualizar el nombre de una parroquia, o agregar más metadatos culturales:

1. Haz un **Fork** de este repositorio.
2. Edita los archivos dentro de `data/` (por ejemplo, `data/cities.json` o `data/images.json`).
3. Crea un **Pull Request** (PR).
4. ¡Una vez aprobado, el script de *seed* actualizará producción automáticamente!

¡Gracias por ayudar a construir la API de nuestro país! 🇻🇪
