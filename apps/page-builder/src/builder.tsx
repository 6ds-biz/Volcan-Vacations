'use client';
import {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import PageEditor from '@6ds/page-builder/editor';
import type {Page} from '@6ds/page-builder/core';
import {parseLayout, serializeLayout} from './portable';
import {vvProject} from './projects/vv';
import type {DesignProject} from './project';

export function Builder({project = vvProject}: {project?: DesignProject}) {
  const [pageType, setPageType] = useState(project.pages[0].id), [generation, setGeneration] = useState(0);
  const working = useRef<Record<string, Page>>({}), saved = useRef<Record<string, string>>({});
  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => {
      if (Object.entries(working.current).some(([key, page]) => JSON.stringify(page) !== (saved.current[key] || JSON.stringify(project.defaults(key))))) {
        event.preventDefault(); event.returnValue = '';
      }
    };
    window.addEventListener('beforeunload', warn);
    return () => window.removeEventListener('beforeunload', warn);
  }, [project]);
  const defaults = useMemo(() => project.defaults(pageType), [project, pageType]);
  const initial = structuredClone(working.current[pageType] || defaults);
  const registry = useMemo(() => project.runtime(pageType), [project, pageType]);
  const remember = useCallback((page: Page) => { working.current[pageType] = page; }, [pageType]);
  const Canvas = project.Canvas;
  function reset() {
    const current = working.current[pageType];
    if (current && JSON.stringify(current) !== (saved.current[pageType] || JSON.stringify(defaults)) && !window.confirm('Discard unsaved changes on this page and load the project default?')) return;
    working.current[pageType] = project.defaults(pageType);
    setGeneration(value => value + 1);
  }
  return <div className="vv-editor-shell standalone-builder"><h1 className="sr-only">6DS Web Builder design workspace</h1><PageEditor key={`${project.id}:${pageType}:${generation}`} initial={initial} defaults={defaults} registry={registry} context={project.context} surfaceLabels={project.surfaceLabels} exit={() => {}} standalone={{
    toolbar: <div className="builder-project-bar"><label>Project<select aria-label="Project" value={project.id} disabled><option value={project.id}>{project.name}</option></select></label><label>Page<select aria-label="Page" value={pageType} onChange={e => setPageType(e.target.value)}>{project.pages.map(page => <option key={page.id} value={page.id}>{page.label}</option>)}</select></label><button type="button" onClick={reset}>{project.defaultLabel}</button><span className="builder-work-note">Working pages stay open in this tab. Export JSON to keep them.</span></div>,
    onChange: remember,
    onExport: page => { saved.current[pageType] = JSON.stringify(page); },
    filename: project.pages.find(page => page.id === pageType)!.filename,
    serialize: page => serializeLayout(page, project, pageType),
    parse: raw => parseLayout(raw, project, pageType),
  }} renderCanvas={(node, device, page, preview) => <Canvas device={device} page={page} preview={preview}>{node}</Canvas>}/></div>;
}
