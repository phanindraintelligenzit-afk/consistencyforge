import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { sourcesApi, DataSource } from '../api/sources';
import SourceCard from '../components/SourceCard';
import AddSourceModal from '../components/AddSourceModal';

export default function SourcesPage() {
  const [showAddModal, setShowAddModal] = useState(false);
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['sources'],
    queryFn: () => sourcesApi.list(),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => sourcesApi.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['sources'] }),
  });

  const syncMutation = useMutation({
    mutationFn: (id: string) => sourcesApi.sync(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['sources'] }),
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Data Sources</h1>
          <p className="text-dark-400 mt-1">Manage your connected data systems</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Source
        </button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500" />
        </div>
      ) : !data || data.items.length === 0 ? (
        <div className="text-center py-12 bg-dark-800 rounded-xl border border-dark-700">
          <svg className="w-12 h-12 mx-auto text-dark-500 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
          </svg>
          <p className="text-dark-400">No data sources yet</p>
          <button
            onClick={() => setShowAddModal(true)}
            className="mt-3 text-primary-400 hover:text-primary-300 text-sm"
          >
            Add your first source
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.items.map((source: DataSource) => (
            <SourceCard
              key={source.id}
              source={source}
              onDelete={() => deleteMutation.mutate(source.id)}
              onSync={() => syncMutation.mutate(source.id)}
            />
          ))}
        </div>
      )}

      {showAddModal && (
        <AddSourceModal
          onClose={() => setShowAddModal(false)}
          onSuccess={() => {
            setShowAddModal(false);
            queryClient.invalidateQueries({ queryKey: ['sources'] });
          }}
        />
      )}
    </div>
  );
}