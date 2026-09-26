"use client";

import React from 'react';
import { usePathname } from 'next/navigation';
import { Sidebar } from './Sidebar';

export function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isAuthOrLanding = pathname === '/' || pathname === '/login' || pathname === '/signup';

  if (isAuthOrLanding) {
    return <main className="flex-1 flex flex-col min-w-0 h-[100dvh] overflow-y-auto">{children}</main>;
  }

  return (
    <>
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 h-[100dvh] overflow-y-auto md:pt-0 pt-16">
        <div className="flex-1 w-full mx-auto p-4 sm:p-6 lg:p-10">
          {children}
        </div>
      </main>
    </>
  );
}
