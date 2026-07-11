import apiClient from './client';

export interface DashboardStats {
  total_sources: number;
  active_sources: number;
  total_checks: number;
  recent_checks: number;
  open_anomalies: number;
  resolved_anomalies: number;
  critical_anomalies: number;
  high_anomalies: number;
  medium_anomalies: number;
  low_anomalies: number;
}

export interface AnomalyTrendPoint {
  date: string;
  count: number;
  severity: string;
}

export interface DashboardResponse {
  stats: DashboardStats;
  anomaly_trend: AnomalyTrendPoint[];
  recent_activity: { id: string; action: string; entity_type: string; actor?: string; details?: unknown; created_at: string }[];
}

export const dashboardApi = {
  summary: async (): Promise<DashboardResponse> => {
    const res = await apiClient.get('/dashboard/summary');
    return res.data;
  },
};