"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { AarohanBrand } from '../components/AarohanBrand';

export default function SignupPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => router.push('/interview'), 700);
  };

  const handleDemoEntry = () => {
    setLoading(true);
    setTimeout(() => router.push('/interview'), 500);
  };

  return (
    <div className="relative flex min-h-screen flex-col bg-[#07090D] lg:flex-row">

      {/* ─── LEFT: Story ─── */}
      <div className="relative z-10 flex flex-1 flex-col justify-center px-5 py-12 sm:px-8 md:px-16 lg:px-20 lg:py-0">
        <div className="relative z-10 max-w-lg">
          <AarohanBrand className="mb-12" />

          <h1 className="text-3xl md:text-4xl font-bold text-white leading-[1.2] mb-6">
            From one voice to a <span className="text-[#00A8FF]">livelihood pathway.</span>
          </h1>

          <p className="text-slate-400 text-base leading-relaxed mb-10">
            From many voices to planning evidence. AAROHAN connects individual livelihood discovery with community-level intelligence for PM-AJAY planning.
          </p>

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="bg-[#0B0F14] border border-[#19212C] rounded-lg p-4">
              <h3 className="text-[10px] font-bold text-[#00A8FF] uppercase tracking-[0.15em] mb-2">Beneficiary</h3>
              <p className="text-xs text-slate-400 leading-relaxed">Voice → Skills → Pathway → Gaps</p>
            </div>
            <div className="bg-[#0B0F14] border border-[#19212C] rounded-lg p-4">
              <h3 className="text-[10px] font-bold text-[#00A8FF] uppercase tracking-[0.15em] mb-2">Planner</h3>
              <p className="text-xs text-slate-400 leading-relaxed">Interest → Capacity → Evidence → Review</p>
            </div>
          </div>
        </div>
      </div>

      {/* ─── RIGHT: Signup Panel ─── */}
      <div className="flex w-full flex-shrink-0 items-center justify-center bg-[#0B0F14]/50 px-5 py-12 sm:px-6 lg:w-[420px] lg:border-l lg:border-[#19212C] lg:py-0">
        <div className="w-full max-w-sm">

          <div className="flex flex-col items-center mb-8 lg:hidden">
            <AarohanBrand />
          </div>

          <div className="rounded-lg border border-[#19212C] bg-[#111720] p-5 sm:p-8">

            <h2 className="text-lg font-semibold text-white mb-1">Create your account</h2>
            <p className="text-xs text-slate-500 mb-8">Join the livelihood intelligence workspace.</p>

            <form onSubmit={handleSignup} className="space-y-4">
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">Full Name</label>
                <input
                  type="text"
                  required
                  className="w-full bg-[#07090D] border border-[#19212C] rounded-md px-4 py-2.5 text-base text-slate-200 focus:outline-none focus:border-[#00A8FF] transition-colors placeholder:text-slate-600 sm:text-sm"
                  placeholder="Ramesh Kumar"
                />
              </div>
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">Email</label>
                <input
                  type="email"
                  required
                  className="w-full bg-[#07090D] border border-[#19212C] rounded-md px-4 py-2.5 text-base text-slate-200 focus:outline-none focus:border-[#00A8FF] transition-colors placeholder:text-slate-600 sm:text-sm"
                  placeholder="demo@aarohan.local"
                />
              </div>
              <div>
                <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">Password</label>
                <input
                  type="password"
                  required
                  className="w-full bg-[#07090D] border border-[#19212C] rounded-md px-4 py-2.5 text-base text-slate-200 focus:outline-none focus:border-[#00A8FF] transition-colors placeholder:text-slate-600 sm:text-sm"
                  placeholder="••••••••"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-[#00A8FF] hover:bg-[#0090DF] text-[#07090D] font-bold py-2.5 rounded-md transition-colors mt-2 shadow-[0_0_15px_rgba(0,168,255,0.12)] flex justify-center items-center"
              >
                {loading ? (
                  <svg className="animate-spin h-5 w-5 text-[#07090D]" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/></svg>
                ) : 'Create account'}
              </button>
            </form>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-[#19212C]"></div></div>
              <div className="relative flex justify-center"><span className="bg-[#111720] px-3 text-[10px] text-slate-500 uppercase tracking-widest">or</span></div>
            </div>

            <button
              onClick={handleDemoEntry}
              disabled={loading}
              className="w-full bg-[#07090D] hover:bg-[#151B24] border border-[#19212C] hover:border-[#00A8FF]/40 text-slate-200 font-medium py-2.5 rounded-md text-sm transition-all"
            >
              Continue to demo workspace
            </button>

            <p className="text-center text-xs text-slate-500 mt-6">
              Already have an account? <Link href="/login" className="text-[#00A8FF] hover:underline">Sign in</Link>
            </p>
          </div>

        </div>
      </div>

    </div>
  );
}
