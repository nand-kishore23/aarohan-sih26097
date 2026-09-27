"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { ProvenanceBadge } from '@/app/components/ProvenanceBadge';

export default function PathwaysListPage() {
  const params = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/pathways/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ beneficiary_id: params.id })
    })
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setLoading(false);
      });
  }, [params.id]);

  if (loading) return <div className="p-8 text-center text-slate-500 text-sm">Running deterministic engine...</div>;
  if (!data) return <div className="p-8 text-center text-red-500 text-sm">Error loading pathways.</div>;

  return (
    <div className="max-w-4xl mx-auto py-4">
      
      <div className="mb-8 border-b border-[#19212C] pb-6 flex flex-col md:flex-row md:justify-between md:items-end gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">Candidate Pathways</h1>
          <p className="text-sm text-slate-400">Based on evidence from Beneficiary Profile</p>
        </div>
      </div>

      {data.count === 0 ? (
        <div className="bg-[#0B0F14] p-10 rounded-xl border border-[#19212C] text-center">
          <p className="text-base font-semibold text-slate-300 mb-2">No supported candidate pathways found</p>
          <p className="text-slate-500 text-sm">Evidence does not meet the minimum requirements for the current qualification catalogue.</p>
          <Link href={`/profile/${params.id}`} className="mt-6 inline-block text-[#00A8FF] hover:text-[#38BDF8] text-sm font-medium">
            ← Back to Profile
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {data.pathways.map((pathway: any) => (
            <Link 
              href={`/pathways/${params.id}/${pathway.id}`} 
              key={pathway.id}
              className="block bg-[#0B0F14] rounded-xl border border-[#19212C] hover:border-[#00A8FF] hover:bg-[#111720] transition-all p-6 group"
            >
              <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <h2 className="text-lg font-bold text-slate-200 group-hover:text-[#00A8FF] transition-colors mb-2">
                    {pathway.pathway_name}
                  </h2>
                  <div className="flex items-center gap-2 text-[11px] text-slate-400 font-medium font-mono">
                    <span className="bg-[#151B24] border border-[#19212C] px-2 py-1 rounded">QP: {pathway.qp_code}</span>
                    <span className="bg-[#151B24] border border-[#19212C] px-2 py-1 rounded">NSQF Level {pathway.nsqf_level}</span>
                  </div>
                </div>
                <ProvenanceBadge origin={pathway.provenance.origin} />
              </div>

              <div className="mt-6 grid gap-4 sm:grid-cols-2">
                <div className="bg-[#07090D] p-3 rounded-md border border-[#151B24]">
                  <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest">Supported By</span>
                  <div className="mt-1 text-sm font-medium text-[#38BDF8]">
                    {pathway.supporting_skills.length} matching skills
                  </div>
                </div>
                <div className="bg-[#07090D] p-3 rounded-md border border-[#151B24]">
                  <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-widest">Potential Gaps</span>
                  <div className="mt-1 text-sm font-medium text-[#F97316]">
                    {pathway.skill_gaps.length} missing competencies
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
