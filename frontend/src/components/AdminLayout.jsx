import { Outlet } from "react-router-dom";
import { Toaster } from "sonner";

export default function AdminLayout() {
  return (
    <div className="admin-shell min-h-screen bg-background">
      <main className="w-full min-w-0 max-w-[1800px] mx-auto px-4 sm:px-6 lg:px-8">
        <Outlet />
      </main>
      <Toaster position="top-right" richColors />
    </div>
  );
}
