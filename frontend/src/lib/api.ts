const BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

export interface QRParams {
  data: string;
  color?: string;
  background_color?: string;
  size?: number;
  logo_size_ratio?: number;
  logo_padding?: number;
  style?: string;
  error_correction?: string;
  dot_size?: number;
  version?: number | null;
  logo?: File | null;
}

async function _fetchPng(url: string, options?: RequestInit): Promise<string> {
  const resp = await fetch(url, options);
  if (!resp.ok) {
    throw new Error(`API error ${resp.status}: ${await resp.text()}`);
  }
  const blob = await resp.blob();
  return URL.createObjectURL(blob);
}

export async function generateQR(params: QRParams): Promise<string> {
  const form = new FormData();
  form.append("data", params.data);
  if (params.color) form.append("color", params.color);
  if (params.background_color) form.append("background_color", params.background_color);
  if (params.size !== undefined) form.append("size", String(params.size));
  if (params.style) form.append("style", params.style);
  if (params.error_correction) form.append("error_correction", params.error_correction);
  if (params.dot_size !== undefined) form.append("dot_size", String(params.dot_size));
  if (params.logo_size_ratio !== undefined) form.append("logo_size_ratio", String(params.logo_size_ratio));
  if (params.logo_padding !== undefined) form.append("logo_padding", String(params.logo_padding));
  if (params.version !== undefined && params.version !== null) form.append("version", String(params.version));
  if (params.logo) form.append("logo", params.logo);

  return _fetchPng(`${BASE}/api/generate`, {
    method: "POST",
    body: form,
  });
}

export async function fetchPreview(params: QRParams): Promise<string> {
  const query = new URLSearchParams();
  query.set("data", params.data);
  if (params.color) query.set("color", params.color);
  if (params.background_color) query.set("background_color", params.background_color);
  if (params.style) query.set("style", params.style);
  if (params.dot_size !== undefined) query.set("dot_size", String(params.dot_size));
  if (params.error_correction) query.set("error_correction", params.error_correction);
  if (params.logo_size_ratio !== undefined) query.set("logo_size_ratio", String(params.logo_size_ratio));
  if (params.logo_padding !== undefined) query.set("logo_padding", String(params.logo_padding));
  if (params.version !== undefined && params.version !== null) query.set("version", String(params.version));
  return _fetchPng(`${BASE}/api/generate/preview?${query}`);
}

export async function fetchPresets(): Promise<Record<string, string>> {
  const resp = await fetch(`${BASE}/api/presets`);
  if (!resp.ok) throw new Error(`API error ${resp.status}`);
  return resp.json();
}
