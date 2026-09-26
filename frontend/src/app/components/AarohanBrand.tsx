import Link from "next/link";

type AarohanMarkProps = {
  size?: number;
  className?: string;
};

export function AarohanMark({ size = 32, className = "" }: AarohanMarkProps) {
  return (
    <svg aria-hidden="true" className={className} fill="none" height={size} viewBox="0 0 32 32" width={size} xmlns="http://www.w3.org/2000/svg">
      <path d="M5 24.5 12.2 17.3l4.1 4.1L27 10.7" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" />
      <path d="M20.5 10.7H27v6.5" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" />
      <path d="M8 26.5h16" stroke="currentColor" strokeLinecap="round" strokeWidth="2" />
    </svg>
  );
}

type AarohanBrandProps = {
  href?: string;
  markSize?: number;
  className?: string;
};

export function AarohanBrand({ href = "/", markSize = 32, className = "" }: AarohanBrandProps) {
  return (
    <Link aria-label="AAROHAN home" className={`inline-flex items-center gap-3 text-white ${className}`} href={href}>
      <span className="flex h-9 w-9 items-center justify-center border border-[#1E3140] bg-[#0B1017] text-[#42C7FF]">
        <AarohanMark size={markSize} />
      </span>
      <span className="text-sm font-bold tracking-[0.24em]">AAROHAN</span>
    </Link>
  );
}
