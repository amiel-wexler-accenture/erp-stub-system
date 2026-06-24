import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { legacyApi } from '../api/legacy'
import { modernApi } from '../api/modern'

function useHealth(apiFn: () => Promise<any>, key: string) {
  const [healthy, setHealthy] = useState<boolean | null>(null)
  useEffect(() => {
    const check = () => apiFn().then(() => setHealthy(true)).catch(() => setHealthy(false))
    check()
    const id = setInterval(check, 30_000)
    return () => clearInterval(id)
  }, [])
  return healthy
}

export default function Config() {
  const qc = useQueryClient()

  const legacyHealth = useHealth(() => fetch('http://localhost:8001/health').then(r => { if (!r.ok) throw r }), 'legacy')
  const modernHealth = useHealth(() => fetch('http://localhost:8002/health').then(r => { if (!r.ok) throw r }), 'modern')

  const legacyProfiles = useQuery({ queryKey: ['legacy-profiles'], queryFn: legacyApi.getProfiles })
  const modernProfiles = useQuery({ queryKey: ['modern-profiles'], queryFn: modernApi.getProfiles })

  const switchLegacy = useMutation({
    mutationFn: (id: string) => legacyApi.switchProfile(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['legacy'] }),
  })

  const resetModern = useMutation({
    mutationFn: () => modernApi.resetAll(),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['modern'] }),
  })

  const HealthDot = ({ ok }: { ok: boolean | null }) => (
    <span style={{
      display: 'inline-block',
      width: 10, height: 10, borderRadius: '50%',
      background: ok === null ? '#94a3b8' : ok ? 'var(--success)' : 'var(--danger)',
      marginRight: 6,
    }} />
  )

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 24 }}>Configuration</h1>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>

        {/* Legacy config */}
        <div style={{ background: 'var(--legacy-bg)', border: '2px solid var(--legacy-border)', borderRadius: 10, padding: 20 }}>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
            <HealthDot ok={legacyHealth} />
            <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--legacy-primary)' }}>Legacy ERP</h2>
            <span style={{ marginLeft: 8, fontSize: 12, color: legacyHealth === null ? 'var(--text-muted)' : legacyHealth ? 'var(--success)' : 'var(--danger)' }}>
              {legacyHealth === null ? 'Checking...' : legacyHealth ? 'Online' : 'Offline'}
            </span>
          </div>
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 8 }}>Active Profile</div>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {(legacyProfiles.data ?? []).map((p: any) => (
                <button
                  key={p.id}
                  onClick={() => switchLegacy.mutate(p.id)}
                  disabled={switchLegacy.isPending}
                  style={{
                    background: p.active ? 'var(--legacy-primary)' : 'var(--surface)',
                    color: p.active ? '#fff' : 'var(--text)',
                    border: '1px solid var(--legacy-border)',
                    fontSize: 12,
                    padding: '5px 12px',
                  }}
                >
                  {p.name}
                </button>
              ))}
            </div>
            {switchLegacy.isPending && <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 8 }}>Switching profile — reseeding data...</div>}
            {switchLegacy.isSuccess && <div style={{ fontSize: 12, color: 'var(--success)', marginTop: 8 }}>Profile switched successfully.</div>}
          </div>
        </div>

        {/* Modern config */}
        <div style={{ background: 'var(--modern-bg)', border: '2px solid var(--modern-border)', borderRadius: 10, padding: 20 }}>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
            <HealthDot ok={modernHealth} />
            <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--modern-primary)' }}>Modern ERP</h2>
            <span style={{ marginLeft: 8, fontSize: 12, color: modernHealth === null ? 'var(--text-muted)' : modernHealth ? 'var(--success)' : 'var(--danger)' }}>
              {modernHealth === null ? 'Checking...' : modernHealth ? 'Online' : 'Offline'}
            </span>
          </div>
          <div style={{ marginBottom: 16 }}>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 8 }}>Active Profile</div>
            <div style={{ display: 'flex', gap: 8 }}>
              {(modernProfiles.data ?? []).map((p: any) => (
                <span key={p.id} style={{
                  padding: '5px 12px',
                  background: p.active ? 'var(--modern-primary)' : 'var(--surface)',
                  color: p.active ? '#fff' : 'var(--text)',
                  borderRadius: 6,
                  fontSize: 12,
                  border: '1px solid var(--modern-border)',
                }}>{p.name}</span>
              ))}
            </div>
          </div>
          <div>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 8 }}>Database Reset</div>
            <button
              onClick={() => { if (confirm('Reset all modern ERP data and reseed?')) resetModern.mutate() }}
              disabled={resetModern.isPending}
              style={{ background: 'var(--danger)', color: '#fff', fontSize: 12 }}
            >
              {resetModern.isPending ? 'Resetting...' : 'Reset & Reseed'}
            </button>
            {resetModern.isSuccess && <div style={{ fontSize: 12, color: 'var(--success)', marginTop: 8 }}>Reset complete.</div>}
          </div>
        </div>
      </div>
    </div>
  )
}
