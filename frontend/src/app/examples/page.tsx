import Link from "next/link";

const EXAMPLES = [
  { name: "Navy circles", desc: "Classic navy blue with circular dots. The most popular choice for formal invitations.", color: "#445E7C", style: "circles" },
  { name: "Gold rounded", desc: "Warm gold with rounded squares. Pairs well with foil-stamped stationery.", color: "#D4AF37", style: "rounded" },
  { name: "Rose gold circles", desc: "Soft rose gold circles. A modern romantic option for spring and summer weddings.", color: "#B76E79", style: "circles" },
  { name: "Dusty blue circles", desc: "Muted blue with circles. Complements dusty blue and slate color palettes.", color: "#8BA9C2", style: "circles" },
  { name: "Sage rounded", desc: "Earthy sage green with rounded dots. Natural and understated for garden weddings.", color: "#9CAF88", style: "rounded" },
  { name: "Burgundy rounded", desc: "Deep burgundy with rounded squares. Bold and elegant for autumn and winter events.", color: "#800020", style: "rounded" },
  { name: "Charcoal circles", desc: "Neutral charcoal with circles. Works with any color palette without competing.", color: "#36454F", style: "circles" },
  { name: "Black rounded", desc: "Classic black with rounded squares. Maximum contrast for easy scanning.", color: "#000000", style: "rounded" },
];

function MiniQR({ color, style }: { color: string; style: string }) {
  const dots = [
    1,1,1,0,1,0,1,1,1,
    1,0,1,1,0,1,1,0,1,
    1,1,1,0,1,0,1,1,1,
    0,1,0,1,0,1,0,1,0,
    1,0,1,0,0,0,1,0,1,
    0,1,0,1,0,1,0,1,0,
    1,1,1,0,1,0,1,1,1,
    1,0,1,1,0,1,1,0,1,
    1,1,1,0,1,0,1,1,1,
  ];
  return (
    <div className="w-full aspect-square bg-white rounded-lg p-4">
      <div className="w-full h-full grid grid-cols-9 grid-rows-9 gap-[2px]">
        {dots.map((on, i) => (
          <div
            key={i}
            className={style === "circles" ? "rounded-full" : "rounded-[2px]"}
            style={{ backgroundColor: on ? color : "transparent" }}
          />
        ))}
      </div>
    </div>
  );
}

export default function ExamplesPage() {
  return (
    <main className="min-h-screen">
      <section className="border-b border-gray-100 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-20 text-center">
          <h1 className="text-4xl font-semibold tracking-tight text-gray-900 mb-4">Examples</h1>
          <p className="text-lg text-gray-500 max-w-md mx-auto">
            Eight color presets designed for wedding invitations and event stationery.
          </p>
        </div>
      </section>

      <section className="max-w-5xl mx-auto px-4 py-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {EXAMPLES.map((ex) => (
            <div key={ex.name} className="group">
              <div className="border border-gray-200 rounded-xl overflow-hidden bg-gray-50 mb-3">
                <MiniQR color={ex.color} style={ex.style} />
              </div>
              <h3 className="text-sm font-medium text-gray-900">{ex.name}</h3>
              <p className="text-xs text-gray-500 mt-1 leading-relaxed">{ex.desc}</p>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <p className="text-sm text-gray-500 mb-4">Ready to create your own?</p>
          <Link
            href="/"
            className="inline-flex px-5 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors"
          >
            Open Designer
          </Link>
        </div>
      </section>
    </main>
  );
}
