import React from "react";

const priorityMap = {
  1: { label: "High", color: "bg-red-500" },
  2: { label: "Medium", color: "bg-yellow-500" },
  3: { label: "Low", color: "bg-green-500" },
};

const PriorityIndicator: React.FC<{ priority: number }> = ({ priority }) => {
  const { label, color } = priorityMap[priority as 1 | 2 | 3] || priorityMap[2];
  return (
    <div className="flex items-center gap-1">
      <span className={`w-3 h-3 rounded-full ${color} inline-block`} />
      <span className="text-xs text-gray-500 dark:text-gray-300">{label}</span>
    </div>
  );
};

export default PriorityIndicator; 