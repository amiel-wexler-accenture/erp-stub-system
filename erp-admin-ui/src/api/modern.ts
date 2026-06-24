import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_MODERN_API_URL || 'http://localhost:8002',
  headers: {
    Authorization: `Bearer ${import.meta.env.VITE_MODERN_TOKEN || 'changeme-modern'}`,
  },
})

export const modernApi = {
  getSystemInfo: () => client.get('/system/info').then(r => r.data),
  getTables: () => client.get('/tables').then(r => r.data),
  getTableSchema: (name: string) => client.get(`/tables/${name}/schema`).then(r => r.data),
  getTableData: (name: string, params?: { limit?: number; offset?: number }) =>
    client.get(`/tables/${name}/data`, { params }).then(r => r.data),
  getTableRelationships: (name: string) => client.get(`/tables/${name}/relationships`).then(r => r.data),
  getTableCount: (name: string) => client.get(`/tables/${name}/count`).then(r => r.data),
  getProfiles: () => client.get('/config/profiles').then(r => r.data),
  validateRecords: (table: string, records: object[]) =>
    client.post(`/tables/${table}/validate`, { records }).then(r => r.data),
  loadRecords: (table: string, records: object[], mode = 'upsert', on_error = 'reject_record') =>
    client.post(`/tables/${table}/load`, { records, mode, on_error }).then(r => r.data),
  getLoadStatus: (table: string, batchId: string) =>
    client.get(`/tables/${table}/load-status/${batchId}`).then(r => r.data),
  getLoadHistory: (table: string) => client.get(`/tables/${table}/load-history`).then(r => r.data),
  resetAll: () => client.post('/admin/reset').then(r => r.data),
  resetTable: (table: string) => client.delete(`/tables/${table}/data`).then(r => r.data),
}
