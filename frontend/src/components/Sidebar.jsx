import { useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function Sidebar() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const navItems = [
    {
      label: "Dashboard",
      path: "/dashboard",
      icon: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
        </svg>
      ),
    },
    {
      label: "AI Chat",
      path: "/chat",
      icon: (
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
        </svg>
      ),
    },
  ];

  return (
    <div className="w-64 bg-forest flex flex-col h-full dark-scrollbar relative">
      {/* ── Logo ────────────────────────────────────────── */}
      <div className="p-6 pb-2">
        <div 
          onClick={() => navigate("/dashboard")}
          className="cursor-pointer group"
        >
          <h1 className="font-heading text-2xl font-bold text-cream-light tracking-tight">
            Enterprise RAG<span className="text-golden group-hover:opacity-80 transition-opacity">.</span>
          </h1>
          <p className="text-cream-light/40 text-xs font-body mt-1 tracking-wider uppercase">
            Research Assistant
          </p>
        </div>
      </div>

      {/* ── Divider ─────────────────────────────────────── */}
      <div className="mx-6 my-4 h-px bg-cream-light/10" />

      {/* ── Navigation ──────────────────────────────────── */}
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map(item => {
          const isActive = location.pathname === item.path;
          return (
            <div
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`
                flex items-center gap-3 px-4 py-3 rounded-xl cursor-pointer 
                transition-all duration-300 ease-out group relative
                ${isActive
                  ? 'bg-cream-light/12 text-cream-light'
                  : 'text-cream-light/55 hover:bg-cream-light/6 hover:text-cream-light/85'
                }
              `}
            >
              {/* Active indicator bar */}
              <div className={`
                absolute left-0 top-1/2 -translate-y-1/2 w-[3px] rounded-full
                transition-all duration-300
                ${isActive ? 'h-6 bg-golden' : 'h-0 bg-transparent'}
              `} />
              
              <span className={`transition-colors duration-300 ${isActive ? 'text-golden' : 'text-cream-light/45 group-hover:text-cream-light/70'}`}>
                {item.icon}
              </span>
              <span className="font-medium text-sm tracking-wide">{item.label}</span>
            </div>
          );
        })}
      </nav>

      {/* ── User Section ────────────────────────────────── */}
      <div className="p-4 mx-2 mb-2">
        <div className="h-px bg-cream-light/10 mb-4" />
        <div className="flex items-center gap-3 px-2">
          {/* Avatar */}
          <div className="w-9 h-9 rounded-xl bg-golden/15 flex items-center justify-center flex-shrink-0">
            <span className="text-golden text-sm font-semibold font-body">
              {user?.email?.charAt(0)?.toUpperCase() || 'U'}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm text-cream-light/70 truncate font-body">
              {user?.email}
            </div>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="mt-3 w-full flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-body
                     text-cream-light/45 hover:text-accent-orange hover:bg-accent-orange/8
                     transition-all duration-300"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
          </svg>
          Sign Out
        </button>
      </div>
    </div>
  );
}
