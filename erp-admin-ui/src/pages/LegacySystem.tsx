import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { legacyApi } from '../api/legacy'

const DOMAINS = ['Vendor Master', 'Customer Master', 'Material Master', 'Finance', 'Purchasing']

export default function LegacySystem() {
  const qc = useQueryClient()
  const info = useQuery({ queryKey: ['legacy-info'], queryFn: legacyApi.getSystemInfo })
  const tables = useQuery({ queryKey: ['legacy-tables'], queryFn: legacyApi.getTables })
  const profiles = useQuery({ queryKey: ['legacy-profiles'], queryFn: legacyApi.getProfiles })

  const switchProfile = useMutation({
    mutationFn: (id: string) => legacyApi.switchProfile(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['legacy-info'] })
      qc.invalidateQueries({ queryKey: ['legacy-tables'] })
      qc.invalidateQueries({ queryKey: ['legacy-profiles'] })
    },
  })

  const tablesByDomain: Record<string, any[]> = {}
  for (const t of tables.data ?? []) {
    const d = t.domain ?? 'Other'
    if (!tablesByDomain[d]) tablesByDomain[d] = []
    tablesByDomain[d].push(t)
  }

  return (
    <div style={{ padding: 24 }}>
      {/* System info card */}
      <div style={{
        background: 'var(--legacy-bg)',
        border: '2px solid var(--legacy-border)',
        borderRadius: 10,
        padding: 20,
        marginBottom: 20,
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'space-between',
        gap: 16,
      }}>
        <div>
          <h1 style={{ fontSize: 20, fontWeight: 700, color: 'var(--legacy-primary)', marginBottom: 8 }}>
            {info.data?.system_name ?? 'Legacy ERP'} — {info.data?.system_type}
          </h1>
          <div style={{ display: 'flex', gap: 20, color: 'var(--text-muted)', fontSize: 13 }}>
            <span>Version: <b>{info.data?.version}</b></span>
            <span>Tables: <b>{info.data?.table_count}</b></span>
            <span>Records: <b>{(info.data?.record_count ?? 0).toLocaleString()}</b></span>
          </div>
        </div>

        {/* Profile switcher */}
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexShrink: 0 }}>
          <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>Profile:</span>
          {(profiles.data ?? []).map((p: any) => (
            <button
              key={p.id}
              onClick={() => switchProfile.mutate(p.id)}
              disabled={switchProfile.isPending}
              style={{
                background: p.active ? 'var(--legacy-primary)' : 'var(--border)',
                color: p.active ? '#fff' : 'var(--text)',
                fontSize: 12,
                padding: '4px 10px',
              }}
            >
              {p.name}
            </button>
          ))}
          {switchProfile.isPending && <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Switching...</span>}
        </div>
      </div>

      {/* Tables grouped by domain */}
      {DOMAINS.filter(d => tablesByDomain[d]).map(domain => (
        <div key={domain} style={{ marginBottom: 20 }}>
          <h2 style={{ fontSize: 15, fontWeight: 600, marginBottom: 8, color: 'var(--text-muted)' }}>{domain}</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {tablesByDomain[domain]?.map((t: any) => (
              <Link key={t.name} to={`/legacy/tables/${t.name}`} style={{
                padding: '8px 14px',
                background: 'var(--surface)',
                border: '1px solid var(--legacy-border)',
                borderRadius: 6,
                color: 'var(--text)',
                fontSize: 13,
                textDecoration: 'none',
              }}>
                <div style={{ fontWeight: 600 }}>{t.name}</div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                  {(t.record_count ?? 0).toLocaleString()} rows
                </div>
              </Link>
            ))}
          </div>
        </div>
      ))}
      {/* Any domains not in DOMAINS */}
      {Object.entries(tablesByDomain)
        .filter(([d]) => !DOMAINS.includes(d))
        .map(([domain, tbls]) => (
          <div key={domain} style={{ marginBottom: 20 }}>
            <h2 style={{ fontSize: 15, fontWeight: 600, marginBottom: 8, color: 'var(--text-muted)' }}>{domain}</h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {tbls.map((t: any) => (
                <Link key={t.name} to={`/legacy/tables/${t.name}`} style={{
                  padding: '8px 14px', background: 'var(--surface)',
                  border: '1px solid var(--legacy-border)', borderRadius: 6,
                  color: 'var(--text)', fontSize: 13, textDecoration: 'none',
                }}>
                  <div style={{ fontWeight: 600 }}>{t.name}</div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{(t.record_count ?? 0).toLocaleString()} rows</div>
                </Link>
              ))}
            </div>
          </div>
        ))}
    </div>
  )
}
