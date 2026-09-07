// Test credentials are supplied in an untracked, mode-0600 file; never logged.
const fs=require('node:fs');
module.exports=async function authenticate(context,api,origin){
 if(!['localhost','127.0.0.1'].includes(new URL(api).hostname)) throw new Error('Credentialed acceptance tests require localhost API transport.');
 const file=process.env.VV_E2E_AUTH_FILE;
 if(!file)throw new Error('Set VV_E2E_AUTH_FILE to a private JSON file with email and password.');
 const {email,password}=JSON.parse(fs.readFileSync(file,'utf8'));
 const response=await context.request.post(api+'/ops/auth/login',{headers:{Origin:origin},data:{email,password}});
 if(!response.ok())throw new Error('Operations test login failed ('+response.status()+')');
 return {Origin:origin,'X-CSRF-Token':(await response.json()).csrf_token};
};
