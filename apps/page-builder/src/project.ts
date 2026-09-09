import type {ComponentType, ReactNode} from 'react';
import type {Device, MediaProvider, Page, Registry} from '@6ds/page-builder/core';
import type {RenderContext, RuntimeRegistry} from '@6ds/page-builder/runtime';

export type ProjectDefinition = {
  id: string;
  name: string;
  defaultLabel: string;
  pages: readonly {id: string; label: string; filename: string}[];
  tokens: Record<string, readonly string[]>;
  surfaceLabels: Record<string, string>;
  media: MediaProvider;
  registry: (pageType: string) => Registry;
  defaults: (pageType: string) => Page;
  publicEmail: string;
};
export type DesignProject = ProjectDefinition & {
  runtime: (pageType: string) => RuntimeRegistry;
  context: RenderContext;
  Canvas: ComponentType<{children: ReactNode; device: Device; page: Page; preview: boolean}>;
};
