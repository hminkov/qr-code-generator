"use client";

import { useEffect, useRef } from "react";
import QRCode from "qrcode";

const COLOR_MAP: Record<string, string> = {
  navy: "#445E7C",
  gold: "#D4AF37",
  rose_gold: "#B76E79",
  burgundy: "#800020",
  sage: "#9CAF88",
  dusty_blue: "#8BA9C2",
  black: "#000000",
  charcoal: "#36454F",
};

const COLOR_LABEL: Record<string, string> = {
  navy: "Navy",
  gold: "Gold",
  rose_gold: "Rose Gold",
  burgundy: "Burgundy",
  sage: "Sage",
  dusty_blue: "Dusty Blue",
  black: "Black",
  charcoal: "Charcoal",
};

interface Props {
  data: string;
  color: string;
  style: "circles" | "rounded" | "diamond" | "square";
  size: number;
  loading: boolean;
  serverUrl: string | null;
}

export default function QRPreview({ data, color, style, size, loading, serverUrl }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!data || !canvasRef.current) return;
    const canvas = canvasRef.current;
    canvas.width = 400;
    canvas.height = 400;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    QRCode.toCanvas(canvas, data, {
      width: 400,
      margin: 2,
      color: { dark: COLOR_MAP[color] ?? color, light: "#FFFFFF" },
    }).catch(() => ctx.clearRect(0, 0, 400, 400));
  }, [data, color, style]);

  const colorName = COLOR_LABEL[color] ?? color;
  const styleName = style === "circles" ? "Circle dots" : "Rounded dots";

  return (
    <div className="flex flex-col">
      {/* Preview card */}
      <div className="relative w-full max-w-md aspect-square bg-white rounded-xl border border-gray-200 flex items-center justify-center overflow-hidden">
        {serverUrl ? (
          <img src={serverUrl} alt="QR code" className="w-full h-full object-contain p-6" />
        ) : data ? (
          <canvas ref={canvasRef} className="w-full h-full p-6" />
        ) : (
          <div className="text-center px-10">
            <div className="w-16 h-16 mx-auto mb-4 rounded-lg bg-gray-50 flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={1}>
                <path d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
              </svg>
            </div>
            <p className="text-sm text-gray-400 mb-1">Your QR code will appear here</p>
            <p className="text-xs text-gray-300">Type a URL above to get started</p>
          </div>
        )}
        {loading && (
          <div className="absolute inset-0 bg-white/80 flex items-center justify-center">
            <div className="w-5 h-5 border-2 border-gray-200 border-t-gray-600 rounded-full animate-spin" />
          </div>
        )}
      </div>

      {/* Info bar below preview */}
      <div className="mt-4 space-y-2">
        {serverUrl ? (
          <>
            <div className="flex items-center gap-1.5 text-xs text-emerald-600">
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Scannable &middot; Error correction H (30% recovery)
            </div>
            <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-400">
              <span>{colorName}</span>
              <span>{styleName}</span>
              <span>{size}px</span>
              <span>PNG</span>
            </div>
          </>
        ) : data && !loading ? (
          <p className="text-xs text-gray-300">
            Live preview &middot; Click <span className="text-gray-500">Create QR Code</span> for the full render with logo and styled dots
          </p>
        ) : null}
      </div>
    </div>
  );
}
