import { useQuery } from '@tanstack/react-query'
import { legacyApi } from '../api/legacy'
import { modernApi } from '../api/modern'

export default function Dashboard() {
  const legacyInfo = useQuery({ queryKey: ['legacy-info'], queryFn: legacyApi.getSystemInfo })
  const modernInfo = useQuery({ queryKey: ['modern-info'], queryFn: modernApi.getSystemInfo })
  const legacyTables = useQuery({ queryKey: ['legacy-tables'], queryFn: legacyApi.getTables })
  const modernTables = useQuery({ queryKey: ['modern-tables'], queryFn: modernApi.getTables })

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 8 }}>ERP System Overview</h1>
      <p style={{ color: 'var(--text-muted)', marginBottom: 24 }}>
        Side-by-side comparison of source and target ERP systems.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Legacy card */}
        <SystemCard
          title="Legacy ERP"
          theme="legacy"
          info={legacyInfo.data}
          tables={legacyTables.data}
          isLoading={legacyInfo.isLoading}
          isError={legacyInfo.isError}
          linkPrefix="/legacy"
        />

        {/* Modern card */}
        <SystemCard
          title="Modern ERP"
          theme="modern"
          info={modernInfo.data}
          tables={modernTables.data}
          isLoading={modernInfo.isLoading}
          isError={modernInfo.isError}
          linkPrefix="/modern"
        />
      </div>

      {/* Data quality gap callout */}
      <div style={{
        marginTop: 24,
        padding: 16,
        background: '#fff7ed',
        border: '1px solid #fed7aa',
        borderRadius: 8,
      }}>
        <div style={{ fontWeight: 600, marginBottom: 4, color: '#c2410c' }}>
          Data Quality Gap
        </div>
        <div style={{ color: '#7c3010', fontSize: 13 }}>
          Legacy system contains ~10 data quality issue types: trailing spaces, inconsistent nulls,
          near-duplicate records, orphan FKs, invalid codes, mixed date formats, unicode edge cases,
          deleted-flag rows (LOEVM=X), wrong client values, and non-padded IDs.
          The migration pipeline must detect and handle all of these.
        </div>
        <div style={{ display: 'flex', gap: 12, marginTop: 10, flexWrap: 'wrap' }}>
          {[
            'Trailing spaces (20%)',
            'Inconsistent nulls (30%)',
            'Near-duplicates (2%)',
            'Orphan FKs (1%)',
            'Invalid codes (3%)',
            'Mixed date formats',
            'Unicode edge cases',
            'Deleted markers (5%)',
            'Wrong client (0.5%)',
            'Zero-padded IDs',
          ].map(issue => (
            <span key={issue} style={{
              padding: '2px 8px',
              background: '#fef2f2',
              border: '1px solid #fecaca',
              borderRadius: 4,
              fontSize: 12,
              color: '#dc2626',
            }}>{issue}</span>
          ))}
        </div>
      </div>
    </div>
  )
}

function SystemCard({ title, theme, info, tables, isLoading, isError, linkPrefix }: {
  title: string
  theme: 'legacy' | 'modern'
  info: any
  tables: any[]
  isLoading: boolean
  isError: boolean
  linkPrefix: string
}) {
  const primary = theme === 'legacy' ? 'var(--legacy-primary)' : 'var(--modern-primary)'
  const bg = theme === 'legacy' ? 'var(--legacy-bg)' : 'var(--modern-bg)'
  const border = theme === 'legacy' ? 'var(--legacy-border)' : 'var(--modern-border)'

  const totalRecords = info?.record_count ?? (tables?.reduce((s: number, t: any) => s + (t.record_count ?? 0), 0) ?? 0)
  const tableCount = info?.table_count ?? tables?.length ?? 0

  return (
    <div style={{
      background: bg,
      border: `2px solid ${border}`,
      borderRadius: 10,
      padding: 20,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
        <h2 style={{ fontSize: 17, fontWeight: 700, color: primary }}>{title}</h2>
        <span style={{
          padding: '2px 8px',
          background: isError ? '#fef2f2' : isLoading ? '#f1f5f9' : '#f0fdf4',
          color: isError ? 'var(--danger)' : isLoading ? 'var(--text-muted)' : 'var(--success)',
          borderRadius: 4,
          fontSize: 12,
          fontWeight: 500,
        }}>
          {isLoading ? 'Connecting...' : isError ? 'Unreachable' : 'Online'}
        </span>
      </div>

      {isLoading ? (
        <div style={{ color: 'var(--text-muted)' }}>Loading...</div>
      ) : isError ? (
        <div style={{ color: 'var(--danger)' }}>Could not connect to API</div>
      ) : (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
            <Stat label="System" value={info?.system_name ?? '—'} />
            <Stat label="Type" value={info?.system_type ?? '—'} />
            <Stat label="Version" value={info?.version ?? info?.api_version ?? '—'} />
            <Stat label="Profile" value={theme === 'legacy' ? 'SAP ECC' : 'S/4HANA'} />
          </div>
          <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
            <BigStat label="Tables" value={tableCount} color={primary} />
            <BigStat label="Records" value={totalRecords.toLocaleString()} color={primary} />
          </div>
          <a href={linkPrefix} style={{
            display: 'inline-block',
            padding: '6px 14px',
            background: primary,
            color: '#fff',
            borderRadius: 6,
            fontSize: 13,
            fontWeight: 500,
            textDecoration: 'none',
          }}>
            Explore →
          </a>
        </>
      )}
    </div>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</div>
      <div style={{ fontWeight: 600, fontSize: 14 }}>{value}</div>
    </div>
  )
}

function BigStat({ label, value, color }: { label: string; value: string | number; color: string }) {
  return (
    <div style={{ flex: 1, background: 'rgba(255,255,255,0.6)', borderRadius: 8, padding: '10px 14px' }}>
      <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase' }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 800, color }}>{value}</div>
    </div>
  )
}
