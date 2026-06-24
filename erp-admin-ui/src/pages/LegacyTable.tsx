import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { legacyApi } from '../api/legacy'
import DataGrid from '../components/DataGrid'
import SchemaViewer from '../components/SchemaViewer'

export default function LegacyTable() {
  const { name } = useParams<{ name: string }>()
  const [tab, setTab] = useState<'schema' | 'data' | 'relationships'>('schema')
  const [page, setPage] = useState(0)
  const PAGE_SIZE = 100

  const schema = useQuery({
    queryKey: ['legacy-schema', name],
    queryFn: () => legacyApi.getTableSchema(name!),
  })
  const data = useQuery({
    queryKey: ['legacy-data', name, page],
    queryFn: () => legacyApi.getTableData(name!, { limit: PAGE_SIZE, offset: page * PAGE_SIZE }),
    enabled: tab === 'data',
  })
  const rels = useQuery({
    queryKey: ['legacy-rels', name],
    queryFn: () => legacyApi.getTableRelationships(name!),
    enabled: tab === 'relationships',
  })

  const columns = (schema.data?.columns ?? []).map((c: any) => ({ key: c.name, header: c.name }))

  const tabStyle = (active: boolean): React.CSSProperties => ({
    padding: '8px 16px',
    fontWeight: 500,
    fontSize: 13,
    borderBottom: active ? '2px solid var(--legacy-primary)' : '2px solid transparent',
    color: active ? 'var(--legacy-primary)' : 'var(--text-muted)',
    cursor: 'pointer',
    background: 'none',
    borderRadius: 0,
  })

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 12 }}>
        <Link to="/legacy" style={{ color: 'var(--text-muted)', fontSize: 13, textDecoration: 'none' }}>← Legacy ERP</Link>
      </div>
      <h1 style={{ fontSize: 20, fontWeight: 700, marginBottom: 4 }}>{name}</h1>
      <div style={{ color: 'var(--text-muted)', fontSize: 13, marginBottom: 16 }}>
        {schema.data?.columns?.length ?? 0} columns
      </div>

      {/* Tab bar */}
      <div style={{ display: 'flex', borderBottom: '1px solid var(--border)', marginBottom: 16 }}>
        {(['schema', 'data', 'relationships'] as const).map(t => (
          <button key={t} onClick={() => setTab(t)} style={tabStyle(tab === t)}>
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {tab === 'schema' && (
        schema.isLoading ? <div>Loading...</div> :
        <SchemaViewer columns={schema.data?.columns ?? []} mode="legacy" />
      )}

      {tab === 'data' && (
        data.isLoading ? <div>Loading...</div> :
        <DataGrid
          columns={columns}
          data={data.data?.records ?? []}
          total={data.data?.total ?? 0}
          page={page}
          pageSize={PAGE_SIZE}
          onPageChange={p => { setPage(p) }}
          dqMode
        />
      )}

      {tab === 'relationships' && (
        rels.isLoading ? <div>Loading...</div> :
        <div>
          {(rels.data ?? []).length === 0 ? (
            <div style={{ color: 'var(--text-muted)' }}>No foreign key relationships for this table.</div>
          ) : (
            <table style={{ borderCollapse: 'collapse', fontSize: 13 }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border)' }}>
                  {['From Table', 'From Column', 'To Table', 'To Column'].map(h => (
                    <th key={h} style={{ padding: '8px 12px', textAlign: 'left', fontWeight: 600, color: 'var(--text-muted)', fontSize: 12 }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(rels.data ?? []).map((r: any, i: number) => (
                  <tr key={i} style={{ borderBottom: '1px solid var(--border)' }}>
                    <td style={{ padding: '6px 12px' }}>{r.from_table}</td>
                    <td style={{ padding: '6px 12px', fontFamily: 'monospace' }}>{r.from_column}</td>
                    <td style={{ padding: '6px 12px' }}>{r.to_table}</td>
                    <td style={{ padding: '6px 12px', fontFamily: 'monospace' }}>{r.to_column}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  )
}
