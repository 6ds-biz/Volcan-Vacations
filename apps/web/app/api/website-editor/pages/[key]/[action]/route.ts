import {NextRequest} from 'next/server';
import {editorProxy} from '../../../../../../lib/website/editor-proxy';
type Params={params:Promise<{key:string;action:string}>};
export async function POST(request:NextRequest,{params}:Params){const {key,action}=await params;return editorProxy(request,key,action);}
export async function GET(request:NextRequest,{params}:Params){const {key,action}=await params;return editorProxy(request,key,action);}
