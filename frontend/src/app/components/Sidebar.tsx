"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { AarohanBrand } from './AarohanBrand';

export interface SessionData {
  id: string;
  title: string;
  timestamp: number;
  profileId?: string;
}

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [sessions, setSessions] = useState<SessionData[]>([]);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAccountMenuOpen, setIsAccountMenuOpen] = useState(false);

  const isAuthOrLanding = pathname === '/' || pathname === '/login' || pathname === '/signup';

  useEffect(() => {
    if (isAuthOrLanding) return;

    const loadSessions = () => {
      try {
        const stored = localStorage.getItem('aarohan_sessions');
        if (stored) setSessions(JSON.parse(stored));
      } catch (e) { /* ignore */ }
    };

    loadSessions();
    window.addEventListener('aarohan_session_update', loadSessions);
    return () => window.removeEventListener('aarohan_session_update', loadSessions);
  }, [pathname, isAuthOrLanding]);

  const handleNewSession = () => {
    router.push('/interview');
    if (window.innerWidth < 768) setIsMobileMenuOpen(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('aarohan_sessions');
    setSessions([]);
    router.push('/login');
  };

  const closeMobile = () => setIsMobileMenuOpen(false);

  const isActive = (path: string) => pathname === path || pathname.startsWith(path + '/');

  if (isAuthOrLanding) return null;

  const navLinks = [
    { href: '/interview', label: 'Beneficiary', icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /> },
    { href: '/community', label: 'Community Intelligence', icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /> },
    { href: '/community/evidence-brief', label: 'Evidence Brief', icon: <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /> },
  ];

  // Group sessions by day
  const today = new Date(); today.setHours(0,0,0,0);
  const yesterday = new Date(today); yesterday.setDate(yesterday.getDate() - 1);
  const todaySessions = sessions.filter(s => s.timestamp >= today.getTime());
  const yesterdaySessions = sessions.filter(s => s.timestamp >= yesterday.getTime() && s.timestamp < today.getTime());
  const earlierSessions = sessions.filter(s => s.timestamp < yesterday.getTime());

  const SessionGroup = ({ label, items }: { label: string; items: SessionData[] }) => {
    if (items.length === 0) return null;
    return (
      <div className="mb-2">
        <p className="text-[9px] font-medium text-slate-600 uppercase tracking-widest px-3 mb-1">{label}</p>
        {items.slice(0, 5).map(session => (
          <Link
            key={session.id}
            href={session.profileId ? `/profile/${session.profileId}` : '/interview'}
            onClick={closeMobile}
            className="block px-3 py-1.5 text-[13px] text-slate-500 hover:text-slate-200 hover:bg-[#111720] rounded-md transition-colors truncate"
            title={session.title}
          >
            {session.title}
          </Link>
        ))}
      </div>
    );
  };

  return (
    <>
      {/* Mobile header */}
      <div className="md:hidden fixed top-0 left-0 right-0 h-14 bg-[#07090D] border-b border-[#19212C] flex items-center justify-between px-4 z-50">
        <AarohanBrand markSize={23} />
        <button aria-label={isMobileMenuOpen ? 'Close navigation' : 'Open navigation'} onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="flex h-11 w-11 items-center justify-center text-slate-400 hover:text-white transition-colors">
          {isMobileMenuOpen ? (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" /></svg>
          )}
        </button>
      </div>

      {/* Mobile overlay */}
      {isMobileMenuOpen && <div className="md:hidden fixed inset-0 bg-black/60 z-40" onClick={closeMobile} />}

      {/* Sidebar */}
      <aside className={`fixed md:sticky top-0 left-0 h-[100dvh] w-60 bg-[#07090D] border-r border-[#19212C] flex flex-col flex-shrink-0 z-50 transform transition-transform duration-200 ease-out ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>

        {/* Logo */}
        <div className="p-5 pb-3 hidden md:block">
          <AarohanBrand />
        </div>

        {/* New Session */}
        <div className="px-3 pt-4 md:pt-2 pb-2">
          <button
            onClick={handleNewSession}
            className="w-full bg-[#0B0F14] hover:bg-[#111720] text-slate-300 hover:text-white border border-[#19212C] hover:border-[#00A8FF]/40 py-2 px-3 rounded-md text-sm font-medium transition-all flex items-center gap-2.5 group"
          >
            <svg className="w-4 h-4 text-[#00A8FF]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
            New Session
          </button>
        </div>

        {/* Scrollable area */}
        <div className="flex-1 overflow-y-auto px-3 py-2 flex flex-col gap-5">

          {/* Recent Sessions */}
          {sessions.length > 0 && (
            <div>
              <h2 className="text-[10px] font-semibold text-slate-600 uppercase tracking-widest mb-2 px-3">Recent</h2>
              <SessionGroup label="Today" items={todaySessions} />
              <SessionGroup label="Yesterday" items={yesterdaySessions} />
              <SessionGroup label="Earlier" items={earlierSessions} />
            </div>
          )}

          {/* Navigation */}
          <div>
            <h2 className="text-[10px] font-semibold text-slate-600 uppercase tracking-widest mb-2 px-3">Workspace</h2>
            <nav className="flex flex-col gap-0.5">
              {navLinks.map(link => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={closeMobile}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2.5 border ${
                    isActive(link.href)
                      ? 'bg-[#111720] text-white border-[#19212C]'
                      : 'text-slate-500 hover:text-slate-200 hover:bg-[#0B0F14] border-transparent'
                  }`}
                >
                  <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">{link.icon}</svg>
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>

        </div>

        {/* Bottom */}
        <div className="p-3 border-t border-[#19212C] space-y-2">
          <div className="px-3 flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-[#38BDF8] rounded-full"></div>
            <span className="text-[10px] text-slate-600 uppercase tracking-[0.15em] font-medium">SIH 2026 • Prototype</span>
          </div>
          <div className="relative">
            <button
              aria-expanded={isAccountMenuOpen}
              aria-haspopup="menu"
              className="w-full rounded-md px-3 py-2 text-left transition-colors hover:bg-[#111720] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#42C7FF]"
              onClick={() => setIsAccountMenuOpen(!isAccountMenuOpen)}
              type="button"
            >
              <span className="flex items-center gap-2.5">
                <span className="flex h-7 w-7 items-center justify-center border border-[#1E536E] bg-[#0B1017] text-xs font-semibold text-[#42C7FF]">D</span>
                <span className="min-w-0 flex-1"><span className="block truncate text-sm font-medium text-slate-200">Demo User</span><span className="block truncate text-[10px] text-slate-500">Beneficiary Workspace</span></span>
                <svg aria-hidden="true" className="h-4 w-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="m7 10 5 5 5-5" strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} /></svg>
              </span>
            </button>
            {isAccountMenuOpen && (
              <div className="absolute bottom-full left-0 right-0 mb-2 border border-[#1E3140] bg-[#0B1017] p-1 shadow-xl" role="menu">
                <button className="w-full px-3 py-2 text-left text-sm text-slate-300 hover:bg-[#111720]" role="menuitem" type="button">Account</button>
                <button className="w-full px-3 py-2 text-left text-sm text-slate-500 hover:bg-[#111720] hover:text-white" onClick={handleLogout} role="menuitem" type="button">Sign out</button>
              </div>
            )}
          </div>
        </div>

      </aside>
    </>
  );
}
