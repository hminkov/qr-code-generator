"use client";

import { useState } from "react";

const PRESETS = [
  { name: "navy", hex: "#445E7C", label: "Navy" },
  { name: "gold", hex: "#D4AF37", label: "Gold" },
  { name: "rose_gold", hex: "#B76E79", label: "Rose Gold" },
  { name: "burgundy", hex: "#800020", label: "Burgundy" },
  { name: "sage", hex: "#9CAF88", label: "Sage" },
  { name: "dusty_blue", hex: "#8BA9C2", label: "Dusty Blue" },
  { name: "black", hex: "#000000", label: "Black" },
  { name: "charcoal", hex: "#36454F", label: "Charcoal" },
];

interface Props {
  value: string;
  onChange: (color: string) => void;
}

export default function ColorPicker({ value, onChange }: Props) {
  const [custom, setCustom] = useState("");

  return (
    <div className="space-y-2.5">
      <div className="grid grid-cols-4 gap-1.5">
        {PRESETS.map((p) => (
          <button
            key={p.name}
            onClick={() => { setCustom(""); onChange(p.name); }}
            className={`flex flex-col items-center gap-1 py-1.5 rounded-lg transition-colors ${
              value === p.name
                ? "bg-gray-100"
                : "hover:bg-gray-50"
            }`}
          >
            <span
              className={`w-7 h-7 rounded-full border-2 transition-all ${
                value === p.name ? "border-gray-900 scale-110" : "border-transparent"
              }`}
              style={{ backgroundColor: p.hex }}
            />
            <span className={`text-[10px] ${value === p.name ? "text-gray-900 font-medium" : "text-gray-400"}`}>
              {p.label}
            </span>
          </button>
        ))}
      </div>
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 rounded-full border border-gray-200" style={{
          backgroundColor: custom || PRESETS.find(p => p.name === value)?.hex || value
        }} />
        <input
          type="text"
          placeholder="#hex"
          value={custom}
          onChange={(e) => {
            setCustom(e.target.value);
            if (/^#[0-9A-Fa-f]{6}$/.test(e.target.value)) onChange(e.target.value);
          }}
          className="border border-gray-200 rounded-lg px-2.5 py-1.5 text-sm w-24 focus:outline-none focus:ring-2 focus:ring-gray-900"
        />
      </div>
    </div>
  );
}
