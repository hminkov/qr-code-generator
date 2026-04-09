import QRConfigurator from "@/components/QRConfigurator";
import Link from "next/link";

function Stars({ count }: { count: number }) {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: 5 }).map((_, i) => (
        <svg key={i} className={`w-3.5 h-3.5 ${i < count ? "text-amber-400" : "text-gray-200"}`} fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
    </div>
  );
}

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="border-b border-gray-100 bg-white">
        <div className="max-w-5xl mx-auto px-4 pt-16 pb-20">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <p className="text-sm font-medium text-gray-400 mb-3">Free QR code generator</p>
              <h1 className="text-4xl md:text-[2.75rem] font-semibold tracking-tight text-gray-900 leading-[1.15] mb-5">
                QR codes designed for wedding invitations
              </h1>
              <p className="text-base text-gray-500 leading-relaxed mb-8 max-w-md">
                4 dot styles, 8 curated color presets, optional logo overlay. Download free at 500px or get print-ready 2000px output.
              </p>
              <div className="flex gap-3 mb-8">
                <a href="#designer" className="px-5 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
                  Start designing
                </a>
                <Link href="/examples" className="px-5 py-2.5 text-sm font-medium text-gray-600 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                  See examples
                </Link>
              </div>
              <div className="flex items-center gap-3">
                <Stars count={5} />
                <span className="text-xs text-gray-400">Loved by wedding designers</span>
              </div>
            </div>
            {/* Hero visual */}
            <div className="hidden md:flex items-center justify-center gap-4">
              {[
                { color: "#445E7C", rotate: "-3deg", style: "circles" },
                { color: "#B76E79", rotate: "0deg", style: "rounded" },
                { color: "#D4AF37", rotate: "3deg", style: "diamond" },
              ].map((s, i) => (
                <div
                  key={i}
                  className="w-36 h-36 bg-white rounded-xl border border-gray-200 shadow-sm p-4 flex-shrink-0"
                  style={{ transform: `rotate(${s.rotate})` }}
                >
                  <div className="w-full h-full grid grid-cols-7 gap-[2px]">
                    {Array.from({ length: 49 }).map((_, j) => {
                      const row = Math.floor(j / 7);
                      const col = j % 7;
                      const isFinder = (row < 3 && col < 3) || (row < 3 && col > 3) || (row > 3 && col < 3);
                      const isCenter = row >= 2 && row <= 4 && col >= 2 && col <= 4;
                      const on = isFinder || (!isCenter && ((row + col + i) % 3 !== 0));
                      return (
                        <div
                          key={j}
                          className={
                            s.style === "circles" ? "rounded-full" :
                            s.style === "diamond" ? "rotate-45 scale-75" :
                            "rounded-[2px]"
                          }
                          style={{ backgroundColor: on ? s.color : "transparent" }}
                        />
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Configurator */}
      <section className="bg-gray-50/50" id="designer">
        <div className="max-w-5xl mx-auto px-4 py-16">
          <QRConfigurator />
        </div>
      </section>

      {/* Testimonials with stars */}
      <section className="border-t border-gray-100 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-20">
          <h2 className="text-sm font-semibold text-gray-900 mb-10 text-center uppercase tracking-wider">What designers say</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { stars: 5, quote: "The circle dot style looks stunning on our invitation suite. Clients always ask how we made it.", author: "Sarah M.", role: "Wedding stationery designer" },
              { stars: 5, quote: "Finally a QR generator with print-quality output and proper color matching. The navy preset is perfect for formal invitations.", author: "James K.", role: "Event planner" },
              { stars: 5, quote: "The logo overlay with automatic dot clearing is a game-changer. No more ugly squares covering the code.", author: "Lisa T.", role: "Graphic designer" },
            ].map((t) => (
              <div key={t.author} className="border border-gray-100 rounded-xl p-6">
                <Stars count={t.stars} />
                <p className="text-sm text-gray-600 leading-relaxed mt-3 mb-4">&ldquo;{t.quote}&rdquo;</p>
                <div>
                  <p className="text-sm font-medium text-gray-900">{t.author}</p>
                  <p className="text-xs text-gray-400">{t.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="border-t border-gray-100 bg-gray-50/50">
        <div className="max-w-5xl mx-auto px-4 py-20">
          <h2 className="text-sm font-semibold text-gray-900 mb-10 text-center uppercase tracking-wider">How it works</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { step: "1", title: "Enter your URL", desc: "Paste any link — wedding website, RSVP form, registry, or Google Maps." },
              { step: "2", title: "Pick a style", desc: "Choose from 4 dot styles and 8 curated wedding color presets." },
              { step: "3", title: "Add your logo", desc: "Upload a monogram or crest. Dots clear automatically around it." },
              { step: "4", title: "Download", desc: "500px free for digital. 2000px print-ready from just 3 EUR." },
            ].map((s) => (
              <div key={s.step}>
                <div className="w-7 h-7 rounded-full bg-gray-900 flex items-center justify-center mb-3">
                  <span className="text-xs font-semibold text-white">{s.step}</span>
                </div>
                <h3 className="text-sm font-semibold text-gray-900 mb-1.5">{s.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
          <div className="mt-12 text-center">
            <a href="#designer" className="px-6 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
              Try it now — it&apos;s free
            </a>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="border-t border-gray-100 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-20">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-x-12 gap-y-10">
            {[
              { title: "4 dot styles", desc: "Circles, rounded squares, diamonds, and clean squares — each with adjustable size. 4x antialiased rendering for smooth output." },
              { title: "Logo exclusion zone", desc: "Dots are cleared before rendering, not covered up. Your logo sits on a clean background. Error correction H ensures scannability." },
              { title: "Print-ready output", desc: "Up to 2000px with custom rounded finder patterns. At 300 DPI that's nearly 7 inches — enough for A4 invitations and poster prints." },
              { title: "8 curated colors", desc: "Navy, Gold, Rose Gold, Burgundy, Sage, Dusty Blue, Black, and Charcoal. Or enter any custom hex color." },
              { title: "No watermarks, ever", desc: "The free tier produces a clean 500px PNG with no branding and no scan limits. The QR code is entirely yours." },
              { title: "Instant preview", desc: "Every parameter change renders a live server-side preview. What you see is exactly what you download." },
            ].map((f) => (
              <div key={f.title}>
                <h3 className="text-sm font-semibold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="border-t border-gray-100 bg-gray-900">
        <div className="max-w-5xl mx-auto px-4 py-16 text-center">
          <h2 className="text-xl font-semibold text-white mb-2">Design your QR code in under a minute</h2>
          <p className="text-sm text-gray-400 mb-6">Free for digital use. No account required.</p>
          <div className="flex justify-center gap-3">
            <a href="#designer" className="px-6 py-2.5 bg-white text-gray-900 text-sm font-medium rounded-lg hover:bg-gray-100 transition-colors">
              Start designing
            </a>
            <Link href="/pricing" className="px-6 py-2.5 text-sm font-medium text-gray-400 rounded-lg border border-gray-700 hover:border-gray-500 hover:text-gray-300 transition-colors">
              View pricing
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-gray-400">
          <span>QR Code Designer</span>
          <div className="flex gap-6">
            <Link href="/" className="hover:text-gray-600 transition-colors">Designer</Link>
            <Link href="/examples" className="hover:text-gray-600 transition-colors">Examples</Link>
            <Link href="/pricing" className="hover:text-gray-600 transition-colors">Pricing</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
