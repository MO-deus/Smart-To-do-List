import React from "react";

interface TaskPriorityIndicatorProps {
  priority: number;
  onPriorityChange: (priority: number) => void;
  suggestedPriority?: string;
  disabled?: boolean;
}

const TaskPriorityIndicator: React.FC<TaskPriorityIndicatorProps> = ({
  priority,
  onPriorityChange,
  suggestedPriority,
  disabled = false
}) => {
  const priorityOptions = [
    { value: 1, label: "High", color: "red", bgColor: "bg-red-100", textColor: "text-red-800", borderColor: "border-red-300" },
    { value: 2, label: "Medium", color: "yellow", bgColor: "bg-yellow-100", textColor: "text-yellow-800", borderColor: "border-yellow-300" },
    { value: 3, label: "Low", color: "green", bgColor: "bg-green-100", textColor: "text-green-800", borderColor: "border-green-300" }
  ];

  const getPriorityOption = (priorityValue: number) => {
    return priorityOptions.find(option => option.value === priorityValue) || priorityOptions[1];
  };

  const currentPriority = getPriorityOption(priority);

  const getPriorityIcon = (priorityValue: number) => {
    switch (priorityValue) {
      case 1:
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      case 2:
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      case 3:
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        );
      default:
        return null;
    }
  };

  const getSuggestedPriorityValue = () => {
    if (!suggestedPriority) return null;
    const priorityMap: { [key: string]: number } = {
      'high': 1,
      'medium': 2,
      'low': 3
    };
    return priorityMap[suggestedPriority.toLowerCase()];
  };

  const suggestedPriorityValue = getSuggestedPriorityValue();
  const isAISuggestion = suggestedPriorityValue && suggestedPriorityValue !== priority;

  return (
    <div className="space-y-3">
      {/* Priority Selection */}
      <div className="flex gap-2">
        {priorityOptions.map((option) => (
          <button
            key={option.value}
            type="button"
            onClick={() => onPriorityChange(option.value)}
            disabled={disabled}
            className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg border-2 transition-all ${
              priority === option.value
                ? `${option.bgColor} ${option.textColor} ${option.borderColor} border-2`
                : 'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            {getPriorityIcon(option.value)}
            <span className="font-medium">{option.label}</span>
          </button>
        ))}
      </div>

      {/* AI Suggestion */}
      {isAISuggestion && suggestedPriority && (
        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span className="text-sm text-blue-800 dark:text-blue-200">
                AI suggests <span className="font-medium">{suggestedPriority}</span> priority
              </span>
            </div>
            <button
              type="button"
              onClick={() => onPriorityChange(suggestedPriorityValue!)}
              disabled={disabled}
              className="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700 disabled:opacity-50"
            >
              Apply
            </button>
          </div>
        </div>
      )}

      {/* Current Priority Display */}
      <div className={`p-3 ${currentPriority.bgColor} border ${currentPriority.borderColor} rounded-lg`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {getPriorityIcon(priority)}
            <span className={`font-medium ${currentPriority.textColor}`}>
              Current Priority: {currentPriority.label}
            </span>
          </div>
          <div className={`w-3 h-3 rounded-full bg-${currentPriority.color}-500`}></div>
        </div>
      </div>

      {/* Priority Explanation */}
      <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
        <p><strong>High:</strong> Urgent tasks requiring immediate attention</p>
        <p><strong>Medium:</strong> Important tasks with moderate urgency</p>
        <p><strong>Low:</strong> Tasks that can be completed when convenient</p>
      </div>
    </div>
  );
};

export default TaskPriorityIndicator; 