"use client";

import React, { useState } from 'react';
import Link from 'next/link';

type ChatResponse = {
  session_id: string;
  beneficiary_id: string;
  message: string;
  questions: string[];
  candidate_pathways: Array<{
    id: string;
    pathway_name: string;
    supporting_skills: string[];
    skill_gaps: string[];
  }>;
  transferable_skills: string[];
};

type ConversationTurn = {
  role: 'beneficiary' | 'assistant';
  text: string;
  response?: ChatResponse;
};

export default function InterviewPage() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [conversation, setConversation] = useState<ConversationTurn[]>([]);

  const demoPresets = [
    "Main tractor aur pump repair karta hoon, papa ke saath kaam karta hoon. Chhoti-moti machine repair kar leta hoon, lekin certificate nahi hai.",
    "Bijli ka kaam seekha hai, fan aur geyser banata hoon. LED bhi theek kar leta hoon.",
    "Dairy mein kaam kiya hai, doodh ka testing aur pasteurization aata hai."
  ];

  const startListening = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert("Your browser doesn't support the Web Speech API. Please type or select a preset.");
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'hi-IN';

    recognition.onstart = () => {
      setIsListening(true);
      setError('');
    };

    recognition.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0])
        .map((result) => result.transcript)
        .join('');
      setText(transcript);
    };

    recognition.onerror = (event: any) => {
      console.error(event.error);
      setIsListening(false);
      setError("Microphone error or not allowed. Please type instead.");
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const beneficiaryMessage = text.trim();
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || '') + '/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: beneficiaryMessage,
          language: 'hi',
          ...(sessionId ? { session_id: sessionId } : {})
        })
      });
      
      if (!res.ok) throw new Error('Failed to process interview');
      
      const data: ChatResponse = await res.json();
      setSessionId(data.session_id);
      setConversation((current) => [
        ...current,
        { role: 'beneficiary', text: beneficiaryMessage },
        { role: 'assistant', text: data.message, response: data }
      ]);
      setText('');
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto py-4">
      
      <div className="flex-1 overflow-y-auto pb-4 space-y-6">
        {/* System Message */}
        <div className="flex gap-4">
          <div className="w-8 h-8 rounded-full bg-[#111720] border border-[#19212C] flex items-center justify-center flex-shrink-0 text-[#00A8FF] font-bold text-xs">
            A
          </div>
          <div className="pt-1">
            <p className="text-slate-300 text-sm leading-relaxed">
              Tell us about your work and experience. 
              <br/>
              <span className="text-slate-500 text-xs mt-1 block">Speak naturally in your preferred language.</span>
            </p>
          </div>
        </div>

        {conversation.map((turn, index) => (
          <div key={index} className={`flex gap-4 ${turn.role === 'beneficiary' ? 'justify-end' : ''}`}>
            {turn.role === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-[#111720] border border-[#19212C] flex items-center justify-center flex-shrink-0 text-[#00A8FF] font-bold text-xs">A</div>
            )}
            <div className={`max-w-xl rounded-md border p-4 text-sm leading-relaxed ${turn.role === 'beneficiary' ? 'bg-[#151B24] border-[#2D3748] text-slate-200' : 'bg-[#0B0F14] border-[#19212C] text-slate-300'}`}>
              <p>{turn.text}</p>
              {turn.response && (
                <div className="mt-4 space-y-3">
                  {turn.response.questions[0] && (
                    <p className="border-l-2 border-[#00A8FF] pl-3 text-slate-200">{turn.response.questions[0]}</p>
                  )}
                  {turn.response.transferable_skills.length > 0 && (
                    <p className="text-xs text-slate-400">Transferable skills: {turn.response.transferable_skills.join(', ').replace(/_/g, ' ')}</p>
                  )}
                  {turn.response.candidate_pathways.length > 0 && (
                    <div className="space-y-2 border-t border-[#19212C] pt-3">
                      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Candidate pathways</p>
                      {turn.response.candidate_pathways.map((pathway) => (
                        <Link key={pathway.id} href={`/pathways/${turn.response?.beneficiary_id}/${pathway.id}`} className="block rounded-md border border-[#19212C] bg-[#111720] p-3 text-slate-200 hover:border-[#00A8FF]">
                          <span className="font-medium">{pathway.pathway_name}</span>
                          <span className="mt-1 block text-xs text-slate-400">{pathway.supporting_skills.length} demonstrated skills, {pathway.skill_gaps.length} potential gaps</span>
                        </Link>
                      ))}
                      <p className="text-xs text-slate-500">OPPORTUNITY EVIDENCE INSUFFICIENT. Field validation required.</p>
                    </div>
                  )}
                  {turn.response.candidate_pathways.length === 0 && turn.response.questions.length === 0 && (
                    <p className="text-xs text-slate-500">OPPORTUNITY EVIDENCE INSUFFICIENT. Field validation required.</p>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {conversation.length === 0 && <div className="flex gap-4">
          <div className="w-8 h-8 flex-shrink-0"></div>
          <div className="flex flex-col gap-2 w-full max-w-xl">
            {demoPresets.map((preset, i) => (
              <button 
                key={i}
                type="button"
                onClick={() => setText(preset)}
                className="text-left text-xs p-3 bg-[#0B0F14] hover:bg-[#111720] border border-[#19212C] hover:border-[#2D3748] rounded-md transition-colors text-slate-400 hover:text-slate-300"
              >
                "{preset}"
              </button>
            ))}
          </div>
        </div>}
      </div>

      {/* Input Area */}
      <div className="mt-auto border-t border-[#19212C] pt-4 bg-[#07090D]">
        <form onSubmit={handleSubmit} className="relative">
          <div className={`relative rounded-xl border transition-colors bg-[#0B0F14] ${isListening ? 'border-[#00A8FF] shadow-[0_0_15px_rgba(0,168,255,0.1)]' : 'border-[#19212C] focus-within:border-[#2D3748]'}`}>
            <textarea
              className="w-full bg-transparent p-4 pb-14 text-slate-200 focus:outline-none resize-none min-h-[120px] text-sm"
              placeholder="Speak or type beneficiary statement..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              disabled={loading || isListening}
            />
            
            <div className="absolute bottom-3 left-3 right-3 flex justify-between items-center">
              <button
                type="button"
                onClick={startListening}
                className={`w-8 h-8 flex items-center justify-center rounded-md transition-all focus:outline-none ${
                  isListening 
                    ? 'bg-[#00A8FF] text-[#07090D] animate-pulse shadow-[0_0_10px_rgba(0,168,255,0.5)]' 
                    : 'bg-[#151B24] text-slate-400 hover:text-[#00A8FF] hover:bg-[#1A2332]'
                }`}
                title={isListening ? "Listening..." : "Click to speak"}
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8h-2a5 5 0 01-10 0H3a7.001 7.001 0 006 6.93V17H6v2h8v-2h-3v-2.07z" clipRule="evenodd" /></svg>
              </button>
              
              <button
                type="submit"
                disabled={loading || isListening || !text.trim()}
                className="bg-[#00A8FF] hover:bg-[#0090DF] disabled:bg-[#151B24] disabled:text-slate-500 text-[#07090D] font-semibold py-1.5 px-4 rounded-md text-sm transition-colors flex justify-center items-center"
              >
                {loading ? 'Thinking...' : 'Send'}
              </button>
            </div>
          </div>
          {error && <p className="text-red-500 mt-2 text-xs text-center">{error}</p>}
        </form>
      </div>

    </div>
  );
}
