interface Column {
  name: string
  type: string
  nullable: boolean
  description: string
  sample_values?: unknown[]
  validation_rules?: { rule_type: string; field: string; constraint: string; severity: string }[]
}

interface SchemaViewerProps {
  columns: Column[]
  mode?: 'legacy' | 'modern'
}

const ruleColors: Record<string, string> = {
  required: '#ef4444',
  pattern: '#f59e0b',
  iso_code: '#3b82f6',
  fk_integrity: '#8b5cf6',
  allowed_values: '#ec4899',
  string_hygiene: '#64748b',
  date_reasonableness: '#6366f1',
  cross_field: '#14b8a6',
}

export default function SchemaViewer({ columns, mode = 'legacy' }: SchemaViewerProps) {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: 13 }}>
        <thead>
          <tr style={{ borderBottom: '2px solid var(--border)' }}>
            {['Column', 'Type', 'Nullable', 'Description', ...(mode === 'modern' ? ['Validation Rules'] : [])].map(h => (
              <th key={h} style={{ padding: '8px 10px', textAlign: 'left', fontWeight: 600, color: 'var(--text-muted)', fontSize: 12 }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {columns.map(col => (
            <tr key={col.name} style={{ borderBottom: '1px solid var(--border)' }}>
              <td style={{ padding: '6px 10px', fontWeight: 600, fontFamily: 'monospace' }}>{col.name}</td>
              <td style={{ padding: '6px 10px', color: 'var(--text-muted)', fontFamily: 'monospace', fontSize: 12 }}>{col.type}</td>
              <td style={{ padding: '6px 10px', color: col.nullable ? 'var(--text-muted)' : 'var(--danger)' }}>
                {col.nullable ? 'Yes' : 'No'}
              </td>
              <td style={{ padding: '6px 10px', color: 'var(--text-muted)' }}>{col.description}</td>
              {mode === 'modern' && (
                <td style={{ padding: '6px 10px' }}>
                  <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                    {(col.validation_rules ?? []).map((rule, i) => (
                      <span key={i} style={{
                        padding: '2px 6px',
                        background: ruleColors[rule.rule_type] ?? '#94a3b8',
                        color: '#fff',
                        borderRadius: 4,
                        fontSize: 11,
                        fontWeight: 600,
                      }}>{rule.rule_type.toUpperCase()}</span>
                    ))}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
