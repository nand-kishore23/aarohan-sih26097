"use client";

import Link from "next/link";
import { useState } from "react";
import { AarohanBrand } from "./components/AarohanBrand";

type Capability = {
  id: string;
  number: string;
  label: string;
  headline: string;
  body: string;
  flow: string[];
  tag: string;
  note?: string;
};

const capabilities: Capability[] = [
  { id: "local-voice", number: "01", label: "LOCAL VOICE", headline: "Designed for the way people communicate.", body: "AAROHAN starts with conversation instead of a form. Beneficiaries can express their experience, interests and aspirations through voice, with support for regional-language and dialect interaction.", flow: ["VOICE", "UNDERSTANDING", "STRUCTURED PROFILE"], tag: "Voice-first", note: "Prototype voice interaction: Hindi" },
  { id: "informal-skills", number: "02", label: "INFORMAL SKILLS", headline: "Experience counts, even when there is no certificate.", body: "A person may repair tractors, work with farm equipment, help in a family trade or perform skilled work without formal certification. AAROHAN converts this lived experience into structured, transferable skill signals.", flow: ["LIVED EXPERIENCE", "SKILL EXTRACTION", "TRANSFERABLE SKILLS"], tag: "Informal to structured" },
  { id: "nsqf-pathways", number: "03", label: "NSQF PATHWAYS", headline: "From what someone can do to what they can train for.", body: "AAROHAN connects identified skills and gaps with documented NSQF-aligned qualification pathways instead of presenting generic career suggestions.", flow: ["CURRENT SKILLS + SKILL GAPS", "NSQF-ALIGNED PATHWAY"], tag: "Explainable pathway mapping" },
  { id: "local-opportunity", number: "04", label: "LOCAL OPPORTUNITY", headline: "Recommendations should respect the place people live.", body: "AAROHAN keeps local context in the decision process, including mobility, livelihood preferences and available opportunity evidence, rather than treating every beneficiary as if they live in the same labour market.", flow: ["PERSON + PLACE + OPPORTUNITY EVIDENCE", "CONTEXT-AWARE PATHWAY"], tag: "Evidence-aware context", note: "Opportunity evidence may be insufficient. Field validation required." },
  { id: "community-evidence", number: "05", label: "COMMUNITY EVIDENCE", headline: "One voice helps a person. Many voices help planners see patterns.", body: "AAROHAN aggregates beneficiary-level signals into anonymized community evidence, helping planners compare observed beneficiary interest, training capacity and available opportunity evidence.", flow: ["MANY BENEFICIARY VOICES", "AGGREGATED SIGNALS", "COMMUNITY EVIDENCE"], tag: "Observed beneficiary interest", note: "Potential interest-capacity mismatch" },
  { id: "human-decision", number: "06", label: "HUMAN DECISION", headline: "AI supports the decision. People remain responsible for it.", body: "AAROHAN explains pathways, skill gaps and evidence so beneficiaries, reviewers and planners can make informed decisions. It does not automatically approve government plans or replace human review.", flow: ["AI ANALYSIS + EVIDENCE + HUMAN REVIEW", "DECISION"], tag: "Human-in-the-loop" },
];

const differentiators = [
  ["01", "VOICE-FIRST", "Conversation instead of form-heavy data collection."],
  ["02", "INDIAN CONTEXT", "Designed around regional-language interaction, local realities and informal livelihoods."],
  ["03", "SKILL TRANSLATION", "Turns lived work experience into structured skill signals."],
  ["04", "NSQF-ALIGNED", "Connects skills and gaps to documented qualification pathways."],
  ["05", "EVIDENCE LAYER", "Turns many beneficiary signals into community-level planning evidence."],
  ["06", "HUMAN DECISION", "Supports people making decisions instead of pretending AI should make them."],
];

export default function Home() {
  const [activeId, setActiveId] = useState<string | null>(null);
  const activeCapability = capabilities.find((capability) => capability.id === activeId);

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#07090D] font-sans text-slate-200">
      <nav className="mx-auto flex w-full max-w-7xl items-center justify-between px-5 py-5 sm:px-8">
        <AarohanBrand />
        <div className="flex items-center gap-3">
          <Link className="px-3 py-2 text-sm font-medium text-slate-300 transition-colors hover:text-white" href="/login">Sign in</Link>
          <Link className="hidden border border-[#1E3140] bg-[#0B1017] px-3 py-2 text-sm font-medium text-white transition-colors hover:border-[#42C7FF] sm:block" href="/signup">Create account</Link>
        </div>
      </nav>

      <main>
        <section className="mx-auto flex w-full max-w-6xl flex-col items-center px-5 pb-20 pt-16 text-center sm:px-8 sm:pt-24">
          <p className="mb-7 text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">SIH 2026 • PROTOTYPE</p>
          <h1 className="max-w-4xl text-4xl font-semibold leading-[1.08] text-white sm:text-5xl md:text-6xl">Livelihood intelligence,<br />built around the way people speak.</h1>
          <p className="mt-7 max-w-2xl text-base leading-7 text-slate-400 sm:text-lg">AAROHAN turns beneficiary voices into structured skills, NSQF-aligned livelihood pathways and community-level planning evidence.</p>
          <p className="mt-3 text-sm leading-6 text-slate-500">Designed for regional-language interaction, informal livelihoods and low-literacy environments.</p>
        </section>

        <section aria-labelledby="differentiators-heading" className="border-y border-[#182431] bg-[#090D13]">
          <div className="mx-auto w-full max-w-7xl px-5 py-14 sm:px-8 md:py-20">
            <div className="mb-10 text-center">
              <p className="text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">WHAT MAKES AAROHAN DIFFERENT</p>
              <h2 className="mt-3 text-xl font-medium text-white sm:text-2xl" id="differentiators-heading">Select a capability to explore.</h2>
            </div>
            <div className="grid items-stretch gap-7 lg:grid-cols-[250px_minmax(0,1fr)] lg:gap-12">
              <div aria-label="AAROHAN capabilities" className="capability-selector" role="tablist">
                {capabilities.map((capability) => {
                  const isActive = capability.id === activeId;
                  return <button aria-controls="capability-stage" aria-selected={isActive} className={`capability-node ${isActive ? "is-active" : ""}`} key={capability.id} onClick={() => setActiveId(capability.id)} role="tab" type="button"><span className="capability-number">{capability.number}</span><span>{capability.label}</span><span aria-hidden="true" className="capability-connector" /></button>;
                })}
              </div>
              <div aria-live="polite" className="capability-stage" id="capability-stage" role="tabpanel">
                {activeCapability ? (
                  <div className="capability-content" key={activeCapability.id}>
                    <div className="flex flex-wrap items-center gap-3"><p className="text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">{activeCapability.number} / {activeCapability.label}</p><span className="border border-[#1E536E] px-2 py-1 text-[10px] font-medium tracking-wide text-[#83D9FF]">{activeCapability.tag}</span></div>
                    <h3 className="mt-6 max-w-2xl text-3xl font-medium leading-tight text-white sm:text-4xl">{activeCapability.headline}</h3>
                    <p className="mt-5 max-w-2xl text-base leading-7 text-slate-400">{activeCapability.body}</p>
                    <div className="capability-flow mt-10">{activeCapability.flow.map((step, index) => <div className="flex items-center gap-3" key={step}><span className="capability-flow-index">0{index + 1}</span><p>{step}</p></div>)}</div>
                    {activeCapability.note && <p className="mt-7 max-w-md border-l border-[#42C7FF] pl-3 text-sm leading-6 text-slate-400">{activeCapability.note}</p>}
                    <p className="mt-10 max-w-2xl text-lg font-medium leading-7 text-white">From one voice to a livelihood pathway.<br /><span className="text-[#42C7FF]">From many voices to planning evidence.</span></p>
                  </div>
                ) : (
                  <div className="flex h-full min-h-[380px] flex-col justify-center border-l border-[#1A2734] pl-7 sm:pl-10"><p className="text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">AAROHAN / DIFFERENTIATION</p><p className="mt-5 max-w-xl text-3xl font-medium leading-tight text-white sm:text-4xl">Most systems begin with a form.<br />AAROHAN begins with a person&apos;s story.</p><p className="mt-5 max-w-lg text-base leading-7 text-slate-400">Choose a capability to see how the platform turns conversation into understandable, evidence-aware livelihood support.</p></div>
                )}
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto w-full max-w-6xl px-5 py-20 sm:px-8 md:py-28">
          <p className="text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">THE PROBLEM</p>
          <div className="mt-7 flex flex-wrap items-center gap-x-3 gap-y-3 text-base font-medium text-slate-300 sm:text-lg">{["TEXT-HEAVY SYSTEMS", "LANGUAGE & DIGITAL BARRIERS", "INFORMAL EXPERIENCE IS MISSED", "TRAINING MISMATCH", "LOCAL OPPORTUNITY GAP"].map((item, index) => <div className="flex items-center gap-3" key={item}><span>{item}</span>{index < 4 && <span aria-hidden="true" className="text-[#42C7FF]">→</span>}</div>)}</div>
          <p className="mt-9 max-w-2xl text-xl leading-8 text-white">AAROHAN addresses this gap by starting with the beneficiary&apos;s voice.</p>
        </section>

        <section className="border-y border-[#182431] bg-[#090D13]"><div className="mx-auto w-full max-w-6xl px-5 py-20 sm:px-8 md:py-24"><p className="text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">WHY AAROHAN?</p><div className="mt-9 divide-y divide-[#182431] border-y border-[#182431]">{differentiators.map(([number, title, description]) => <div className="grid gap-2 py-5 sm:grid-cols-[54px_210px_1fr] sm:items-baseline sm:gap-4" key={number}><span className="text-sm font-semibold text-[#42C7FF]">{number}</span><h3 className="text-sm font-semibold tracking-[0.08em] text-white">{title}</h3><p className="text-sm leading-6 text-slate-400">{description}</p></div>)}</div></div></section>

        <section className="mx-auto w-full max-w-6xl px-5 py-20 text-center sm:px-8 md:py-28"><p className="text-3xl font-medium leading-tight text-white sm:text-4xl">Most systems begin with a form.<br /><span className="text-[#42C7FF]">AAROHAN begins with a person&apos;s story.</span></p><p className="mt-8 text-sm font-medium tracking-wide text-slate-400">Voice <span className="px-2 text-[#42C7FF]">→</span> Understanding <span className="px-2 text-[#42C7FF]">→</span> Skills <span className="px-2 text-[#42C7FF]">→</span> Pathways <span className="px-2 text-[#42C7FF]">→</span> Evidence <span className="px-2 text-[#42C7FF]">→</span> Human Decision</p></section>

        <section className="border-t border-[#182431] bg-[#090D13]"><div className="mx-auto w-full max-w-6xl px-5 py-20 sm:px-8 md:py-24"><p className="text-center text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">BUILT FOR TWO SIDES OF THE LIVELIHOOD JOURNEY</p><div className="mt-12 grid gap-10 md:grid-cols-2 md:gap-16"><div className="border-t border-[#1E536E] pt-6"><p className="text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">BENEFICIARY</p><p className="mt-4 whitespace-pre-line text-2xl font-medium leading-9 text-white">Tell your story.{"\n"}Understand your skills.{"\n"}See possible pathways.{"\n"}Understand the gaps.</p></div><div className="border-t border-[#1E536E] pt-6"><p className="text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">PLANNER</p><p className="mt-4 whitespace-pre-line text-2xl font-medium leading-9 text-white">See aggregated signals.{"\n"}Compare training capacity.{"\n"}Review opportunity evidence.{"\n"}Support better planning.</p></div></div></div></section>

        <section className="mx-auto flex w-full max-w-6xl flex-col items-center px-5 py-20 text-center sm:px-8 md:py-28"><p className="text-[11px] font-semibold tracking-[0.18em] text-[#42C7FF]">ENTER AAROHAN</p><p className="mt-4 max-w-xl text-2xl leading-8 text-white">Voice-first livelihood intelligence for beneficiaries and community planning.</p><div className="mt-9 flex flex-col gap-3 sm:flex-row"><Link className="bg-[#42C7FF] px-6 py-3 text-sm font-semibold text-[#061018] transition-colors hover:bg-[#83D9FF]" href="/login">Sign in</Link><Link className="border border-[#1E3140] bg-[#0B1017] px-6 py-3 text-sm font-medium text-white transition-colors hover:border-[#42C7FF]" href="/interview">Continue to demo workspace</Link><Link className="px-6 py-3 text-sm font-medium text-slate-300 transition-colors hover:text-white" href="/signup">Create account</Link></div></section>
      </main>
      <footer className="border-t border-[#182431] px-5 py-8 sm:px-8"><div className="mx-auto flex w-full max-w-7xl items-center justify-between gap-4 text-xs text-slate-500"><AarohanBrand className="scale-90 origin-left" markSize={22} /><p>Voice-first livelihood intelligence</p></div></footer>
    </div>
  );
}
