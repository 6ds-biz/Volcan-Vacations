const configuredApiUrl = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '');

export const apiUrl =
  configuredApiUrl || (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : '');

// GitHub private-port cookies are infrastructure access, not Operations auth.
const apiCredentials: RequestCredentials = /^https:\/\/[^/:]+\.app\.github\.dev(?::443)?(?:\/|$)/.test(apiUrl) ? 'include' : 'omit';

export function requireApiUrl(): string {
  if (!apiUrl) {
    throw new Error('NEXT_PUBLIC_API_URL must be configured for this deployment.');
  }

  return apiUrl;
}

export async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${requireApiUrl()}${path}`, {
    ...options, cache: 'no-store', credentials: apiCredentials, signal: options.signal ?? AbortSignal.timeout(15000),
    headers: {'Content-Type': 'application/json', ...options.headers},
  });
  if (!response.ok) {
    const data = await response.json().catch(() => null);
    const detail = data?.detail;
    const message = typeof detail === 'string' ? detail : Array.isArray(detail)
      ? detail.map((item: {loc: string[]; msg: string}) => `${item.loc.slice(1).join('.')}: ${item.msg}`).join('; ')
      : `Request failed (${response.status}). Please try again.`;
    throw new Error(message);
  }
  return response.status === 204 ? undefined as T : response.json();
}

export function imagePreviewUrl(url: string): string | undefined {
  if (!url.startsWith('/')) return url;
  // Relative /images/ URLs belong to the public site, not Operations.
  if (process.env.NEXT_PUBLIC_WEB_URL) return `${process.env.NEXT_PUBLIC_WEB_URL.replace(/\/$/, '')}${url}`;
  const base = new URL(requireApiUrl());
  if (['localhost', '127.0.0.1'].includes(base.hostname)) { base.port = '3000'; return `${base.origin}${url}`; }
  if (base.hostname.endsWith('.app.github.dev') && base.hostname.includes('-8000.')) return `${base.origin.replace('-8000.', '-3000.')}${url}`;
  return undefined;
}
