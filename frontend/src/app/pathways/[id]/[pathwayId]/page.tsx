"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { ProvenanceBadge } from '@/app/components/ProvenanceBadge';

export default function PathwayDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/pathways/${params.pathwayId}`)
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setLoading(false);
      });
  }, [params.pathwayId]);

  const handleDecision = async (decision: string) => {
    setSaving(true);
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/pathways/${params.pathwayId}/decision`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decision, notes: '' })
      });
      router.push(`/pathways/${params.id}`);
    } catch (e) {
      console.error(e);
      setSaving(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-500 text-sm">Loading pathway detail...</div>;
  if (!data || !data.candidate) return <div className="p-8 text-center text-red-500 text-sm">Pathway not found.</div>;

  const { candidate } = data;

  return (
    <div className="max-w-4xl mx-auto py-4">
      <Link href={`/pathways/${params.id}`} className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 hover:text-[#00A8FF] mb-6 inline-flex items-center gap-2">
        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
        Back to Candidate Pathways
      </Link>

      <div className="bg-[#0B0F14] rounded-xl border border-[#19212C] overflow-hidden mb-6">
        
        <div className="flex flex-col gap-4 border-b border-[#19212C] bg-[#07090D] p-4 sm:p-6 md:flex-row md:items-start md:justify-between">
          <div className="min-w-0">
            <h1 className="text-xl font-bold text-white leading-tight mb-3">{candidate.pathway_name}</h1>
            <div className="flex flex-wrap items-center gap-2 text-[11px] font-mono text-slate-400">
              <span className="bg-[#111720] px-2 py-1 rounded border border-[#19212C]">QP: {candidate.qp_code}</span>
              <span className="bg-[#111720] px-2 py-1 rounded border border-[#19212C]">NSQF Level {candidate.nsqf_level}</span>
              <span className="bg-[#111720] px-2 py-1 rounded border border-[#19212C]">{candidate.sector}</span>
            </div>
          </div>
          <ProvenanceBadge origin={candidate.provenance.origin} />
        </div>

        <div className="grid grid-cols-1 gap-8 p-4 sm:p-6 md:grid-cols-2">
            
          {/* WHY THIS PATHWAY */}
          <div>
            <h2 className="text-[10px] font-semibold text-[#10B981] uppercase tracking-widest mb-4">Why This May Fit</h2>
            {candidate.supporting_skills.length === 0 ? (
              <p className="text-slate-500 text-sm italic">No direct skill matches.</p>
            ) : (
              <ul className="space-y-3">
                {candidate.why_this.map((reason: string, i: number) => (
                  <li key={i} className="flex gap-3 text-sm text-slate-300">
                    <span className="text-[#10B981] mt-0.5">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                    </span>
                    <span className="leading-relaxed">{reason}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* SKILL GAPS */}
          <div>
            <h2 className="text-[10px] font-semibold text-[#F97316] uppercase tracking-widest mb-4">Potential Skill Gaps</h2>
            {candidate.skill_gaps.length === 0 ? (
              <p className="text-slate-500 text-sm italic">No significant skill gaps detected.</p>
            ) : (
              <ul className="space-y-3">
                {candidate.skill_gaps.map((gap: string, i: number) => (
                  <li key={i} className="flex gap-3 text-sm text-slate-300">
                    <span className="text-[#F97316] mt-0.5">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                    </span>
                    <span className="leading-relaxed">Requires {gap.replace(/_/g, ' ')}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* WHY IT MAY NOT FIT */}
          {candidate.why_not.length > 0 && (
            <div className="col-span-1 md:col-span-2 bg-[#1A1215] border border-[#3D1418] p-5 rounded-lg mt-2">
              <h2 className="text-[10px] font-semibold text-[#F43F5E] uppercase tracking-widest mb-3">Why It May Not Fit</h2>
              <ul className="space-y-2">
                {candidate.why_not.map((reason: string, i: number) => (
                  <li key={i} className="flex gap-3 text-sm text-slate-200">
                    <span className="text-[#F43F5E] mt-0.5">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                    </span>
                    {reason}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* ACCESS CONSIDERATIONS */}
          {candidate.access_constraints.length > 0 && (
            <div className="col-span-1 md:col-span-2 border-t border-[#19212C] pt-6 mt-2">
              <h2 className="text-[10px] font-semibold text-[#38BDF8] uppercase tracking-widest mb-3">Access Considerations</h2>
              <ul className="space-y-2">
                {candidate.access_constraints.map((constraint: string, i: number) => (
                  <li key={i} className="flex gap-3 text-sm text-slate-300">
                    <span className="text-[#38BDF8] mt-0.5">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    </span>
                    {constraint}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* HUMAN DECISION */}
      <div className="bg-[#111720] p-6 rounded-xl border border-[#19212C]">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-sm font-bold text-white mb-1">Human Decision</h2>
            <p className="text-slate-500 text-xs">Review candidate profile and evidence before proceeding.</p>
          </div>
          <div className="flex w-full flex-col gap-3 sm:flex-row md:w-auto">
            <button 
              onClick={() => handleDecision('interested')}
              disabled={saving}
              className="flex-1 md:flex-none bg-[#00A8FF] hover:bg-[#0090DF] text-[#07090D] py-2 px-5 rounded-md font-semibold text-sm transition-colors"
            >
              Interested
            </button>
            <button 
              onClick={() => handleDecision('need_more_info')}
              disabled={saving}
              className="flex-1 md:flex-none bg-[#151B24] hover:bg-[#1A2332] text-slate-300 border border-[#2D3748] py-2 px-5 rounded-md font-medium text-sm transition-colors"
            >
              Need Info
            </button>
            <button 
              onClick={() => handleDecision('not_suitable')}
              disabled={saving}
              className="flex-1 md:flex-none bg-[#151B24] hover:bg-[#2D1418] text-slate-300 border border-[#2D3748] hover:border-[#F43F5E] hover:text-[#F43F5E] py-2 px-5 rounded-md font-medium text-sm transition-colors"
            >
              Not Suitable
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
