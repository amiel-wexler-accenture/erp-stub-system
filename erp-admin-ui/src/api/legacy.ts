import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_LEGACY_API_URL || 'http://localhost:8001',
  headers: {
    Authorization: `Bearer ${import.meta.env.VITE_LEGACY_TOKEN || 'changeme-legacy'}`,
  },
})

export const legacyApi = {
  getSystemInfo: () => client.get('/system/info').then(r => r.data),
  getTables: () => client.get('/tables').then(r => r.data),
  getTableSchema: (name: string) => client.get(`/tables/${name}/schema`).then(r => r.data),
  getTableData: (name: string, params?: { limit?: number; offset?: number; since?: string }) =>
    client.get(`/tables/${name}/data`, { params }).then(r => r.data),
  getTableRelationships: (name: string) => client.get(`/tables/${name}/relationships`).then(r => r.data),
  getTableCount: (name: string) => client.get(`/tables/${name}/count`).then(r => r.data),
  getProfiles: () => client.get('/config/profiles').then(r => r.data),
  switchProfile: (id: string) => client.post(`/config/profiles/${id}/activate`).then(r => r.data),
}
