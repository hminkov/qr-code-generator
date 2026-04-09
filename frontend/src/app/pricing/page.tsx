import Link from "next/link";

export default function PricingPage() {
  return (
    <main className="min-h-screen">
      <section className="border-b border-gray-100 bg-white">
        <div className="max-w-5xl mx-auto px-4 py-20 text-center">
          <h1 className="text-4xl font-semibold tracking-tight text-gray-900 mb-4">Pricing</h1>
          <p className="text-lg text-gray-500 max-w-md mx-auto">
            Free for digital use. One-time payment for print quality.
          </p>
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Free */}
          <div className="border border-gray-200 rounded-xl p-8">
            <h2 className="text-sm font-medium text-gray-900 mb-1">Free</h2>
            <p className="text-3xl font-semibold text-gray-900 mb-1">&euro;0</p>
            <p className="text-sm text-gray-400 mb-6">No account needed</p>
            <ul className="space-y-3 text-sm text-gray-600 mb-8">
              {[
                "500px PNG output",
                "All 8 color presets",
                "Circle and rounded dot styles",
                "Custom hex colors",
                "Logo overlay",
                "Unlimited generations",
              ].map((f) => (
                <li key={f} className="flex gap-2">
                  <svg className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  {f}
                </li>
              ))}
            </ul>
            <Link
              href="/"
              className="block text-center w-full py-2.5 border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Start designing
            </Link>
          </div>

          {/* Print */}
          <div className="border-2 border-gray-900 rounded-xl p-8 relative">
            <span className="absolute -top-3 left-6 bg-gray-900 text-white text-xs font-medium px-2.5 py-0.5 rounded-full">
              Recommended
            </span>
            <h2 className="text-sm font-medium text-gray-900 mb-1">Print Quality</h2>
            <p className="text-3xl font-semibold text-gray-900 mb-1">&euro;3</p>
            <p className="text-sm text-gray-400 mb-6">One-time payment per QR code</p>
            <ul className="space-y-3 text-sm text-gray-600 mb-8">
              {[
                "Everything in Free",
                "Up to 2000px PNG output",
                "300 DPI print-ready quality",
                "4x antialiased rendering",
                "Ideal for wedding stationery",
                "Commercial use license",
              ].map((f) => (
                <li key={f} className="flex gap-2">
                  <svg className="w-4 h-4 text-gray-900 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  {f}
                </li>
              ))}
            </ul>
            <Link
              href="/"
              className="block text-center w-full py-2.5 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors"
            >
              Start designing
            </Link>
          </div>
        </div>

        {/* FAQ */}
        <div className="mt-20">
          <h2 className="text-lg font-semibold text-gray-900 mb-8 text-center">Questions</h2>
          <div className="space-y-6 max-w-xl mx-auto">
            {[
              {
                q: "Will my QR code work after downloading?",
                a: "Yes. All generated QR codes use error correction level H, which means they remain scannable even with a logo covering up to 30% of the code.",
              },
              {
                q: "What file format do I get?",
                a: "PNG at the resolution you choose. 500px is suitable for screens and social media. 2000px is print-ready at 300 DPI for stationery.",
              },
              {
                q: "Do I need an account?",
                a: "No. The free tier requires no signup. Payment for print quality is a one-time checkout — no subscription.",
              },
              {
                q: "Can I use this for commercial projects?",
                a: "Yes. The free tier is fine for personal and client work at 500px. The paid tier includes a commercial license for the high-resolution output.",
              },
            ].map((item) => (
              <div key={item.q}>
                <h3 className="text-sm font-medium text-gray-900 mb-1">{item.q}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{item.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
