/** Plain public links only; no protocol-relative URLs, control characters or credentials. */
export function safePublicLink(value:unknown):value is string{
 if(typeof value!=='string'||value.length>2000||/[\s<>\\\u0000-\u001f\u007f]/.test(value)||/%(?:0[0-9a-f]|1[0-9a-f]|7f)/i.test(value))return false;
 if(/^\/(?!\/)/.test(value)||/^#[a-zA-Z0-9_-]+$/.test(value))return true;
 if(/^mailto:[^@?]+@[^@?]+(?:\?[^#]*)?$/.test(value)||/^tel:\+?[0-9().-]+$/.test(value))return true;
 try{const url=new URL(value);return url.protocol==='https:'&&!!url.hostname&&!url.username&&!url.password;}catch{return false;}
}
