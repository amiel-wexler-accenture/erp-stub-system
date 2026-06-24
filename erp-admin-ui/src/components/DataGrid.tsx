import { useReactTable, getCoreRowModel, flexRender, ColumnDef } from '@tanstack/react-table'
import { useMemo } from 'react'

interface DataGridProps {
  columns: { key: string; header: string }[]
  data: Record<string, unknown>[]
  total: number
  page: number
  pageSize: number
  onPageChange: (page: number) => void
  dqMode?: boolean
}

function hasTrailingSpace(val: unknown): boolean {
  return typeof val === 'string' && val !== val.trimEnd()
}

function isNullLike(val: unknown): boolean {
  return val === null || val === undefined || val === '' || val === 'N/A'
}

export default function DataGrid({ columns, data, total, page, pageSize, onPageChange, dqMode }: DataGridProps) {
  const tableColumns = useMemo<ColumnDef<Record<string, unknown>>[]>(
    () =>
      columns.map(col => ({
        id: col.key,
        accessorKey: col.key,
        header: col.header,
        cell: ({ getValue }) => {
          const val = getValue()
          if (!dqMode) return <span>{String(val ?? '')}</span>

          if (isNullLike(val)) {
            return (
              <span style={{
                display: 'inline-block',
                padding: '1px 5px',
                background: '#f1f5f9',
                color: '#94a3b8',
                borderRadius: 3,
                fontSize: 11,
                fontWeight: 600,
              }}>NULL</span>
            )
          }

          if (hasTrailingSpace(val)) {
            return (
              <span style={{ position: 'relative', display: 'inline-block' }}>
                <span style={{
                  position: 'absolute',
                  top: -4,
                  right: -6,
                  fontSize: 9,
                  color: '#f59e0b',
                  fontWeight: 700,
                }}>⚠</span>
                <span style={{ background: '#fffbeb' }}>{String(val)}</span>
              </span>
            )
          }

          return <span>{String(val)}</span>
        },
      })),
    [columns, dqMode]
  )

  const table = useReactTable({
    data,
    columns: tableColumns,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    rowCount: total,
  })

  const totalPages = Math.ceil(total / pageSize)

  return (
    <div>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: 13 }}>
          <thead>
            {table.getHeaderGroups().map(hg => (
              <tr key={hg.id} style={{ borderBottom: '2px solid var(--border)' }}>
                {hg.headers.map(h => (
                  <th key={h.id} style={{
                    padding: '8px 10px',
                    textAlign: 'left',
                    fontWeight: 600,
                    color: 'var(--text-muted)',
                    fontSize: 12,
                    whiteSpace: 'nowrap',
                  }}>
                    {flexRender(h.column.columnDef.header, h.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map(row => {
              const isDeleted = dqMode && row.original['LOEVM'] === 'X'
              return (
                <tr key={row.id} style={{
                  background: isDeleted ? '#fef2f2' : undefined,
                  borderBottom: '1px solid var(--border)',
                }}>
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} style={{ padding: '6px 10px', maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 12, fontSize: 13, color: 'var(--text-muted)' }}>
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={page === 0}
          style={{ background: 'var(--border)', color: 'var(--text)' }}
        >← Prev</button>
        <span>Page {page + 1} of {totalPages} ({total.toLocaleString()} rows)</span>
        <button
          onClick={() => onPageChange(page + 1)}
          disabled={page >= totalPages - 1}
          style={{ background: 'var(--border)', color: 'var(--text)' }}
        >Next →</button>
      </div>
    </div>
  )
}
