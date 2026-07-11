import apiClient from './client';

export interface ConsistencyCheck {
  id: string;
  source_a_id: string;
  source_b_id: string;
  field_mapping_id?: string;
  status: string;
  results?: Record<string, unknown>;
  summary?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Anomaly {
  id: string;
  check_id: string;
  source_a_id: string;
  source_b_id: string;
  field_name: string;
  severity: string;
  status: string;
  source_a_value?: unknown;
  source_b_value?: unknown;
  expected_value?: unknown;
  actual_value?: unknown;
  root_cause?: string;
  resolution?: string;
  created_at: string;
  updated_at: string;
}

export interface RunCheckRequest {
  source_a_id: string;
  source_b_id: string;
  field_mapping_id?: string;
}

export interface ResolveAnomalyRequest {
  resolution: string;
  status: 'resolved' | 'dismissed';
}

export const consistencyApi = {
  runCheck: async (data: RunCheckRequest): Promise<ConsistencyCheck> => {
    const res = await apiClient.post('/consistency/checks', data);
    return res.data;
  },

  listChecks: async (skip = 0, limit = 50): Promise<{ items: ConsistencyCheck[]; total: number }> => {
    const res = await apiClient.get('/consistency/checks', { params: { skip, limit } });
    return res.data;
  },

  getCheck: async (id: string): Promise<ConsistencyCheck> => {
    const res = await apiClient.get(`/consistency/checks/${id}`);
    return res.data;
  },

  listAnomalies: async (
    skip = 0,
    limit = 50,
    severity?: string,
    status?: string
  ): Promise<{ items: Anomaly[]; total: number }> => {
    const res = await apiClient.get('/consistency/anomalies', {
      params: { skip, limit, severity, status },
    });
    return res.data;
  },

  resolveAnomaly: async (id: string, data: ResolveAnomalyRequest): Promise<Anomaly> => {
    const res = await apiClient.put(`/consistency/anomalies/${id}/resolve`, data);
    return res.data;
  },
};