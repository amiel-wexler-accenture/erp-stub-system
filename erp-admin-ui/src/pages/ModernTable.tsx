import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { modernApi } from '../api/modern'
import DataGrid from '../components/DataGrid'
import SchemaViewer from '../components/SchemaViewer'

const STATUS_COLORS: Record<string, string> = {
  completed: '#22c55e',
  partial: '#f59e0b',
  failed: '#ef4444',
}

export default function ModernTable() {
  const { name } = useParams<{ name: string }>()
  const [tab, setTab] = useState<'schema' | 'data' | 'history'>('schema')
  const [page, setPage] = useState(0)
  const PAGE_SIZE = 100

  const schema = useQuery({
    queryKey: ['modern-schema', name],
    queryFn: () => modernApi.getTableSchema(name!),
  })
  const data = useQuery({
    queryKey: ['modern-data', name, page],
    queryFn: () => modernApi.getTableData(name!, { limit: PAGE_SIZE, offset: page * PAGE_SIZE }),
    enabled: tab === 'data',
  })
  const history = useQuery({
    queryKey: ['modern-load-history', name],
    queryFn: () => modernApi.getLoadHistory(name!),
    enabled: tab === 'history',
  })

  const columns = (schema.data?.columns ?? []).map((c: any) => ({ key: c.name, header: c.name }))

  const tabStyle = (active: boolean): React.CSSProperties => ({
    padding: '8px 16px',
    fontWeight: 500,
    fontSize: 13,
    borderBottom: active ? '2px solid var(--modern-primary)' : '2px solid transparent',
    color: active ? 'var(--modern-primary)' : 'var(--text-muted)',
    cursor: 'pointer',
    background: 'none',
    borderRadius: 0,
  })

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 12 }}>
        <Link to="/modern" style={{ color: 'var(--text-muted)', fontSize: 13 }}>← Modern ERP</Link>
      </div>
      <h1 style={{ fontSize: 20, fontWeight: 700, marginBottom: 4 }}>{name}</h1>
      <div style={{ color: 'var(--text-muted)', fontSize: 13, marginBottom: 16 }}>
        {schema.data?.columns?.length ?? 0} columns
      </div>

      <div style={{ display: 'flex', borderBottom: '1px solid var(--border)', marginBottom: 16 }}>
        {([['schema', 'Schema'], ['data', 'Data'], ['history', 'Load History']] as const).map(([t, label]) => (
          <button key={t} onClick={() => setTab(t)} style={tabStyle(tab === t)}>{label}</button>
        ))}
      </div>

      {tab === 'schema' && (
        schema.isLoading ? <div>Loading...</div> :
        <SchemaViewer columns={schema.data?.columns ?? []} mode="modern" />
      )}

      {tab === 'data' && (
        data.isLoading ? <div>Loading...</div> :
        <DataGrid
          columns={columns}
          data={data.data?.records ?? []}
          total={data.data?.total ?? 0}
          page={page}
          pageSize={PAGE_SIZE}
          onPageChange={setPage}
          dqMode={false}
        />
      )}

      {tab === 'history' && (
        history.isLoading ? <div>Loading...</div> :
        <div>
          {(history.data ?? []).length === 0 ? (
            <div style={{ color: 'var(--text-muted)' }}>No load history for this table.</div>
          ) : (
            <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: 13 }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border)' }}>
                  {['Batch ID', 'Mode', 'Status', 'Inserted', 'Updated', 'Rejected', 'Created At'].map(h => (
                    <th key={h} style={{ padding: '8px 10px', textAlign: 'left', fontWeight: 600, color: 'var(--text-muted)', fontSize: 12 }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(history.data ?? []).map((row: any) => (
                  <tr key={row.batch_id} style={{ borderBottom: '1px solid var(--border)' }}>
                    <td style={{ padding: '6px 10px', fontFamily: 'monospace', fontSize: 11 }}>{row.batch_id?.slice(0, 8)}…</td>
                    <td style={{ padding: '6px 10px' }}>{row.mode}</td>
                    <td style={{ padding: '6px 10px' }}>
                      <span style={{
                        padding: '2px 8px',
                        borderRadius: 4,
                        fontSize: 11,
                        fontWeight: 600,
                        color: '#fff',
                        background: STATUS_COLORS[row.status] ?? '#94a3b8',
                      }}>{row.status}</span>
                    </td>
                    <td style={{ padding: '6px 10px', color: 'var(--success)' }}>{row.inserted}</td>
                    <td style={{ padding: '6px 10px' }}>{row.updated}</td>
                    <td style={{ padding: '6px 10px', color: row.rejected > 0 ? 'var(--danger)' : undefined }}>{row.rejected}</td>
                    <td style={{ padding: '6px 10px', color: 'var(--text-muted)', fontSize: 12 }}>{row.created_at}</td>
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
