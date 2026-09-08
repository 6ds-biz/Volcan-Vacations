const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@6ds/page-builder'],
  async headers() { return [{source:'/:path*',headers:[{key:'X-Frame-Options',value:'DENY'},{key:'Content-Security-Policy',value:"frame-ancestors 'none'"},{key:'Referrer-Policy',value:'same-origin'},{key:'X-Content-Type-Options',value:'nosniff'}]}]; },
};

export default nextConfig;
