import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Dashboard from './pages/Dashboard'
import LegacySystem from './pages/LegacySystem'
import LegacyTable from './pages/LegacyTable'
import ModernSystem from './pages/ModernSystem'
import ModernTable from './pages/ModernTable'
import LoadManager from './pages/LoadManager'
import Config from './pages/Config'

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, staleTime: 30_000 } },
})

const navStyle: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: 4,
  padding: '0 24px',
  height: 48,
  background: '#1e293b',
  color: '#e2e8f0',
  fontSize: 13,
  fontWeight: 500,
}

const linkStyle = (isActive: boolean): React.CSSProperties => ({
  padding: '6px 12px',
  borderRadius: 6,
  color: isActive ? '#fff' : '#94a3b8',
  background: isActive ? '#334155' : 'transparent',
  transition: 'all 0.15s',
})

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <nav style={navStyle}>
          <span style={{ fontWeight: 700, marginRight: 16, color: '#fff' }}>ERP Admin</span>
          {[
            ['/', 'Dashboard'],
            ['/legacy', 'Legacy ERP'],
            ['/modern', 'Modern ERP'],
            ['/load-manager', 'Load Manager'],
            ['/config', 'Config'],
          ].map(([to, label]) => (
            <NavLink key={to} to={to} end={to === '/'} style={({ isActive }) => linkStyle(isActive)}>
              {label}
            </NavLink>
          ))}
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/legacy" element={<LegacySystem />} />
          <Route path="/legacy/tables/:name" element={<LegacyTable />} />
          <Route path="/modern" element={<ModernSystem />} />
          <Route path="/modern/tables/:name" element={<ModernTable />} />
          <Route path="/load-manager" element={<LoadManager />} />
          <Route path="/config" element={<Config />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
