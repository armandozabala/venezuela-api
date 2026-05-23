import { PrismaClient } from '@prisma/client';
import fs from 'fs';
import path from 'path';

const prisma = new PrismaClient();

async function main() {
  console.log('Seeding database...');
  
  const dataDir = path.join(__dirname, '../data');
  
  // 1. Leer archivos JSON
  const states = JSON.parse(fs.readFileSync(path.join(dataDir, 'states.json'), 'utf-8'));
  const municipalities = JSON.parse(fs.readFileSync(path.join(dataDir, 'municipalities.json'), 'utf-8'));
  const cities = JSON.parse(fs.readFileSync(path.join(dataDir, 'cities.json'), 'utf-8'));
  const parishes = JSON.parse(fs.readFileSync(path.join(dataDir, 'parishes.json'), 'utf-8'));
  const images = JSON.parse(fs.readFileSync(path.join(dataDir, 'images.json'), 'utf-8'));

  // 2. Insertar Estados
  console.log(`Inserting ${states.length} states...`);
  for (const s of states) {
    const img = images.find((i: any) => i.state === s.name);
    await prisma.state.upsert({
      where: { id: s.id },
      update: {
        cover_image_url: img ? img.url : null,
        description: s.description,
        surface: s.surface,
        population: s.population,
        phone_prefix: s.phone_prefix,
        region: s.region
      },
      create: {
        id: s.id,
        name: s.name,
        capital: s.capital,
        cover_image_url: img ? img.url : null,
        description: s.description,
        surface: s.surface,
        population: s.population,
        phone_prefix: s.phone_prefix,
        region: s.region
      }
    });
  }

  // 3. Insertar Municipios
  console.log(`Inserting ${municipalities.length} municipalities...`);
  await prisma.municipality.createMany({
    data: municipalities.map((m: any) => ({
      id: m.id,
      name: m.name,
      state_id: m.state_id
    })),
    skipDuplicates: true,
  });

  // 4. Insertar Ciudades
  console.log(`Inserting ${cities.length} cities...`);
  await prisma.city.createMany({
    data: cities.map((c: any) => ({
      id: c.id,
      name: c.name,
      state_id: c.state_id
    })),
    skipDuplicates: true,
  });

  // 5. Insertar Parroquias
  console.log(`Inserting ${parishes.length} parishes...`);
  // Insertar en lotes si son muchas (SQLite/MySQL pueden tener límites de placeholders)
  const chunkSize = 1000;
  for (let i = 0; i < parishes.length; i += chunkSize) {
    const chunk = parishes.slice(i, i + chunkSize);
    await prisma.parish.createMany({
      data: chunk.map((p: any) => ({
        id: p.id,
        name: p.name,
        municipality_id: p.municipality_id
      })),
      skipDuplicates: true,
    });
  }
  
  // 6. Insertar Imágenes como registro
  console.log(`Inserting images...`);
  for (const img of images) {
    const state = await prisma.state.findUnique({ where: { name: img.state } });
    if (state) {
      await prisma.locationImage.create({
        data: {
          url: img.url,
          location_type: 'State',
          state_id: state.id,
          description: `Bandera del estado ${state.name}`
        }
      });
    }
  }

  console.log('Seeding finished.');
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
