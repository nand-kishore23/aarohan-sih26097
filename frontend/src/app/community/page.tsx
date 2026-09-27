"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { ProvenanceBadge } from '@/app/components/ProvenanceBadge';

export default function CommunityDashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/community/summary`)
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

  if (loading) return <div className="p-8 text-center text-slate-500 text-sm">Loading community intelligence...</div>;
  if (!data) return <div className="p-8 text-center text-red-500 text-sm">Failed to load data.</div>;

  return (
    <div className="max-w-5xl mx-auto py-4">
      
      <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-6 mb-8 border-b border-[#19212C] pb-6">
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">Community Intelligence</h1>
          <p className="flex flex-wrap gap-x-2 gap-y-1 text-sm text-slate-400 font-mono">
            District: <span className="text-slate-300">{data.district}</span> &nbsp;|&nbsp; Period: <span className="text-slate-300">{data.data_period}</span>
          </p>
        </div>
        <div className="flex flex-col items-start gap-3 md:items-end">
          <Link href="/community/evidence-brief" className="bg-[#111720] hover:bg-[#151B24] border border-[#19212C] text-slate-200 font-medium py-2 px-5 rounded-md text-sm transition-colors flex items-center gap-2">
            <svg className="w-4 h-4 text-[#00A8FF]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            Evidence Brief
          </Link>
        </div>
      </div>

      {/* Top Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
        <div className="bg-[#0B0F14] p-5 rounded-xl border border-[#19212C]">
          <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">Profiles Analyzed</p>
          <p className="text-3xl font-light text-white">{data.beneficiaries_represented}</p>
          <div className="mt-3"><ProvenanceBadge origin="SYNTHETIC" /></div>
        </div>
        <div className="bg-[#0B0F14] p-5 rounded-xl border border-[#19212C]">
          <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">Observed Interest</p>
          <p className="text-3xl font-light text-[#00A8FF]">
            {data.pathways.reduce((acc: number, p: any) => acc + p.observed_interest_count, 0)}
          </p>
          <div className="mt-3"><ProvenanceBadge origin="DERIVED" /></div>
        </div>
        <div className="bg-[#0B0F14] p-5 rounded-xl border border-[#19212C]">
          <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">Training Capacity</p>
          <p className="text-3xl font-light text-[#10B981]">
            {data.pathways.reduce((acc: number, p: any) => acc + p.training_capacity, 0)}
          </p>
          <div className="mt-3"><ProvenanceBadge origin="SYNTHETIC" /></div>
        </div>
        <div className="bg-[#0B0F14] p-5 rounded-xl border border-[#19212C]">
          <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest mb-2">Primary Gap</p>
          <p className="text-lg font-medium text-slate-200 mt-3 truncate">
            {data.pathways.some((p:any) => p.interest_capacity_gap > 20) ? "Capacity Shortfall" : "Balanced"}
          </p>
          <div className="mt-4"><ProvenanceBadge origin="DERIVED" /></div>
        </div>
      </div>

      <h2 className="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">Pathway Breakdown</h2>
      
      <div className="space-y-3">
        {data.pathways.map((p: any) => (
          <div key={p.pathway_id} className="bg-[#0B0F14] p-5 rounded-xl border border-[#19212C] flex flex-col md:flex-row gap-6 items-center hover:border-[#2D3748] transition-colors">
            
            <div className="flex-1 w-full">
              <h3 className="font-bold text-base text-slate-200">{p.pathway_name}</h3>
              <p className="text-xs text-slate-500 mb-3 font-mono">ID: {p.qualification_id}</p>
              
              <div>
                {p.opportunity_evidence_status === "OPPORTUNITY EVIDENCE INSUFFICIENT" ? (
                  <span className="inline-flex items-center gap-1.5 text-[10px] font-semibold text-[#F97316] bg-[#3D1E0C] border border-[#663113] px-2 py-0.5 rounded-md uppercase tracking-wide">
                    ⚪ Insufficient Evidence
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1.5 text-[10px] font-semibold text-[#10B981] bg-[#062817] border border-[#044E29] px-2 py-0.5 rounded-md uppercase tracking-wide">
                    🟢 Evidence Available
                  </span>
                )}
              </div>
            </div>
            
            <div className="flex w-full flex-wrap items-center justify-between gap-4 md:w-auto md:flex-nowrap md:justify-end md:gap-6">
              <div className="text-right">
                <p className="text-[10px] text-slate-500 uppercase font-semibold tracking-wider">Interest</p>
                <p className="text-xl font-light text-slate-300">{p.observed_interest_count}</p>
              </div>
              <div className="text-right">
                <p className="text-[10px] text-slate-500 uppercase font-semibold tracking-wider">Capacity</p>
                <p className="text-xl font-light text-slate-300">{p.training_capacity}</p>
              </div>
              <div className="min-w-[110px] bg-[#111720] px-3 py-3 text-right rounded-md border border-[#19212C] sm:min-w-[130px] sm:px-4">
                <p className="text-[10px] text-slate-500 uppercase font-semibold tracking-wider mb-1">Mismatch</p>
                <p className={`text-sm font-medium ${p.interest_capacity_gap > 20 ? 'text-[#F43F5E]' : p.interest_capacity_gap < -20 ? 'text-[#00A8FF]' : 'text-[#10B981]'}`}>
                  {p.mismatch_status}
                </p>
                <p className="text-[11px] font-mono text-slate-400 mt-1">Gap: {p.interest_capacity_gap > 0 ? '+' : ''}{p.interest_capacity_gap}</p>
              </div>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}
