import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";

export default function MainLayout() {
  return (
    <div className="min-h-screen flex bg-cream font-body">
      <Sidebar />
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <main className="flex-1 p-8 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
