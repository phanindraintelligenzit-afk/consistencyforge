import apiClient from './client';

export interface DataSource {
  id: string;
  name: string;
  source_type: string;
  connection_config: Record<string, unknown>;
  schema_snapshot?: Record<string, unknown>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface DataSourceCreate {
  name: string;
  source_type: string;
  connection_config: Record<string, unknown>;
}

export interface DataSourceListResponse {
  items: DataSource[];
  total: number;
}

export const sourcesApi = {
  list: async (skip = 0, limit = 100): Promise<DataSourceListResponse> => {
    const res = await apiClient.get('/sources/', { params: { skip, limit } });
    return res.data;
  },

  get: async (id: string): Promise<DataSource> => {
    const res = await apiClient.get(`/sources/${id}`);
    return res.data;
  },

  create: async (data: DataSourceCreate): Promise<DataSource> => {
    const res = await apiClient.post('/sources/', data);
    return res.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/sources/${id}`);
  },

  sync: async (id: string): Promise<DataSource> => {
    const res = await apiClient.post(`/sources/${id}/sync`);
    return res.data;
  },
};