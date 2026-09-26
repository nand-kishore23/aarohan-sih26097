"use client";

import React, { useState, useEffect, useRef } from 'react';

export default function VoiceDiagnosticPage() {
  const [isSupported, setIsSupported] = useState<boolean | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState('');
  const [finalTranscript, setFinalTranscript] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Check support on mount
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      setIsSupported(!!SpeechRecognition);
      
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = true;
        recognitionRef.current.interimResults = true;
        recognitionRef.current.lang = 'hi-IN';

        recognitionRef.current.onstart = () => {
          setIsListening(true);
          setErrorMsg('');
        };

        recognitionRef.current.onresult = (event: any) => {
          let interim = '';
          let finalStr = '';
          
          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              finalStr += transcript + ' ';
            } else {
              interim += transcript;
            }
          }
          
          if (finalStr) {
            setFinalTranscript(prev => prev + finalStr);
          }
          setInterimTranscript(interim);
        };

        recognitionRef.current.onerror = (event: any) => {
          console.error(event.error);
          setErrorMsg(`Error: ${event.error}`);
          setIsListening(false);
        };

        recognitionRef.current.onend = () => {
          setIsListening(false);
        };
      }
    }
  }, []);

  const startVoiceTest = () => {
    if (recognitionRef.current) {
      setInterimTranscript('');
      setFinalTranscript('');
      setErrorMsg('');
      try {
        recognitionRef.current.start();
      } catch (e: any) {
        setErrorMsg(`Failed to start: ${e.message}`);
      }
    }
  };

  const stopVoiceTest = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  const useSampleTranscript = () => {
    setFinalTranscript("Main tractor aur pump repair karta hoon, papa ke saath kaam karta hoon. Chhoti-moti machine repair kar leta hoon, lekin certificate nahi hai.");
    setInterimTranscript('');
  };

  return (
    <div className="max-w-2xl mx-auto py-10 px-4 font-sans">
      <h1 className="text-3xl font-bold text-slate-900 mb-6 border-b pb-4">AAROHAN Voice Diagnostic</h1>
      
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 mb-6 space-y-6">
        
        {/* Support Status */}
        <div className="flex items-center gap-3">
          <span className="font-semibold text-slate-700">Browser API Status:</span>
          {isSupported === null ? (
            <span className="text-slate-500">Checking...</span>
          ) : isSupported ? (
            <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">✅ SpeechRecognition supported</span>
          ) : (
            <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">❌ SpeechRecognition not supported</span>
          )}
        </div>

        {/* Microphone State */}
        <div className="flex items-center gap-3">
          <span className="font-semibold text-slate-700">Microphone State:</span>
          {isListening ? (
            <span className="flex items-center gap-2 text-red-600 font-bold animate-pulse">
              <span className="w-3 h-3 bg-red-600 rounded-full"></span> Listening...
            </span>
          ) : (
            <span className="text-slate-500">Idle</span>
          )}
        </div>

        {/* Controls */}
        <div className="flex gap-3">
          <button 
            onClick={startVoiceTest}
            disabled={!isSupported || isListening}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white font-medium py-2 px-4 rounded transition-colors"
          >
            Start Voice Test
          </button>
          <button 
            onClick={stopVoiceTest}
            disabled={!isListening}
            className="bg-red-600 hover:bg-red-700 disabled:bg-slate-300 text-white font-medium py-2 px-4 rounded transition-colors"
          >
            Stop
          </button>
          <button 
            onClick={useSampleTranscript}
            className="bg-slate-200 hover:bg-slate-300 text-slate-800 font-medium py-2 px-4 rounded transition-colors ml-auto"
          >
            Use Sample Transcript
          </button>
        </div>

        {/* Error Display */}
        {errorMsg && (
          <div className="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded text-sm font-medium">
            {errorMsg}
          </div>
        )}

        {/* Transcripts */}
        <div className="grid grid-cols-1 gap-4">
          <div>
            <p className="text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Final Transcript</p>
            <div className="w-full min-h-[100px] border border-slate-300 rounded-lg p-4 bg-slate-50 text-slate-900">
              {finalTranscript || <span className="text-slate-400 italic">No final result yet...</span>}
            </div>
          </div>
          <div>
            <p className="text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Interim Transcript</p>
            <div className="w-full min-h-[50px] border border-blue-100 rounded-lg p-3 bg-blue-50 text-blue-800">
              {interimTranscript || <span className="text-blue-300 italic">No interim result yet...</span>}
            </div>
          </div>
        </div>

      </div>
      
      <p className="text-xs text-slate-500 text-center">
        This is an isolated diagnostic page. It does not communicate with the AAROHAN backend.
      </p>
    </div>
  );
}
