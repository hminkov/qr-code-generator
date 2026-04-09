const BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

export type PaymentStatus = "pending" | "verified" | "failed";

declare global {
  interface Window {
    createLemonSqueezy?: () => void;
    LemonSqueezy?: {
      Setup: (opts: { eventHandler: (e: { event: string }) => void }) => void;
      Url: { Open: (url: string) => void };
    };
  }
}

export async function initCheckout(checkoutUrl: string): Promise<void> {
  if (!window.LemonSqueezy) {
    await new Promise<void>((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "https://app.lemonsqueezy.com/js/lemon.js";
      script.defer = true;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error("Failed to load Lemon Squeezy SDK"));
      document.head.appendChild(script);
    });
  }
  window.createLemonSqueezy?.();
  window.LemonSqueezy?.Url.Open(checkoutUrl);
}

export async function verifyPayment(orderId: string): Promise<PaymentStatus> {
  const maxAttempts = 10;
  let delay = 1000;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    await new Promise((r) => setTimeout(r, delay));
    delay = Math.min(delay * 1.5, 8000);

    try {
      const resp = await fetch(`${BASE}/api/verify/${orderId}`);
      if (resp.ok) {
        const data = await resp.json();
        if (data.paid) return "verified";
      }
    } catch {
      // network error - retry
    }
  }

  return "failed";
}
