'use client';
import {useEffect,useState,type ReactNode} from 'react';
import {WebsiteHandoff} from '../handoff';
/** Finish a new handoff before mounting editable state, even if an older cookie is valid. */
export function EditorEntry({children}:{children:ReactNode}){const [handoff,setHandoff]=useState<boolean|null>(null);useEffect(()=>setHandoff(new URLSearchParams(location.hash.slice(1)).has('ticket')),[]);if(handoff===null)return <p role="status">Opening your website editor…</p>;return handoff?<WebsiteHandoff/>:<>{children}</>;}
