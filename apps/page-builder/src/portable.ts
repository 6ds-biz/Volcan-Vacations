import {exportPage, keys, object, validatePage, type MediaConfig, type Page, type Section} from '@6ds/page-builder/core';
import type {ProjectDefinition} from './project';

/** Version 1 envelope. Focal x/y are normalized to [0,1] on the wire. */
export type PortableLayout = {schema_version: 1; project: string; page_type: string; sections: Section[]};
function pageDefinition(project: ProjectDefinition, pageType: string) {
  const definition = project.pages.find(p => p.id === pageType);
  if (!definition) throw Error(`Unknown page type: ${pageType}.`);
  return definition;
}
function mediaConfigs(page: Page) {
  return page.sections.flatMap(s => s.columns.flatMap(c => c.widgets.flatMap(w =>
    w.type === 'media' ? [w.config as unknown as MediaConfig] : w.config.media ? [w.config.media as MediaConfig] : [])));
}
function validateReferences(page: Page, project: ProjectDefinition) {
  for (const media of mediaConfigs(page)) {
    for (const ref of [media.asset, media.poster, media.tablet.asset, media.mobile.asset]) {
      if (!ref) continue;
      const asset = project.media.getSync?.(ref);
      if (!asset || asset.rights_status !== 'APPROVED' || !project.media.validateSource(asset)) throw Error(`Media reference is not approved for this project: ${ref}.`);
      if (ref === media.poster && asset.type !== 'image') throw Error('A poster must reference an image.');
    }
    if (media.asset && !media.decorative && !(media.alt.trim() || project.media.getSync?.(media.asset)?.alt.trim())) throw Error('Meaningful images need alt text.');
  }
  // Public copy only. The project provides its canonical public contact.
  for (const email of JSON.stringify(page).match(/[\w.+-]+@[\w.-]+\.[a-z]{2,}/gi) || []) {
    if (email.toLowerCase() !== project.publicEmail) throw Error('Use only the project’s canonical public contact email in layouts.');
  }
}
export function validateLayout(page: unknown, project: ProjectDefinition, pageType: string): Page {
  pageDefinition(project, pageType);
  const valid = validatePage(page, project.registry(pageType), project.defaults(pageType).page_id);
  validateReferences(valid, project);
  return valid;
}
function focalCoordinates(page: Page, importing: boolean) {
  for (const media of mediaConfigs(page)) for (const crop of [media, media.tablet, media.mobile]) {
    for (const key of ['x', 'y'] as const) if (crop[key] !== undefined) {
      const value = crop[key]!;
      if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > (importing ? 1 : 100)) throw Error('Focal coordinates must be normalized between 0 and 1.');
      crop[key] = Number((importing ? value * 100 : value / 100).toFixed(10));
    }
  }
}
function canonical(value: unknown): unknown {
  return Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object'
    ? Object.fromEntries(Object.entries(value).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => [k, canonical(v)])) : value;
}
export function serializeLayout(page: Page, project: ProjectDefinition, pageType: string) {
  const valid = validateLayout(page, project, pageType);
  // Reuse the core's deterministic serialization before adding portable metadata.
  const normalized = JSON.parse(exportPage(valid, project.registry(pageType))) as Page;
  focalCoordinates(normalized, false);
  const portable: PortableLayout = {schema_version: 1, project: project.id, page_type: pageType, sections: normalized.sections};
  const result = JSON.stringify(canonical(portable), null, 2) + '\n';
  if (new TextEncoder().encode(result).length > 100000) throw Error('Layout JSON exceeds 100 KB.');
  return result;
}
export function parseLayout(raw: string, project: ProjectDefinition, pageType: string) {
  if (new TextEncoder().encode(raw).length > 100000) throw Error('Layout JSON exceeds 100 KB.');
  let value: unknown;
  try { value = JSON.parse(raw); } catch { throw Error('Invalid JSON. Choose a complete exported layout file.'); }
  object(value);
  keys(value, ['schema_version', 'project', 'page_type', 'sections']);
  if (value.schema_version !== 1) throw Error('Unsupported layout schema version. Expected version 1.');
  if (value.project !== project.id) throw Error(`This layout belongs to a different project. Expected ${project.id}.`);
  if (value.page_type !== pageType) throw Error(`This layout belongs to ${String(value.page_type)}. Select that page before importing.`);
  pageDefinition(project, pageType);
  // Validate nesting and config before walking media, then convert and validate again.
  const page = validatePage({schema_version: 1, page_id: project.defaults(pageType).page_id, sections: value.sections}, project.registry(pageType));
  focalCoordinates(page, true);
  return validateLayout(page, project, pageType);
}
