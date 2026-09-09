import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
export default {
  reactStrictMode: true,
  devIndicators: false,
  transpilePackages: ['@6ds/page-builder'],
  images: {unoptimized: true},
  experimental: {cpus: 2},
  // Reuse VV presentation source, replacing its two live inventory boundaries.
  // No API/authentication/publishing modules are used by this application.
  webpack(config, {webpack}) {
    // Public presentation imports resolve against this app's dependencies.
    config.resolve.modules = [path.join(root, 'node_modules'), ...config.resolve.modules];
    for (const [name, file] of Object.entries({core: 'core.ts', runtime: 'runtime.tsx', editor: 'editor.tsx', 'styles.css': 'styles.css'})) {
      config.resolve.alias[`@6ds/page-builder/${name}$`] = path.join(root, 'node_modules/@6ds/page-builder/src', file);
    }
    config.plugins.push(new webpack.NormalModuleReplacementPlugin(
      /(^|\/)tour-(inventory|availability)$/,
      path.join(root, 'src/projects/vv/sample-inventory.tsx')
    ));
    return config;
  },
  async headers() {
    return [{source: '/:path*', headers: [
      {key: 'Referrer-Policy', value: 'no-referrer'},
      {key: 'X-Content-Type-Options', value: 'nosniff'}
    ]}];
  }
};
