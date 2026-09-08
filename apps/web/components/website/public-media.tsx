'use client';
import {createContext,useContext} from 'react';
import {MediaView,type RenderContext} from '@6ds/page-builder/runtime';
import type {MediaConfig} from '@6ds/page-builder/core';
export const WebsiteContext=createContext<RenderContext|null>(null);
export function ConfiguredMedia({config,scenic=false}:{config:MediaConfig;scenic?:boolean}){const context=useContext(WebsiteContext);return context?<div className={scenic?'website-scenic-media':undefined}><MediaView config={config} context={context}/></div>:null;}
