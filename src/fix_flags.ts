import mysql from 'mysql2/promise';
import dotenv from 'dotenv';
dotenv.config();

/**
 * Convierte una URL de SVG de Wikimedia Commons a PNG thumbnail.
 * Ejemplo:
 *   https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Amazonas_State.svg
 *   → https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_Amazonas_State.svg/320px-Flag_of_Amazonas_State.svg.png
 */
function svgToPng(url: string): string {
  // Solo procesar URLs de Wikimedia con .svg
  if (!url.includes('upload.wikimedia.org') || !url.endsWith('.svg')) return url;

  // Formato: /wikipedia/commons/HASH1/HASH2/FileName.svg
  const match = url.match(/\/wikipedia\/commons\/([a-f0-9])\/([a-f0-9]{2})\/(.+\.svg)$/);
  if (!match) return url;

  const [, h1, h2, filename] = match;
  return `https://upload.wikimedia.org/wikipedia/commons/thumb/${h1}/${h2}/${filename}/320px-${filename}.png`;
}

async function main() {
  const conn = await mysql.createConnection(process.env.DATABASE_URL!);

  // 1. Obtener todas las imágenes SVG
  const [rows] = await conn.execute(
    "SELECT id, url, state_id FROM LocationImage WHERE url LIKE '%.svg'"
  ) as any;

  console.log(`\n🔍 Encontradas ${rows.length} imágenes SVG en la base de datos.\n`);

  // 2. Agrupar por state_id para detectar duplicados
  const byState: Record<number, any[]> = {};
  for (const row of rows) {
    if (!byState[row.state_id]) byState[row.state_id] = [];
    byState[row.state_id].push(row);
  }

  let updated = 0;
  let deleted = 0;

  for (const [stateId, images] of Object.entries(byState)) {
    // Quedarse con el primero (id más bajo), borrar los demás
    const [keep, ...dupes] = images;

    // Convertir URL SVG → PNG en el que conservamos
    const newUrl = svgToPng(keep.url);
    await conn.execute('UPDATE LocationImage SET url = ? WHERE id = ?', [newUrl, keep.id]);
    console.log(`✅ Estado ${stateId} | Actualizada: ${newUrl}`);
    updated++;

    // Eliminar duplicados
    for (const dupe of dupes) {
      await conn.execute('DELETE FROM LocationImage WHERE id = ?', [dupe.id]);
      deleted++;
    }
  }

  console.log(`\n🎉 Listo! ${updated} banderas actualizadas a PNG. ${deleted} duplicados eliminados.\n`);
  await conn.end();
}

main().catch(console.error);
