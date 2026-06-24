import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { modernApi } from '../api/modern'

export default function ModernSystem() {
  const info = useQuery({ queryKey: ['modern-info'], queryFn: modernApi.getSystemInfo })
  const tables = useQuery({ queryKey: ['modern-tables'], queryFn: modernApi.getTables })

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
        background: 'var(--modern-bg)',
        border: '2px solid var(--modern-border)',
        borderRadius: 10,
        padding: 20,
        marginBottom: 20,
      }}>
        <h1 style={{ fontSize: 20, fontWeight: 700, color: 'var(--modern-primary)', marginBottom: 8 }}>
          {info.data?.system_name ?? 'Modern ERP'} — SAP S/4HANA
        </h1>
        <div style={{ display: 'flex', gap: 20, color: 'var(--text-muted)', fontSize: 13, flexWrap: 'wrap' }}>
          <span>API Version: <b>{info.data?.api_version ?? '—'}</b></span>
          <span>Validation: <b style={{ color: info.data?.supports_validation ? 'var(--success)' : 'var(--danger)' }}>
            {info.data?.supports_validation ? 'Supported' : 'Not supported'}
          </b></span>
          <span>Max Batch: <b>{(info.data?.max_batch_size ?? 0).toLocaleString()} records</b></span>
          <span>Tables: <b>{tables.data?.length ?? 0}</b></span>
        </div>
      </div>

      {/* Tables grouped by domain */}
      {Object.entries(tablesByDomain).map(([domain, tbls]) => (
        <div key={domain} style={{ marginBottom: 20 }}>
          <h2 style={{ fontSize: 15, fontWeight: 600, marginBottom: 8, color: 'var(--text-muted)' }}>{domain}</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {tbls.map((t: any) => (
              <Link key={t.name} to={`/modern/tables/${t.name}`} style={{
                padding: '8px 14px',
                background: 'var(--surface)',
                border: '1px solid var(--modern-border)',
                borderRadius: 6,
                color: 'var(--text)',
                fontSize: 13,
                textDecoration: 'none',
              }}>
                <div style={{ fontWeight: 600 }}>{t.name}</div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                  {(t.record_count ?? 0).toLocaleString()} rows
                </div>
                <div style={{ display: 'flex', gap: 4, marginTop: 4 }}>
                  {t.validate_supported && (
                    <span style={{ fontSize: 10, padding: '1px 4px', background: '#eff6ff', color: 'var(--modern-primary)', borderRadius: 3, border: '1px solid var(--modern-border)' }}>VALIDATE</span>
                  )}
                  {t.load_supported && (
                    <span style={{ fontSize: 10, padding: '1px 4px', background: '#f0fdf4', color: '#16a34a', borderRadius: 3, border: '1px solid #86efac' }}>LOAD</span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
