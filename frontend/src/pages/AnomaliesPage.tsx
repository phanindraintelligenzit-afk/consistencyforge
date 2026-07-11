import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { consistencyApi, Anomaly } from '../api/consistency';
import AnomalyRow from '../components/AnomalyRow';

export default function AnomaliesPage() {
  const [severityFilter, setSeverityFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['anomalies', severityFilter, statusFilter],
    queryFn: () =>
      consistencyApi.listAnomalies(0, 100, severityFilter || undefined, statusFilter || undefined),
  });

  const resolveMutation = useMutation({
    mutationFn: ({
      id,
      resolution,
      status,
    }: {
      id: string;
      resolution: string;
      status: 'resolved' | 'dismissed';
    }) => consistencyApi.resolveAnomaly(id, { resolution, status }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['anomalies'] }),
  });

  const handleResolve = (id: string, resolution: string, status: 'resolved' | 'dismissed') => {
    resolveMutation.mutate({ id, resolution, status });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Anomalies</h1>
        <p className="text-dark-400 mt-1">Review and resolve data consistency anomalies</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4">
        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="bg-dark-700 border border-dark-600 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="bg-dark-700 border border-dark-600 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="">All Statuses</option>
          <option value="open">Open</option>
          <option value="investigating">Investigating</option>
          <option value="resolved">Resolved</option>
          <option value="dismissed">Dismissed</option>
        </select>
      </div>

      {/* Anomalies Table */}
      <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden">
        {isLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500" />
          </div>
        ) : !data || data.items.length === 0 ? (
          <div className="text-center py-12">
            <svg className="w-12 h-12 mx-auto text-dark-500 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-dark-400">No anomalies found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-dark-700/50">
                <tr>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Field</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Severity</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Status</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Source A Value</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Source B Value</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Date</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-700">
                {data.items.map((anomaly: Anomaly) => (
                  <AnomalyRow
                    key={anomaly.id}
                    anomaly={anomaly}
                    onResolve={handleResolve}
                  />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}