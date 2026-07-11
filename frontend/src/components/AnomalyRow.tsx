import React, { useState } from 'react';
import { Anomaly } from '../api/consistency';

interface AnomalyRowProps {
  anomaly: Anomaly;
  onResolve: (id: string, resolution: string, status: 'resolved' | 'dismissed') => void;
}

const severityColors: Record<string, string> = {
  critical: 'bg-red-900/50 text-red-300 border-red-700',
  high: 'bg-orange-900/50 text-orange-300 border-orange-700',
  medium: 'bg-yellow-900/50 text-yellow-300 border-yellow-700',
  low: 'bg-blue-900/50 text-blue-300 border-blue-700',
};

const statusColors: Record<string, string> = {
  open: 'text-red-400',
  investigating: 'text-yellow-400',
  resolved: 'text-green-400',
  dismissed: 'text-dark-400',
};

export default function AnomalyRow({ anomaly, onResolve }: AnomalyRowProps) {
  const [showResolve, setShowResolve] = useState(false);
  const [resolution, setResolution] = useState('');

  const handleResolve = () => {
    if (resolution.trim()) {
      onResolve(anomaly.id, resolution, 'resolved');
      setShowResolve(false);
      setResolution('');
    }
  };

  const handleDismiss = () => {
    onResolve(anomaly.id, 'Dismissed without action', 'dismissed');
  };

  const formatValue = (val: unknown): string => {
    if (val === null || val === undefined) return '—';
    if (typeof val === 'object') return JSON.stringify(val);
    return String(val);
  };

  return (
    <tr className="hover:bg-dark-700/30">
      <td className="px-4 py-3 text-sm font-medium">{anomaly.field_name}</td>
      <td className="px-4 py-3">
        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${severityColors[anomaly.severity] || severityColors.low}`}>
          {anomaly.severity}
        </span>
      </td>
      <td className="px-4 py-3">
        <span className={`text-sm font-medium ${statusColors[anomaly.status] || 'text-dark-400'}`}>
          {anomaly.status}
        </span>
      </td>
      <td className="px-4 py-3 text-sm text-dark-300 max-w-[150px] truncate" title={formatValue(anomaly.source_a_value)}>
        {formatValue(anomaly.source_a_value)}
      </td>
      <td className="px-4 py-3 text-sm text-dark-300 max-w-[150px] truncate" title={formatValue(anomaly.source_b_value)}>
        {formatValue(anomaly.source_b_value)}
      </td>
      <td className="px-4 py-3 text-sm text-dark-400">
        {new Date(anomaly.created_at).toLocaleDateString()}
      </td>
      <td className="px-4 py-3">
        {anomaly.status === 'open' && (
          <div className="flex gap-1">
            <button
              onClick={() => setShowResolve(!showResolve)}
              className="text-xs bg-green-900/30 hover:bg-green-900/50 text-green-400 px-2 py-1 rounded transition-colors"
            >
              Resolve
            </button>
            <button
              onClick={handleDismiss}
              className="text-xs bg-dark-700 hover:bg-dark-600 text-dark-300 px-2 py-1 rounded transition-colors"
            >
              Dismiss
            </button>
          </div>
        )}
        {showResolve && (
          <div className="mt-2 flex gap-1">
            <input
              type="text"
              value={resolution}
              onChange={(e) => setResolution(e.target.value)}
              placeholder="Resolution note..."
              className="bg-dark-700 border border-dark-600 rounded px-2 py-1 text-xs text-white w-32 focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
            <button
              onClick={handleResolve}
              disabled={!resolution.trim()}
              className="text-xs bg-green-900/50 hover:bg-green-900/70 text-green-300 px-2 py-1 rounded disabled:opacity-50"
            >
              Save
            </button>
          </div>
        )}
      </td>
    </tr>
  );
}