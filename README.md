# Venezuela API 🇻🇪

Una API REST abierta y colaborativa que proporciona información geográfica detallada de Venezuela, incluyendo:
- 23 Estados + Distrito Capital
- 335 Municipios
- 1136 Parroquias
- Ciudades y Capitales
- Imágenes representativas (Banderas, escudos, locaciones).

## Tecnologías
- Node.js & TypeScript
- Fastify
- Prisma ORM
- MySQL

## ¿Cómo contribuir? (Open Source) ❤️
La base de datos se alimenta directamente de los archivos JSON alojados en la carpeta `data/`.
Si deseas agregar una nueva foto, actualizar el nombre de una parroquia, o agregar más metadatos culturales a una ciudad:

1. Haz un **Fork** de este repositorio.
2. Edita los archivos dentro de la carpeta `data/` (por ejemplo, `data/cities.json` o `data/images.json`).
3. Crea un **Pull Request** (PR).
4. ¡Listo! Una vez aprobado, nuestro script de *seed* alimentará la base de datos de producción con tus cambios.

## Instalación Local

```bash
# 1. Instalar dependencias
npm install

# 2. Configurar base de datos
# Copia el archivo .env.example a .env y coloca tu conexión de MySQL
# DATABASE_URL="mysql://root:@localhost:3306/venezuela_api"

# 3. Aplicar migraciones de base de datos
npx prisma migrate dev --name init

# 4. Poblar la base de datos con la información de los JSON
npx prisma db seed

# 5. Iniciar en modo desarrollo
npm run dev
```

## Endpoints Principales

- `GET /api/states` - Lista todos los estados de Venezuela.
- `GET /api/states/:id` - Detalles de un estado (incluye ciudades y municipios).
- `GET /api/cities` - Lista de ciudades.
- `GET /api/cities/:id` - Detalle de una ciudad.
- `GET /api/search?q=nombre` - Buscador general de estados y ciudades.

¡Gracias por ayudar a construir la API de nuestro país! 🇻🇪
