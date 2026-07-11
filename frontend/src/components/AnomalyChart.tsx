import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { AnomalyTrendPoint } from '../api/dashboard';

interface AnomalyChartProps {
  data: AnomalyTrendPoint[];
}

export default function AnomalyChart({ data }: AnomalyChartProps) {
  // Group data by date
  const groupedMap = new Map<string, Record<string, number>>();
  data.forEach((point) => {
    if (!groupedMap.has(point.date)) {
      groupedMap.set(point.date, { date: point.date });
    }
    const entry = groupedMap.get(point.date)!;
    entry[point.severity] = (entry[point.severity] || 0) + point.count;
  });

  const chartData = Array.from(groupedMap.values());

  const severityColors: Record<string, string> = {
    low: '#3b82f6',
    medium: '#eab308',
    high: '#f97316',
    critical: '#ef4444',
  };

  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={chartData.length > 0 ? chartData : [{ date: 'No data', low: 0, medium: 0, high: 0, critical: 0 }]}>
        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
        <XAxis dataKey="date" stroke="#64748b" fontSize={12} />
        <YAxis stroke="#64748b" fontSize={12} />
        <Tooltip
          contentStyle={{
            backgroundColor: '#1e293b',
            border: '1px solid #334155',
            borderRadius: '8px',
            color: '#f1f5f9',
          }}
        />
        <Legend />
        {Object.entries(severityColors).map(([severity, color]) => (
          <Bar
            key={severity}
            dataKey={severity}
            stackId="a"
            fill={color}
            name={severity.charAt(0).toUpperCase() + severity.slice(1)}
          />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}