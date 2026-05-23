import Fastify from 'fastify';
import cors from '@fastify/cors';
import { PrismaClient } from '@prisma/client';

const app = Fastify({
  logger: true
});

const prisma = new PrismaClient();

app.register(cors, {
  origin: '*'
});

// Ruta raíz con documentación detallada
app.get('/', async (request, reply) => {
  return {
    name: 'Venezuela API',
    version: '1.0.0',
    description: 'API REST con información geográfica, política y turística de Venezuela 🇻🇪',
    base_url: 'https://venezuela-api-two.vercel.app',
    source_code: 'https://github.com/armandozabala/venezuela-api',
    endpoints: [
      {
        method: 'GET',
        path: '/health',
        description: 'Verifica que la API esté en línea',
        example_response: { status: 'ok', message: 'Venezuela API is running' },
      },
      {
        method: 'GET',
        path: '/api/states',
        description: 'Retorna todos los estados de Venezuela con sus imágenes',
        example_response: [
          { id: 1, name: 'Amazonas', capital: 'Puerto Ayacucho', region: 'Sur', population: 180000 }
        ],
      },
      {
        method: 'GET',
        path: '/api/states/:id',
        description: 'Retorna un estado específico con sus ciudades, municipios e imágenes',
        params: { id: 'ID numérico del estado (1-24)' },
        example: '/api/states/1',
      },
      {
        method: 'GET',
        path: '/api/cities',
        description: 'Retorna las primeras 50 ciudades con su estado relacionado',
        example_response: [
          { id: 1, name: 'Caracas', is_capital: true, state: { name: 'Distrito Capital' } }
        ],
      },
      {
        method: 'GET',
        path: '/api/cities/:id',
        description: 'Retorna una ciudad específica con su estado e imágenes',
        params: { id: 'ID numérico de la ciudad' },
        example: '/api/cities/1',
      },
      {
        method: 'GET',
        path: '/api/search',
        description: 'Busca estados y ciudades por nombre',
        query_params: { q: 'Texto a buscar (requerido)' },
        example: '/api/search?q=Caracas',
      },
    ],
  };
});

// Ruta básica para chequear salud
app.get('/health', async (request, reply) => {
  return { status: 'ok', message: 'Venezuela API is running' };
});

// Endpoints para Estados
app.get('/api/states', async (request, reply) => {
  const states = await prisma.state.findMany({
    include: { images: true }
  });
  return states;
});

app.get('/api/states/:id', async (request, reply) => {
  const { id } = request.params as { id: string };
  const state = await prisma.state.findUnique({
    where: { id: parseInt(id) },
    include: {
      images: true,
      cities: true,
      municipalities: true
    }
  });
  if (!state) return reply.status(404).send({ error: 'Estado no encontrado' });
  return state;
});

// Endpoints para Ciudades
app.get('/api/cities', async (request, reply) => {
  const cities = await prisma.city.findMany({
    take: 50,
    include: { state: true }
  });
  return cities;
});

app.get('/api/cities/:id', async (request, reply) => {
  const { id } = request.params as { id: string };
  const city = await prisma.city.findUnique({
    where: { id: parseInt(id) },
    include: { state: true, images: true }
  });
  if (!city) return reply.status(404).send({ error: 'Ciudad no encontrada' });
  return city;
});

// Buscador
app.get('/api/search', async (request, reply) => {
  const { q } = request.query as { q: string };
  if (!q) return reply.status(400).send({ error: 'Falta el parámetro q' });

  const states = await prisma.state.findMany({
    where: { name: { contains: q } }
  });
  const cities = await prisma.city.findMany({
    where: { name: { contains: q } },
    take: 10
  });

  return { states, cities };
});

export default app;
