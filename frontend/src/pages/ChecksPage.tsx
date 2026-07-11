import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { consistencyApi, ConsistencyCheck } from '../api/consistency';
import { sourcesApi } from '../api/sources';

export default function ChecksPage() {
  const [selectedA, setSelectedA] = useState('');
  const [selectedB, setSelectedB] = useState('');
  const queryClient = useQueryClient();

  const { data: checksData, isLoading: checksLoading } = useQuery({
    queryKey: ['checks'],
    queryFn: () => consistencyApi.listChecks(),
  });

  const { data: sourcesData } = useQuery({
    queryKey: ['sources'],
    queryFn: () => sourcesApi.list(),
  });

  const runCheckMutation = useMutation({
    mutationFn: () =>
      consistencyApi.runCheck({ source_a_id: selectedA, source_b_id: selectedB }),
    onSuccess: () => {
      setSelectedA('');
      setSelectedB('');
      queryClient.invalidateQueries({ queryKey: ['checks'] });
    },
  });

  const getSeverityBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-900/50 text-green-300 border border-green-700';
      case 'running':
        return 'bg-blue-900/50 text-blue-300 border border-blue-700';
      case 'failed':
        return 'bg-red-900/50 text-red-300 border border-red-700';
      default:
        return 'bg-dark-700 text-dark-300 border border-dark-600';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Consistency Checks</h1>
        <p className="text-dark-400 mt-1">Run and monitor cross-system data consistency checks</p>
      </div>

      {/* Run Check Form */}
      <div className="bg-dark-800 rounded-xl p-6 border border-dark-700">
        <h2 className="text-lg font-semibold mb-4">Run New Check</h2>
        <div className="flex flex-wrap gap-4 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium text-dark-300 mb-1">Source A</label>
            <select
              value={selectedA}
              onChange={(e) => setSelectedA(e.target.value)}
              className="w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Select source...</option>
              {sourcesData?.items.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.source_type})
                </option>
              ))}
            </select>
          </div>
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium text-dark-300 mb-1">Source B</label>
            <select
              value={selectedB}
              onChange={(e) => setSelectedB(e.target.value)}
              className="w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Select source...</option>
              {sourcesData?.items.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.source_type})
                </option>
              ))}
            </select>
          </div>
          <button
            onClick={() => runCheckMutation.mutate()}
            disabled={!selectedA || !selectedB || runCheckMutation.isPending}
            className="bg-primary-600 hover:bg-primary-700 disabled:bg-primary-800/50 text-white px-6 py-2.5 rounded-lg transition-colors"
          >
            {runCheckMutation.isPending ? 'Running...' : 'Run Check'}
          </button>
        </div>
        {runCheckMutation.isError && (
          <p className="mt-2 text-red-400 text-sm">Failed to run check. Please try again.</p>
        )}
      </div>

      {/* Checks List */}
      <div className="bg-dark-800 rounded-xl border border-dark-700 overflow-hidden">
        <div className="p-4 border-b border-dark-700">
          <h2 className="text-lg font-semibold">Check History</h2>
        </div>

        {checksLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500" />
          </div>
        ) : !checksData || checksData.items.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-dark-400">No checks have been run yet</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-dark-700/50">
                <tr>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Status</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Source A</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Source B</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Summary</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-dark-400">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-700">
                {checksData.items.map((check: ConsistencyCheck) => (
                  <tr key={check.id} className="hover:bg-dark-700/30">
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityBadge(check.status)}`}>
                        {check.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm">{check.source_a_id.slice(0, 8)}...</td>
                    <td className="px-4 py-3 text-sm">{check.source_b_id.slice(0, 8)}...</td>
                    <td className="px-4 py-3 text-sm text-dark-300 max-w-xs truncate">
                      {check.summary || '-'}
                    </td>
                    <td className="px-4 py-3 text-sm text-dark-400">
                      {new Date(check.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}