"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

export default function EvidenceBriefPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/community/evidence-brief`)
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-8 text-center text-slate-500 text-sm">Generating Evidence Brief...</div>;
  if (!data) return <div className="p-8 text-center text-red-500 text-sm">Failed to load brief.</div>;

  return (
    <div className="max-w-3xl mx-auto py-4 font-sans">
      
      <Link href="/community" className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 hover:text-[#00A8FF] mb-6 inline-flex items-center gap-2">
        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
        Back to Dashboard
      </Link>

      <div className="rounded-lg border border-[#19212C] bg-[#0B0F14] p-5 shadow-sm sm:p-8 md:p-12">
        <div className="text-center mb-12 border-b border-[#19212C] pb-8">
          <h1 className="text-2xl font-bold text-white mb-4 uppercase tracking-widest">Livelihood Evidence Brief</h1>
          <div className="inline-block bg-[#111720] border border-[#19212C] rounded-md px-4 py-2">
            <p className="text-[#38BDF8] text-xs font-medium tracking-wide">
              {data.disclaimer_1}
            </p>
            <p className="text-slate-500 text-[10px] mt-1 uppercase tracking-wider">
              {data.disclaimer_2}
            </p>
          </div>
        </div>

        <div className="mb-10 grid gap-6 border-b border-[#19212C] pb-8 text-sm sm:grid-cols-2">
          <div>
            <span className="font-semibold text-slate-500 uppercase tracking-widest text-[10px] block mb-1">District / Area</span>
            <span className="font-medium text-slate-200 text-base">{data.district}</span>
          </div>
          <div>
            <span className="font-semibold text-slate-500 uppercase tracking-widest text-[10px] block mb-1">Data Period</span>
            <span className="font-medium text-slate-200 text-base">{data.data_period}</span>
          </div>
        </div>

        <div className="space-y-10">
          
          <section>
            <h2 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 border-l-2 border-[#19212C] pl-3">1. Beneficiary Profiles Represented</h2>
            <p className="text-base text-slate-300 font-medium pl-3">
              <span className="text-white">{data.beneficiaries_represented}</span> recorded beneficiary profiles analyzed.
            </p>
          </section>

          <section>
            <h2 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 border-l-2 border-[#19212C] pl-3">2. Observed Beneficiary Interest</h2>
            <p className="text-slate-400 leading-relaxed pl-3 text-sm">
              {data.observed_interest_summary}
            </p>
          </section>

          <section>
            <h2 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 border-l-2 border-[#19212C] pl-3">3. Training Capacity</h2>
            <p className="text-slate-400 leading-relaxed pl-3 text-sm">
              {data.training_capacity_summary}
            </p>
          </section>

          <section>
            <h2 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 border-l-2 border-[#19212C] pl-3">4. Potential Interest-Capacity Mismatch</h2>
            <div className="bg-[#111720] p-5 border-l-2 border-[#00A8FF] rounded-r-md ml-3">
              <p className="text-slate-300 text-sm leading-relaxed">
                {data.potential_mismatch_summary}
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3 border-l-2 border-[#19212C] pl-3">5. Opportunity Evidence Status</h2>
            <p className="text-slate-400 leading-relaxed pl-3 text-sm">
              {data.opportunity_evidence_status}
            </p>
          </section>

          <section className="border-t border-[#19212C] pt-8">
            <h2 className="text-[10px] font-bold text-[#F43F5E] uppercase tracking-widest mb-4">Evidence Gaps</h2>
            <ul className="space-y-2 text-slate-400 text-sm">
              {data.evidence_gaps.map((gap: string, i: number) => (
                <li key={i} className="flex gap-3">
                  <span className="text-[#F43F5E]">•</span> {gap}
                </li>
              ))}
            </ul>
          </section>

          <section className="border-t border-[#19212C] pt-8">
            <h2 className="text-[10px] font-bold text-[#00A8FF] uppercase tracking-widest mb-4">Suggested Next Validation</h2>
            <ul className="space-y-2 text-slate-400 text-sm">
              {data.suggested_next_validation.map((sug: string, i: number) => (
                <li key={i} className="flex gap-3">
                  <span className="text-[#00A8FF]">•</span> {sug}
                </li>
              ))}
            </ul>
          </section>

        </div>
      </div>
    </div>
  );
}
