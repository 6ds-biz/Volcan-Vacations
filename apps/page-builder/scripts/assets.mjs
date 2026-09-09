import {cp, mkdir} from 'node:fs/promises';
// Copy only public design assets. This is build preparation, not media storage.
for (const folder of ['images', 'fonts', 'branding']) {
  const target = new URL(`../public/${folder}/`, import.meta.url);
  await mkdir(target, {recursive: true});
  await cp(new URL(`../../web/public/${folder}/`, import.meta.url), target, {recursive: true});
}
