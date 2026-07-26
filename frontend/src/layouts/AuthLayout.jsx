import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex font-body">
      {/* ── Left Panel: Forest Green Branding ─────────────── */}
      <div className="hidden lg:flex lg:w-1/2 bg-forest relative overflow-hidden items-center justify-center p-12">
        {/* Decorative floating shapes */}
        <div className="absolute top-16 left-16 w-32 h-32 rounded-full bg-golden/10 animate-float" />
        <div className="absolute bottom-24 right-20 w-24 h-24 rounded-full bg-accent-orange/10 animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/3 right-16 w-16 h-16 rounded-full bg-cream/5 animate-float" style={{ animationDelay: '4s' }} />
        <div className="absolute bottom-1/3 left-24 w-20 h-20 rounded-2xl bg-golden/5 rotate-12 animate-float" style={{ animationDelay: '3s' }} />
        
        {/* Branding content */}
        <div className="relative z-10 text-center max-w-md animate-fade-up">
          <div className="mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-golden/15 mb-6">
              <svg className="w-8 h-8 text-golden" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
              </svg>
            </div>
          </div>
          <h1 className="font-heading text-4xl xl:text-5xl font-bold text-cream-light mb-4 leading-tight">
            Enterprise RAG
            <span className="block text-golden mt-1">Assistant</span>
          </h1>
          <p className="text-cream-light/60 text-base leading-relaxed max-w-sm mx-auto">
            AI-powered research platform for interacting with your private knowledge base using natural language.
          </p>
          <div className="mt-10 flex items-center justify-center gap-3">
            <div className="w-8 h-[2px] bg-golden/40 rounded-full" />
            <div className="w-2 h-2 rounded-full bg-golden/50" />
            <div className="w-8 h-[2px] bg-golden/40 rounded-full" />
          </div>
        </div>
      </div>

      {/* ── Right Panel: Cream Auth Form ──────────────────── */}
      <div className="w-full lg:w-1/2 flex items-center justify-center bg-cream p-6 sm:p-12">
        <div className="w-full max-w-md animate-fade-up" style={{ animationDelay: '0.15s' }}>
          {/* Mobile-only branding */}
          <div className="lg:hidden text-center mb-8">
            <h2 className="font-heading text-3xl font-bold text-forest">
              Enterprise RAG<span className="text-golden">.</span>
            </h2>
          </div>
          
          {/* Auth card */}
          <div className="bg-cream-light rounded-3xl p-8 sm:p-10 shadow-card border border-[rgba(0,0,0,0.06)]">
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
}
