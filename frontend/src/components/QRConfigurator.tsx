"use client";

import { useState, useCallback, useRef } from "react";
import QRPreview from "./QRPreview";
import ColorPicker from "./ColorPicker";
import { generateQR } from "@/lib/api";

interface Config {
  data: string;
  color: string;
  background_color: string;
  style: "circles" | "rounded" | "diamond" | "square";
  dot_size: number;
  size: number;
  error_correction: "L" | "M" | "Q" | "H";
}

const DEFAULT: Config = {
  data: "",
  color: "navy",
  background_color: "#FFFFFF",
  style: "circles",
  dot_size: 0.9,
  size: 1000,
  error_correction: "H",
};

export default function QRConfigurator() {
  const [config, setConfig] = useState<Config>(DEFAULT);
  const [logoFile, setLogoFile] = useState<File | null>(null);
  const [logoPreviewUrl, setLogoPreviewUrl] = useState<string | null>(null);
  const [serverUrl, setServerUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const logoRef = useRef<File | null>(null);

  const schedulePreview = useCallback((cfg: Config) => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (!cfg.data) return;
    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const url = await generateQR({
          data: cfg.data,
          color: cfg.color,
          background_color: cfg.background_color,
          style: cfg.style,
          dot_size: cfg.dot_size,
          size: 500,
          error_correction: cfg.error_correction,
          logo: logoRef.current,
        });
        setServerUrl(url);
      } catch { /* keep showing canvas */ }
      finally { setLoading(false); }
    }, 500);
  }, []);

  const update = (patch: Partial<Config>) => {
    const next = { ...config, ...patch };
    setConfig(next);
    schedulePreview(next);
  };

  const handleLogoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] ?? null;
    setLogoFile(file);
    logoRef.current = file;
    if (logoPreviewUrl) URL.revokeObjectURL(logoPreviewUrl);
    setLogoPreviewUrl(file ? URL.createObjectURL(file) : null);
    schedulePreview(config);
  };

  const removeLogo = () => {
    setLogoFile(null);
    logoRef.current = null;
    if (logoPreviewUrl) URL.revokeObjectURL(logoPreviewUrl);
    setLogoPreviewUrl(null);
    schedulePreview(config);
  };

  const handleGenerate = async () => {
    if (!config.data) return;
    setGenerating(true);
    try {
      const url = await generateQR({
        data: config.data,
        color: config.color,
        background_color: config.background_color,
        style: config.style,
        dot_size: config.dot_size,
        size: config.size,
        error_correction: config.error_correction,
        logo: logoFile,
      });
      setServerUrl(url);
    } finally { setGenerating(false); }
  };

  return (
    <div className="flex flex-col-reverse md:grid md:grid-cols-2 gap-12">
      {/* Controls */}
      <div className="space-y-6">
        {/* URL */}
        <div>
          <label className="block text-sm font-medium text-gray-900 mb-1.5">URL or text</label>
          <input
            type="text"
            className="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
            placeholder="https://yourwedding.com/rsvp"
            value={config.data}
            onChange={e => update({ data: e.target.value })}
          />
        </div>

        {/* Color */}
        <div>
          <label className="block text-sm font-medium text-gray-900 mb-1.5">Color</label>
          <ColorPicker value={config.color} onChange={color => update({ color })} />
        </div>

        {/* Style */}
        <div>
          <label className="block text-sm font-medium text-gray-900 mb-1.5">Dot style</label>
          <div className="grid grid-cols-4 gap-2">
            {([
              { value: "circles", label: "Circles" },
              { value: "rounded", label: "Rounded" },
              { value: "diamond", label: "Diamond" },
              { value: "square", label: "Square" },
            ] as const).map(s => (
              <button
                key={s.value}
                onClick={() => update({ style: s.value })}
                className={`py-2 rounded-lg text-xs font-medium border transition-colors ${
                  config.style === s.value
                    ? "bg-gray-900 text-white border-gray-900"
                    : "bg-white text-gray-600 border-gray-200 hover:border-gray-300"
                }`}
              >
                {s.label}
              </button>
            ))}
          </div>
        </div>

        {/* Logo */}
        <div>
          <div className="flex items-baseline justify-between mb-1.5">
            <label className="text-sm font-medium text-gray-900">Logo</label>
            <span className="text-xs text-gray-400">optional</span>
          </div>
          {logoPreviewUrl ? (
            <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-100">
              <img src={logoPreviewUrl} alt="Logo" className="w-10 h-10 object-contain rounded bg-white p-0.5" />
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-700 truncate">{logoFile?.name}</p>
                <p className="text-xs text-gray-400">Dots will clear around the logo automatically</p>
              </div>
              <button onClick={removeLogo} className="text-xs text-gray-400 hover:text-red-500 flex-shrink-0 transition-colors">
                Remove
              </button>
            </div>
          ) : (
            <label className="flex items-center justify-center gap-2 w-full py-4 border border-dashed border-gray-300 rounded-lg text-sm text-gray-400 cursor-pointer hover:border-gray-400 hover:text-gray-500 transition-colors">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Upload monogram, crest, or icon
              <input type="file" accept="image/png,image/jpeg,image/svg+xml,image/webp" onChange={handleLogoChange} className="hidden" />
            </label>
          )}
        </div>

        {/* Advanced */}
        <div>
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-sm text-gray-400 hover:text-gray-600 transition-colors"
          >
            {showAdvanced ? "Hide" : "Show"} advanced options
          </button>

          {showAdvanced && (
            <div className="mt-4 space-y-5 pt-4 border-t border-gray-100">
              <div>
                <div className="flex justify-between mb-1.5">
                  <label className="text-sm font-medium text-gray-900">Dot size</label>
                  <span className="text-xs text-gray-400 tabular-nums">{config.dot_size.toFixed(1)}</span>
                </div>
                <input
                  type="range" min="0.5" max="1.2" step="0.05"
                  value={config.dot_size}
                  onChange={e => update({ dot_size: parseFloat(e.target.value) })}
                  className="w-full"
                />
                <div className="flex justify-between text-[10px] text-gray-300 mt-0.5">
                  <span>Small with gaps</span>
                  <span>Overlapping</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-900 mb-1.5">Output size</label>
                <div className="flex gap-2">
                  {[
                    { v: 500, label: "500px", note: "Free" },
                    { v: 1000, label: "1000px", note: null },
                    { v: 2000, label: "2000px", note: "Print" },
                  ].map(s => (
                    <button
                      key={s.v}
                      onClick={() => update({ size: s.v })}
                      className={`flex-1 py-2 rounded-lg text-sm border transition-colors ${
                        config.size === s.v
                          ? "bg-gray-900 text-white border-gray-900"
                          : "bg-white text-gray-600 border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      {s.label}
                      {s.note && (
                        <span className={`block text-[10px] mt-0.5 ${config.size === s.v ? "text-gray-400" : "text-gray-300"}`}>
                          {s.note}
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-900 mb-1.5">Error correction</label>
                <select
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
                  value={config.error_correction}
                  onChange={e => update({ error_correction: e.target.value as Config["error_correction"] })}
                >
                  <option value="L">Low — 7% recovery</option>
                  <option value="M">Medium — 15% recovery</option>
                  <option value="Q">Quartile — 25% recovery</option>
                  <option value="H">High — 30% recovery (recommended with logo)</option>
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="space-y-3 pt-2">
          <button
            onClick={handleGenerate}
            disabled={!config.data || generating}
            className="w-full bg-gray-900 text-white py-3 rounded-lg text-sm font-medium disabled:opacity-30 hover:bg-gray-800 transition-colors"
          >
            {generating ? "Creating..." : "Create QR Code"}
          </button>

          {serverUrl && (
            <a
              href={serverUrl}
              download={`qr-code-${config.size}px.png`}
              className="flex items-center justify-center gap-2 w-full py-3 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Download PNG &middot; {config.size}px
            </a>
          )}
        </div>
      </div>

      {/* Preview */}
      <div className="md:sticky md:top-20 md:self-start">
        <QRPreview
          data={config.data}
          color={config.color}
          style={config.style}
          size={config.size}
          loading={loading}
          serverUrl={serverUrl}
        />
      </div>
    </div>
  );
}
