// Vercel inlines this public setting at build time. Fail before deploying a
// disconnected preview; local/Docker builds retain their existing workflow.
if (process.env.VERCEL === '1') {
  const value = process.env.NEXT_PUBLIC_API_URL;
  let url;
  try { url = new URL(value); } catch { /* Report configuration without its value. */ }
  if (!url || url.protocol !== 'https:' || url.username || url.password || url.search || url.hash
      || url.pathname !== '/' || ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)
      || url.hostname.endsWith('.app.github.dev')) {
    throw new Error('Set NEXT_PUBLIC_API_URL to the permanent HTTPS API origin before building on Vercel.');
  }
}

const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@6ds/page-builder'],
};

export default nextConfig;
