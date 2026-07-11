import React from 'react';
import { DataSource } from '../api/sources';

interface SourceCardProps {
  source: DataSource;
  onDelete: () => void;
  onSync: () => void;
}

const typeIcons: Record<string, string> = {
  postgresql: '🐘',
  mysql: '🐬',
  mongodb: '🍃',
  csv: '📄',
  api: '🔌',
};

export default function SourceCard({ source, onDelete, onSync }: SourceCardProps) {
  return (
    <div className="bg-dark-800 rounded-xl p-5 border border-dark-700 hover:border-dark-600 transition-colors">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{typeIcons[source.source_type] || '🗄️'}</span>
          <div>
            <h3 className="font-semibold">{source.name}</h3>
            <span className="text-xs bg-dark-700 text-dark-300 px-2 py-0.5 rounded-full">
              {source.source_type}
            </span>
          </div>
        </div>
        <span
          className={`w-2.5 h-2.5 rounded-full ${
            source.is_active ? 'bg-green-500' : 'bg-red-500'
          }`}
        />
      </div>

      <div className="text-xs text-dark-400 space-y-1 mb-4">
        <p>ID: {source.id.slice(0, 12)}...</p>
        <p>Created: {new Date(source.created_at).toLocaleDateString()}</p>
      </div>

      <div className="flex gap-2">
        <button
          onClick={onSync}
          className="flex-1 bg-dark-700 hover:bg-dark-600 text-sm text-white py-1.5 rounded-lg transition-colors"
        >
          Sync Schema
        </button>
        <button
          onClick={onDelete}
          className="px-3 bg-red-900/30 hover:bg-red-900/50 text-red-400 py-1.5 rounded-lg transition-colors"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  );
}