import React from 'react';

interface StatsCardProps {
  title: string;
  value: number;
  subtitle: string;
  icon: React.ReactNode;
  color: 'blue' | 'green' | 'red' | 'purple' | 'orange';
}

const colorMap = {
  blue: 'from-blue-500/20 to-blue-600/5 border-blue-500/30',
  green: 'from-green-500/20 to-green-600/5 border-green-500/30',
  red: 'from-red-500/20 to-red-600/5 border-red-500/30',
  purple: 'from-purple-500/20 to-purple-600/5 border-purple-500/30',
  orange: 'from-orange-500/20 to-orange-600/5 border-orange-500/30',
};

const iconColorMap = {
  blue: 'text-blue-400',
  green: 'text-green-400',
  red: 'text-red-400',
  purple: 'text-purple-400',
  orange: 'text-orange-400',
};

export default function StatsCard({ title, value, subtitle, icon, color }: StatsCardProps) {
  return (
    <div
      className={`bg-gradient-to-br ${colorMap[color]} rounded-xl p-5 border`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-dark-300">{title}</p>
          <p className="text-3xl font-bold mt-1">{value}</p>
          <p className="text-xs text-dark-400 mt-1">{subtitle}</p>
        </div>
        <div className={`${iconColorMap[color]}`}>{icon}</div>
      </div>
    </div>
  );
}