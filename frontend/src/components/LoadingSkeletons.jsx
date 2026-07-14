import { Skeleton } from "./ui/skeleton";

export function LanguageCardSkeleton() {
  return (
    <div
      className="rounded-xl border bg-card p-5 space-y-3 no-hover"
      style={{ boxShadow: "var(--shadow-card)" }}
    >
      <div className="flex items-center justify-between">
        <Skeleton className="h-8 w-8 rounded-full" />
        <Skeleton className="h-5 w-16 rounded-full" />
      </div>
      <Skeleton className="h-5 w-3/4" />
      <Skeleton className="h-3 w-1/2" />
    </div>
  );
}

export function SnippetCardSkeleton() {
  return (
    <div
      className="rounded-xl border bg-card overflow-hidden no-hover"
      style={{ boxShadow: "var(--shadow-card)" }}
    >
      <div className="px-4 py-3 bg-muted flex items-center justify-between gap-2">
        <Skeleton className="h-4 w-32" />
        <div className="flex gap-2">
          <Skeleton className="h-6 w-14 rounded" />
          <Skeleton className="h-6 w-14 rounded" />
        </div>
      </div>
      <div className="p-4 space-y-3">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
        <Skeleton className="h-24 w-full rounded-lg" />
        <div className="flex gap-2">
          <Skeleton className="h-7 w-20 rounded" />
          <Skeleton className="h-7 w-20 rounded" />
          <Skeleton className="h-7 w-20 rounded" />
        </div>
      </div>
    </div>
  );
}

export function SidebarSkeleton() {
  return (
    <div
      className="rounded-xl border bg-card overflow-hidden no-hover"
      style={{ boxShadow: "var(--shadow-card)" }}
    >
      <div className="px-4 py-3 bg-muted">
        <Skeleton className="h-4 w-16" />
      </div>
      <div className="p-3 space-y-2">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-7 w-full rounded-lg" />
        ))}
      </div>
    </div>
  );
}

export function AICodeDoctorSkeleton() {
  return (
    <div
      className="rounded-xl border bg-card overflow-hidden no-hover"
      style={{ boxShadow: "var(--shadow-card)" }}
    >
      <div className="px-4 py-3 bg-muted border-b border-border">
        <Skeleton className="h-4 w-28" />
      </div>
      <div className="p-4 space-y-3">
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-24 w-full rounded-lg" />
        <Skeleton className="h-9 w-full rounded-lg" />
      </div>
    </div>
  );
}

export function StatsSkeleton() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="rounded-xl border bg-card p-6 text-center no-hover"
          style={{ boxShadow: "var(--shadow-card)" }}
        >
          <Skeleton className="h-10 w-20 mx-auto mb-2" />
          <Skeleton className="h-4 w-32 mx-auto" />
        </div>
      ))}
    </div>
  );
}

export function HeroSkeleton() {
  return (
    <div className="mb-14 text-center max-w-2xl mx-auto space-y-4">
      <Skeleton className="h-6 w-48 mx-auto rounded-full" />
      <Skeleton className="h-14 w-64 mx-auto" />
      <Skeleton className="h-6 w-56 mx-auto" />
      <Skeleton className="h-4 w-full max-w-96 mx-auto" />
    </div>
  );
}

export function PageSkeleton() {
  return (
    <div className="py-8 md:py-14 space-y-6">
      <div className="max-w-3xl mx-auto space-y-4">
        <Skeleton className="h-8 w-56 mx-auto" />
        <Skeleton className="h-4 w-full max-w-md mx-auto" />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="rounded-xl border bg-card p-5 no-hover">
            <Skeleton className="h-8 w-8 rounded-lg mb-4" />
            <Skeleton className="h-5 w-3/4 mb-3" />
            <Skeleton className="h-3 w-full" />
          </div>
        ))}
      </div>
    </div>
  );
}

export function AdminDashboardSkeleton() {
  return (
    <div className="py-6 md:py-8 space-y-6">
      <div className="rounded-xl border bg-card p-6 md:p-8 no-hover">
        <div className="flex items-center gap-3">
          <Skeleton className="h-10 w-10 rounded-lg" />
          <div className="space-y-2 flex-1">
            <Skeleton className="h-7 w-56" />
            <Skeleton className="h-4 w-full max-w-md" />
          </div>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {Array.from({ length: 5 }).map((_, index) => (
          <div key={index} className="rounded-xl border bg-card p-5 no-hover">
            <div className="flex items-center gap-3">
              <Skeleton className="h-10 w-10 rounded-lg" />
              <div className="space-y-2 flex-1">
                <Skeleton className="h-7 w-14" />
                <Skeleton className="h-3 w-20" />
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="rounded-xl border bg-card p-4 no-hover">
        <Skeleton className="h-10 w-full max-w-xl" />
      </div>
      <div className="rounded-xl border bg-card overflow-hidden no-hover">
        <div className="p-4 border-b border-border">
          <Skeleton className="h-5 w-40" />
        </div>
        <div className="p-4 space-y-3">
          {Array.from({ length: 6 }).map((_, index) => (
            <Skeleton key={index} className="h-12 w-full rounded-lg" />
          ))}
        </div>
      </div>
    </div>
  );
}
