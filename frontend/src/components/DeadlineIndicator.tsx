/**
 * DeadlineIndicator component for displaying deadline information.
 */

import React from 'react';

interface DeadlineIndicatorProps {
  deadline: string;
  isOverdue: boolean;
  isDueSoon: boolean;
  daysUntilDeadline: number | null;
  compact?: boolean;
  className?: string;
}

export const DeadlineIndicator: React.FC<DeadlineIndicatorProps> = ({
  deadline,
  isOverdue,
  isDueSoon,
  daysUntilDeadline,
  compact = false,
  className = '',
}) => {
  const getDeadlineConfig = () => {
    if (isOverdue) {
      return {
        color: 'text-red-600 dark:text-red-400',
        bgColor: 'bg-red-100 dark:bg-red-900/30',
        borderColor: 'border-red-300 dark:border-red-600',
        icon: '🚨',
        urgency: 'Overdue',
      };
    }
    
    if (isDueSoon) {
      return {
        color: 'text-yellow-600 dark:text-yellow-400',
        bgColor: 'bg-yellow-100 dark:bg-yellow-900/30',
        borderColor: 'border-yellow-300 dark:border-yellow-600',
        icon: '⚠️',
        urgency: 'Due Soon',
      };
    }
    
    return {
      color: 'text-gray-600 dark:text-gray-400',
      bgColor: 'bg-gray-100 dark:bg-gray-700',
      borderColor: 'border-gray-300 dark:border-gray-600',
      icon: '📅',
      urgency: 'On Track',
    };
  };

  const formatDeadline = (deadline: string) => {
    const date = new Date(deadline);
    const now = new Date();
    const diffTime = date.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Tomorrow';
    } else if (diffDays === -1) {
      return 'Yesterday';
    } else if (diffDays > 0) {
      return `In ${diffDays} days`;
    } else {
      return `${Math.abs(diffDays)} days ago`;
    }
  };

  const config = getDeadlineConfig();

  if (compact) {
    return (
      <span
        className={`
          inline-flex items-center gap-1
          ${config.color}
          ${className}
        `}
        title={`Deadline: ${new Date(deadline).toLocaleDateString()} (${config.urgency})`}
      >
        <span>{config.icon}</span>
        <span className="text-xs">{formatDeadline(deadline)}</span>
      </span>
    );
  }

  return (
    <div
      className={`
        inline-flex items-center gap-2 px-2 py-1 rounded-full border
        ${config.bgColor}
        ${config.borderColor}
        ${className}
      `}
      title={`Deadline: ${new Date(deadline).toLocaleDateString()} (${config.urgency})`}
    >
      <span>{config.icon}</span>
      <div className="flex flex-col">
        <span className={`text-xs font-medium ${config.color}`}>
          {formatDeadline(deadline)}
        </span>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {new Date(deadline).toLocaleDateString()}
        </span>
      </div>
    </div>
  );
};

export default DeadlineIndicator; 