"use client";

import React, { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { ProvenanceBadge } from '@/app/components/ProvenanceBadge';

export default function ProfilePage() {
  const params = useParams();
  const router = useRouter();
  const [ben, setBen] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/beneficiaries/${params.id}`)
      .then(r => r.json())
      .then(data => {
        setBen(data);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setLoading(false);
      });
  }, [params.id]);

  const handleRecommend = async () => {
    setGenerating(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/pathways/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ beneficiary_id: ben.id })
      });
      if (res.ok) {
        router.push(`/pathways/${ben.id}`);
      }
    } catch (e) {
      console.error(e);
      setGenerating(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-500 text-sm">Loading profile...</div>;
  if (!ben) return <div className="p-8 text-center text-red-500 text-sm">Beneficiary not found.</div>;

  return (
    <div className="max-w-4xl mx-auto py-4">
      
      <div className="mb-8 flex flex-col gap-4 border-b border-[#19212C] pb-6 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white mb-2">Beneficiary Profile</h1>
          <ProvenanceBadge origin={ben.data_origin} />
        </div>
        <button
          onClick={handleRecommend}
          disabled={generating}
          className="bg-[#00A8FF] hover:bg-[#0090DF] disabled:bg-[#151B24] disabled:text-slate-500 text-[#07090D] font-semibold py-2 px-6 rounded-md text-sm transition-colors shadow-[0_0_10px_rgba(0,168,255,0.2)]"
        >
          {generating ? 'Engine Running...' : 'Generate Pathways'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        
        {/* Basic Details */}
        <div className="bg-[#0B0F14] p-6 rounded-xl border border-[#19212C]">
          <h2 className="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">Basic Details</h2>
          <dl className="grid grid-cols-[minmax(0,auto)_minmax(0,1fr)] gap-x-4 gap-y-4 text-sm">
            <dt className="text-slate-500">Name</dt><dd className="font-medium text-slate-200">{ben.name}</dd>
            <dt className="text-slate-500">District</dt><dd className="font-medium text-slate-200">{ben.district}</dd>
            <dt className="text-slate-500">Education</dt><dd className="font-medium text-slate-200">{ben.education}</dd>
            <dt className="text-slate-500">Mobility</dt><dd className="font-medium text-slate-200">{ben.mobility_radius_km} km</dd>
            <dt className="text-slate-500">Livelihood</dt><dd className="font-medium text-slate-200 col-span-2">{ben.current_livelihood}</dd>
          </dl>
        </div>

        {/* Raw Evidence */}
        <div className="bg-[#0B0F14] p-6 rounded-xl border border-[#19212C] flex flex-col">
          <h2 className="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">Raw Evidence</h2>
          <div className="flex-1 break-words bg-[#07090D] p-4 rounded-md text-sm text-slate-400 italic border border-[#151B24] leading-relaxed">
            "{ben.raw_statement}"
          </div>
          <div className="mt-4">
            <ProvenanceBadge origin="SELF_REPORTED" />
          </div>
        </div>
      </div>

      {/* Extracted Skills */}
      <div className="bg-[#0B0F14] p-6 rounded-xl border border-[#19212C]">
        <h2 className="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">Extracted Skills</h2>
        
        {ben.skills.length === 0 ? (
          <p className="text-slate-500 text-sm">No specific skills extracted from evidence.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {ben.skills.map((skill: any, i: number) => (
              <div key={i} className="p-4 border border-[#19212C] rounded-lg bg-[#111720]">
                <div className="mb-3 flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                  <span className="break-words font-semibold text-white text-sm">{skill.normalized_skill.replace(/_/g, ' ')}</span>
                  <ProvenanceBadge origin={skill.provenance.origin} />
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Evidence: <span className="italic text-slate-300">{skill.evidence_text}</span>
                </p>
                <p className="text-[10px] text-slate-500 mt-2 font-mono">raw: "{skill.raw_skill}"</p>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}
