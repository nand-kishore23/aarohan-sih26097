import React from 'react';

export type ProvenanceOrigin = 'SOURCE_BACKED' | 'SELF_REPORTED' | 'DERIVED' | 'SYNTHETIC' | 'MISSING';

export function ProvenanceBadge({ origin }: { origin: ProvenanceOrigin }) {
  let style = 'bg-[#151B24] text-slate-400 border-[#19212C]';
  let label = origin.replace('_', ' ');
  let icon = '⚪';

  switch (origin) {
    case 'SOURCE_BACKED':
      style = 'bg-[#062817] text-[#10B981] border-[#044E29]';
      icon = '🟢';
      break;
    case 'SELF_REPORTED':
      style = 'bg-[#0E2442] text-[#38BDF8] border-[#133A6B]';
      icon = '🔵';
      break;
    case 'DERIVED':
      style = 'bg-[#22103D] text-[#A78BFA] border-[#3B1C6B]';
      icon = '🟣';
      break;
    case 'SYNTHETIC':
      style = 'bg-[#3D1E0C] text-[#F97316] border-[#663113]';
      icon = '🟠';
      break;
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-[10px] font-semibold tracking-wider uppercase border ${style}`}>
      <span className="text-[10px] leading-none">{icon}</span>
      {label}
    </span>
  );
}
