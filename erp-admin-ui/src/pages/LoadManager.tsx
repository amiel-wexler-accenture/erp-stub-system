import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { modernApi } from '../api/modern'

const TRACKED_TABLES = ['BusinessPartner', 'BPRole', 'BPBankAccount', 'BPAddress', 'BPCompanyCode', 'BPPurchasingOrg', 'Product', 'ProductPlant', 'ProductValuation', 'PurchaseOrder', 'PurchaseOrderItem']

const STATUS_COLORS: Record<string, { bg: string; text: string }> = {
  completed: { bg: '#f0fdf4', text: '#16a34a' },
  partial: { bg: '#fffbeb', text: '#b45309' },
  failed: { bg: '#fef2f2', text: '#dc2626' },
}

function useAllLoadHistory() {
  return useQuery({
    queryKey: ['all-load-history'],
    queryFn: async () => {
      const results = await Promise.allSettled(
        TRACKED_TABLES.map(t => modernApi.getLoadHistory(t).then(rows => rows.map((r: any) => ({ ...r, table_name: r.table_name || t }))))
      )
      return results
        .filter((r): r is PromiseFulfilledResult<any[]> => r.status === 'fulfilled')
        .flatMap(r => r.value)
        .sort((a, b) => (b.created_at ?? '').localeCompare(a.created_at ?? ''))
    },
    refetchInterval: 30_000,
  })
}

export default function LoadManager() {
  const history = useAllLoadHistory()
  const [expanded, setExpanded] = useState<string | null>(null)

  const batches = history.data ?? []
  const counts = {
    completed: batches.filter(b => b.status === 'completed').length,
    partial: batches.filter(b => b.status === 'partial').length,
    failed: batches.filter(b => b.status === 'failed').length,
  }

  return (
    <div style={{ padding: 24 }}>
      <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 8 }}>Load Manager</h1>
      <p style={{ color: 'var(--text-muted)', marginBottom: 20, fontSize: 13 }}>
        All load batch operations across modern ERP tables.
      </p>

      {/* Summary row */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
        {[
          { label: 'Completed', count: counts.completed, color: '#16a34a', bg: '#f0fdf4' },
          { label: 'Partial', count: counts.partial, color: '#b45309', bg: '#fffbeb' },
          { label: 'Failed', count: counts.failed, color: '#dc2626', bg: '#fef2f2' },
          { label: 'Total Batches', count: batches.length, color: 'var(--text)', bg: 'var(--surface)' },
        ].map(({ label, count, color, bg }) => (
          <div key={label} style={{
            flex: 1, background: bg, border: '1px solid var(--border)',
            borderRadius: 8, padding: '12px 16px',
          }}>
            <div style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 4 }}>{label}</div>
            <div style={{ fontSize: 28, fontWeight: 800, color }}>{count}</div>
          </div>
        ))}
      </div>

      {history.isLoading && <div style={{ color: 'var(--text-muted)' }}>Loading batch history...</div>}

      {batches.length === 0 && !history.isLoading && (
        <div style={{ color: 'var(--text-muted)', padding: 24, textAlign: 'center', background: 'var(--surface)', borderRadius: 8, border: '1px solid var(--border)' }}>
          No load batches yet. Use the validate/load endpoints to push data into the modern ERP.
        </div>
      )}

      {/* Batch list */}
      {batches.length > 0 && (
        <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: 13 }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--border)' }}>
              {['Table', 'Batch ID', 'Mode', 'Status', 'Inserted', 'Updated', 'Rejected', 'Created At', ''].map(h => (
                <th key={h} style={{ padding: '8px 10px', textAlign: 'left', fontWeight: 600, color: 'var(--text-muted)', fontSize: 12 }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {batches.map((row: any) => {
              const isExpanded = expanded === row.batch_id
              const sc = STATUS_COLORS[row.status] ?? { bg: '#f1f5f9', text: '#64748b' }
              const hasErrors = row.rejected > 0 || row.error_details

              return (
                <>
                  <tr key={row.batch_id} style={{ borderBottom: '1px solid var(--border)', background: isExpanded ? '#f8fafc' : undefined }}>
                    <td style={{ padding: '6px 10px', fontWeight: 600 }}>{row.table_name}</td>
                    <td style={{ padding: '6px 10px', fontFamily: 'monospace', fontSize: 11 }}>{(row.batch_id ?? '').slice(0, 8)}…</td>
                    <td style={{ padding: '6px 10px' }}>{row.mode}</td>
                    <td style={{ padding: '6px 10px' }}>
                      <span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 11, fontWeight: 600, background: sc.bg, color: sc.text, border: `1px solid ${sc.text}33` }}>
                        {row.status}
                      </span>
                    </td>
                    <td style={{ padding: '6px 10px', color: 'var(--success)' }}>{row.inserted}</td>
                    <td style={{ padding: '6px 10px' }}>{row.updated}</td>
                    <td style={{ padding: '6px 10px', color: row.rejected > 0 ? 'var(--danger)' : undefined }}>{row.rejected}</td>
                    <td style={{ padding: '6px 10px', color: 'var(--text-muted)', fontSize: 12 }}>{row.created_at?.slice(0, 19)}</td>
                    <td style={{ padding: '6px 10px' }}>
                      {hasErrors && (
                        <button
                          onClick={() => setExpanded(isExpanded ? null : row.batch_id)}
                          style={{ background: 'var(--border)', color: 'var(--text)', fontSize: 11, padding: '2px 8px' }}
                        >
                          {isExpanded ? 'Hide' : 'Errors'}
                        </button>
                      )}
                    </td>
                  </tr>
                  {isExpanded && (
                    <tr key={`${row.batch_id}-detail`}>
                      <td colSpan={9} style={{ padding: '8px 16px', background: '#fef2f2', fontSize: 12 }}>
                        <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', color: '#dc2626', margin: 0 }}>
                          {typeof row.error_details === 'string' ? row.error_details : JSON.stringify(row.error_details, null, 2)}
                        </pre>
                      </td>
                    </tr>
                  )}
                </>
              )
            })}
          </tbody>
        </table>
      )}
    </div>
  )
}
