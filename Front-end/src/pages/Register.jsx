import { Link, useNavigate } from 'react-router-dom'

function RegisterPage() {
  const navigate = useNavigate()

  return (
    <main className="flex min-h-screen w-full flex-col bg-surface font-body-md text-on-surface md:flex-row">
      <section className="relative hidden items-center justify-center overflow-hidden p-2xl md:flex md:w-1/2" style={{ background: 'linear-gradient(135deg, #0F172A 0%, #4F46E5 100%)' }}>
        <div className="absolute top-0 right-0 h-96 w-96 translate-x-1/2 -translate-y-1/2 rounded-full bg-primary opacity-20 blur-[120px]"></div>
        <div className="absolute bottom-0 left-0 h-64 w-64 -translate-x-1/2 translate-y-1/2 rounded-full bg-secondary opacity-10 blur-[80px]"></div>
        <div className="relative z-10 max-w-lg text-center md:text-left">
          <div className="mb-lg inline-flex items-center space-x-2 rounded-full border border-primary/30 bg-primary/20 px-md py-xs">
            <span className="h-2 w-2 rounded-full bg-secondary-fixed animate-pulse"></span>
            <span className="text-label-sm font-label-sm text-on-primary-container">Enterprise Ready</span>
          </div>
          <h1 className="mb-md font-headline-lg text-headline-lg leading-tight text-white">
            No-code integration.<br />Set up in 3 minutes.
          </h1>
          <p className="mb-3xl font-body-lg text-body-lg text-primary-fixed-dim/80">
            Connect your existing commerce ecosystem directly to our AI brain without a single line of code.
          </p>
          <div className="grid grid-cols-3 gap-lg rounded-xl border border-white/10 bg-white/5 p-lg backdrop-blur-sm">
            <div className="flex flex-col items-center justify-center space-y-sm">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-white/20 bg-white/10">
                <span className="material-symbols-outlined text-3xl text-white">chat</span>
              </div>
              <span className="text-label-sm font-label-sm text-white/60">WhatsApp</span>
            </div>
            <div className="flex items-center justify-center">
              <span className="material-symbols-outlined text-4xl text-secondary-fixed animate-bounce">arrow_forward</span>
            </div>
            <div className="flex flex-col items-center justify-center space-y-sm">
              <div className="flex h-20 w-20 items-center justify-center rounded-full border-2 border-primary-fixed-dim/30 bg-primary shadow-xl shadow-primary/40">
                <span className="material-symbols-outlined text-4xl text-white" style={{ fontVariationSettings: 'FILL 1' }}>psychology</span>
              </div>
              <span className="text-label-sm font-label-sm text-white">AI Core</span>
            </div>
            <div className="flex flex-col items-center justify-center space-y-sm">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-white/20 bg-white/10">
                <span className="material-symbols-outlined text-3xl text-white">photo_camera</span>
              </div>
              <span className="text-label-sm font-label-sm text-white/60">Instagram</span>
            </div>
            <div className="flex items-center justify-center">
              <span className="material-symbols-outlined text-4xl text-secondary-fixed animate-pulse">sync</span>
            </div>
            <div className="flex flex-col items-center justify-center space-y-sm">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-white/20 bg-white/10">
                <span className="material-symbols-outlined text-3xl text-white">shopping_cart</span>
              </div>
              <span className="text-label-sm font-label-sm text-white/60">Web Store</span>
            </div>
          </div>
        </div>
      </section>

      <section className="flex w-full items-center justify-center bg-surface p-lg md:w-1/2 md:p-2xl">
        <div className="w-full max-w-xl">
          <div className="mb-xl flex items-center space-x-2 md:hidden">
            <span className="material-symbols-outlined text-3xl text-primary">hub</span>
            <span className="text-headline-md font-headline-md text-primary">CommerceMind AI</span>
          </div>

          <div className="mb-2xl flex items-center space-x-sm">
            <div className="h-1.5 flex-1 rounded-full bg-primary"></div>
            <div className="h-1.5 flex-1 rounded-full bg-surface-container-high"></div>
            <div className="h-1.5 flex-1 rounded-full bg-surface-container-high"></div>
          </div>

          <form className="space-y-xl">
            <div>
              <header className="mb-lg">
                <h2 className="mb-xs text-headline-lg-mobile font-headline-lg-mobile text-on-surface md:text-headline-lg md:font-headline-lg">Create your account</h2>
                <p className="text-body-md font-body-md text-on-surface-variant">Start your 14-day free trial. No credit card required.</p>
              </header>
              <div className="space-y-md">
                <div className="space-y-xs">
                  <label className="text-label-sm font-label-sm text-on-surface-variant" htmlFor="full_name">Full Name</label>
                  <input className="w-full rounded-lg border border-outline-variant bg-white px-md py-sm outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/20" id="full_name" placeholder="John Doe" type="text" />
                </div>
                <div className="space-y-xs">
                  <label className="text-label-sm font-label-sm text-on-surface-variant" htmlFor="email">Business Email</label>
                  <input className="w-full rounded-lg border border-outline-variant bg-white px-md py-sm outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/20" id="email" placeholder="john@company.com" type="email" />
                </div>
                <div className="space-y-xs">
                  <label className="text-label-sm font-label-sm text-on-surface-variant" htmlFor="password">Password</label>
                  <input className="w-full rounded-lg border border-outline-variant bg-white px-md py-sm outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/20" id="password" placeholder="••••••••" type="password" />
                </div>
              </div>
              <button className="mt-xl w-full rounded-lg bg-primary py-md text-headline-md font-headline-md text-white shadow-lg shadow-primary/20 transition-all hover:bg-primary/90 active:scale-95" type="button" onClick={() => navigate('/register/step-2')}>
                Continue to Store Details
              </button>
            </div>
          </form>

          <div className="mt-lg text-center">
            <p className="text-body-md font-body-md text-on-surface-variant">
              Already have an account?
              <Link className="ml-xs font-bold text-primary transition-all hover:underline" to="/signin">Sign In</Link>
            </p>
          </div>

          <div className="mt-2xl flex items-center justify-between border-t border-outline-variant pt-xl text-on-surface-variant">
            <div className="flex items-center space-x-2">
              <span className="material-symbols-outlined text-sm">lock</span>
              <span className="text-label-sm font-label-sm">256-bit encryption</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="material-symbols-outlined text-sm">verified_user</span>
              <span className="text-label-sm font-label-sm">GDPR Compliant</span>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}

export default RegisterPage
