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
