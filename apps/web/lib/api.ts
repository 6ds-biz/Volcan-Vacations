const configuredApiUrl = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '');

export const apiUrl =
  configuredApiUrl || (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : '');

// Preserve GitHub's private-port session in Codespaces; not application auth.
export const apiCredentials: RequestCredentials = /^https:\/\/[^/:]+\.app\.github\.dev(?::443)?(?:\/|$)/.test(apiUrl) ? 'include' : 'omit';

export function requireApiUrl(): string {
  if (!apiUrl) {
    throw new Error('NEXT_PUBLIC_API_URL must be configured for this deployment.');
  }

  return apiUrl;
}
