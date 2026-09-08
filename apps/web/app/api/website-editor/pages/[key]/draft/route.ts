import {NextRequest} from 'next/server';
import {editorProxy} from '../../../../../../lib/website/editor-proxy';
export async function PUT(request:NextRequest,{params}:{params:Promise<{key:string}>}){return editorProxy(request,(await params).key,'draft');}
