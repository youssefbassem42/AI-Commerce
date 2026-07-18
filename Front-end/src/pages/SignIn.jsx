import { Link } from 'react-router-dom'

function SignInPage() {
  return (
    <main className="flex min-h-screen flex-col bg-background text-on-surface antialiased md:flex-row">
      <section className="relative hidden flex-col items-center justify-center overflow-hidden px-2xl md:flex md:w-1/2" style={{ background: 'linear-gradient(135deg, #0F172A 0%, #4F46E5 100%)' }}>
        <div className="pointer-events-none absolute inset-0 subtle-grid"></div>
        <div className="absolute left-[-10%] top-[-10%] h-[60%] w-[60%] rounded-full bg-primary/20 blur-[120px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] h-[40%] w-[40%] rounded-full bg-secondary/10 blur-[100px]"></div>
        <div className="relative z-10 max-w-lg">
          <h1 className="mb-lg font-headline-lg text-headline-lg text-white">
            Welcome back to the Future of Social Commerce.
          </h1>
          <div className="glass-card flex items-center gap-md rounded-xl p-lg transition-all duration-700 ease-out hover:scale-105 active:scale-95" id="sales-card">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-secondary-container">
              <span className="material-symbols-outlined text-on-secondary-container" style={{ fontVariationSettings: 'FILL 1' }}>payments</span>
            </div>
            <div>
              <p className="text-label-sm font-label-sm uppercase tracking-wider text-white/70">New Conversion</p>
              <h3 className="font-headline-md text-headline-md text-white">Sale! +$149.00 from WhatsApp</h3>
            </div>
            <div className="ml-auto">
              <span className="material-symbols-outlined text-secondary-fixed-dim">trending_up</span>
            </div>
          </div>
          <div className="mt-2xl flex gap-md">
            <div className="h-1 w-12 rounded-full bg-white"></div>
            <div className="h-1 w-2 rounded-full bg-white/30"></div>
            <div className="h-1 w-2 rounded-full bg-white/30"></div>
          </div>
        </div>
      </section>

      <section className="flex w-full flex-col justify-center bg-surface px-md py-2xl md:w-1/2 md:px-3xl">
        <div className="mb-2xl text-center md:hidden">
          <h2 className="flex items-center justify-center gap-sm text-headline-md font-headline-md text-primary">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: 'FILL 1' }}>auto_awesome</span>
            CommerceMind AI
          </h2>
        </div>

        <div className="mb-3xl hidden md:block">
          <Link className="flex items-center gap-sm text-headline-md font-headline-md text-primary" to="/">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: 'FILL 1' }}>auto_awesome</span>
            CommerceMind AI
          </Link>
        </div>

        <div className="mx-auto w-full max-w-md">
          <header className="mb-xl">
            <h2 className="mb-xs text-headline-lg-mobile font-headline-lg-mobile text-on-surface md:text-headline-lg md:font-headline-lg">Sign in to your account</h2>
            <p className="text-body-md font-body-md text-on-surface-variant">Enter your credentials to manage your AI commerce channels.</p>
          </header>

          <form className="space-y-lg" onSubmit={(event) => event.preventDefault()}>
            <div className="space-y-xs">
              <label className="text-label-sm font-label-sm text-on-surface-variant" htmlFor="email">Email Address</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-md top-1/2 -translate-y-1/2 text-outline">mail</span>
                <input className="w-full rounded-lg border border-outline-variant bg-surface-container-lowest py-md pl-[48px] pr-md text-body-md font-body-md outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/20" id="email" placeholder="name@company.com" type="email" />
              </div>
            </div>

            <div className="space-y-xs">
              <label className="text-label-sm font-label-sm text-on-surface-variant" htmlFor="password">Password</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-md top-1/2 -translate-y-1/2 text-outline">lock</span>
                <input className="w-full rounded-lg border border-outline-variant bg-surface-container-lowest py-md pl-[48px] pr-[48px] text-body-md font-body-md outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/20" id="password" placeholder="••••••••" type="password" />
                <button className="absolute right-md top-1/2 -translate-y-1/2 text-outline transition-colors hover:text-primary" type="button">
                  <span className="material-symbols-outlined">visibility</span>
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="group flex cursor-pointer items-center gap-sm">
                <input className="peer h-5 w-5 cursor-pointer rounded border-outline-variant text-primary transition-all focus:ring-primary/30" type="checkbox" />
                <span className="text-body-md font-body-md text-on-surface transition-colors group-hover:text-primary">Remember me</span>
              </label>
              <a className="text-label-sm font-label-sm text-primary transition-all hover:underline" href="#">Forgot Password?</a>
            </div>

            <button className="group flex w-full items-center justify-center gap-sm rounded-lg bg-primary py-lg text-headline-md font-headline-md text-white shadow-lg transition-all active:scale-[0.98] hover:bg-on-primary-fixed-variant" type="submit">
              Sign In
              <span className="transition-transform group-hover:translate-x-1">🚀</span>
            </button>
          </form>

          <div className="mt-xl">
            <div className="relative flex items-center py-md">
              <div className="flex-grow border-t border-outline-variant"></div>
              <span className="mx-4 flex-shrink text-label-sm font-label-sm uppercase tracking-widest text-on-surface-variant">Or continue with</span>
              <div className="flex-grow border-t border-outline-variant"></div>
            </div>
            <div className="mt-md grid grid-cols-2 gap-md">
              <button className="flex items-center justify-center gap-sm rounded-lg border border-outline-variant py-md text-label-sm font-label-sm transition-colors hover:bg-surface-container-low">
                <span className="material-symbols-outlined">google</span>
                Google
              </button>
              <button className="flex items-center justify-center gap-sm rounded-lg border border-outline-variant py-md text-label-sm font-label-sm transition-colors hover:bg-surface-container-low">
                <span className="material-symbols-outlined">cloud_circle</span>
                Salesforce
              </button>
            </div>
          </div>

          <footer className="mt-2xl text-center">
            <p className="text-body-md font-body-md text-on-surface-variant">
              Don't have an account?
              <Link className="ml-xs font-bold text-primary transition-all hover:underline" to="/register">Sign Up</Link>
            </p>
          </footer>
        </div>

        <div className="mx-auto mt-auto flex w-full max-w-md flex-wrap items-center justify-center gap-lg pt-2xl md:justify-between">
          <p className="text-label-sm font-label-sm text-outline">© 2024 CommerceMind AI</p>
          <div className="flex gap-md">
            <a className="text-label-sm font-label-sm text-outline transition-colors hover:text-on-surface-variant" href="#">Privacy</a>
            <a className="text-label-sm font-label-sm text-outline transition-colors hover:text-on-surface-variant" href="#">Terms</a>
            <a className="text-label-sm font-label-sm text-outline transition-colors hover:text-on-surface-variant" href="#">Help</a>
          </div>
        </div>
      </section>
    </main>
  )
}

export default SignInPage
