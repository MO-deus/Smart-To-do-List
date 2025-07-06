import React, { useState, useRef, useEffect } from "react";

interface DeadlineSuggestionProps {
  deadline: string;
  onDeadlineChange: (deadline: string) => void;
  suggestedDeadline?: string;
  aiDeadlineSuggestions?: Array<{
    date: string;
    reason: string;
    confidence: number;
    urgency?: string;
  }>;
  contextData?: string;
  disabled?: boolean;
}

interface DeadlineSuggestion {
  label: string;
  value: string;
  description: string;
  confidence?: number;
  urgency?: string;
  isAI: boolean;
  isPrimary?: boolean;
}

const DeadlineSuggestion: React.FC<DeadlineSuggestionProps> = ({
  deadline,
  onDeadlineChange,
  suggestedDeadline,
  aiDeadlineSuggestions,
  contextData,
  disabled = false
}) => {
  const [showAIDropdown, setShowAIDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowAIDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Generate deadline suggestions based on context
  const getDeadlineSuggestions = (): DeadlineSuggestion[] => {
    const suggestions: DeadlineSuggestion[] = [];
    const today = new Date();
    
    // Add AI-suggested deadlines if available - these should be the primary options
    if (aiDeadlineSuggestions && aiDeadlineSuggestions.length > 0) {
      aiDeadlineSuggestions.forEach((aiSuggestion, index) => {
        suggestions.push({
          label: `AI Suggestion ${index + 1}`,
          value: aiSuggestion.date,
          description: aiSuggestion.reason,
          confidence: aiSuggestion.confidence,
          urgency: aiSuggestion.urgency || 'medium',
          isAI: true,
          isPrimary: true // Mark AI suggestions as primary
        });
      });
    }
    
    // Add legacy AI-suggested deadline if available
    if (suggestedDeadline) {
      suggestions.push({
        label: "AI Suggested",
        value: suggestedDeadline,
        description: "Based on context analysis",
        isAI: true
      });
    }

    // Generate context-based suggestions
    if (contextData) {
      const content = contextData.toLowerCase();
      
      // Tomorrow
      if (content.includes('tomorrow') || content.includes('next day')) {
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        suggestions.push({
          label: "Tomorrow",
          value: tomorrow.toISOString().split('T')[0],
          description: "Based on 'tomorrow' mention",
          isAI: false
        });
      }
      
      // This week
      if (content.includes('this week') || content.includes('end of week')) {
        const endOfWeek = new Date(today);
        endOfWeek.setDate(endOfWeek.getDate() + (7 - endOfWeek.getDay()));
        suggestions.push({
          label: "End of Week",
          value: endOfWeek.toISOString().split('T')[0],
          description: "Based on 'this week' mention",
          isAI: false
        });
      }
      
      // Next week
      if (content.includes('next week')) {
        const nextWeek = new Date(today);
        nextWeek.setDate(nextWeek.getDate() + 7);
        suggestions.push({
          label: "Next Week",
          value: nextWeek.toISOString().split('T')[0],
          description: "Based on 'next week' mention",
          isAI: false
        });
      }
      
      // Friday
      if (content.includes('friday')) {
        const friday = new Date(today);
        const daysUntilFriday = (5 - friday.getDay() + 7) % 7;
        friday.setDate(friday.getDate() + daysUntilFriday);
        suggestions.push({
          label: "Friday",
          value: friday.toISOString().split('T')[0],
          description: "Based on 'Friday' mention",
          isAI: false
        });
      }
      
      // End of month
      if (content.includes('end of month') || content.includes('month end')) {
        const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
        suggestions.push({
          label: "End of Month",
          value: endOfMonth.toISOString().split('T')[0],
          description: "Based on 'end of month' mention",
          isAI: false
        });
      }
    }

    // Add quick options
    const quickOptions = [
      { label: "Today", days: 0 },
      { label: "Tomorrow", days: 1 },
      { label: "In 3 days", days: 3 },
      { label: "In 1 week", days: 7 },
      { label: "In 2 weeks", days: 14 }
    ];

    quickOptions.forEach(option => {
      const date = new Date(today);
      date.setDate(date.getDate() + option.days);
      suggestions.push({
        label: option.label,
        value: date.toISOString().split('T')[0],
        description: "Quick selection",
        isAI: false
      });
    });

    // Remove duplicates and limit to 10 suggestions
    const uniqueSuggestions = suggestions.filter((suggestion, index, self) => 
      index === self.findIndex(s => s.value === suggestion.value)
    ).slice(0, 10);

    return uniqueSuggestions;
  };

  const deadlineSuggestions = getDeadlineSuggestions();
  const aiSuggestions = deadlineSuggestions.filter(s => s.isAI && s.isPrimary);

  const handleSuggestionSelect = (value: string, event?: React.MouseEvent) => {
    // Prevent form submission
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    
    onDeadlineChange(value);
    setShowAIDropdown(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getDaysUntilDeadline = (dateString: string) => {
    const deadline = new Date(dateString);
    const today = new Date();
    const diffTime = deadline.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Tomorrow";
    if (diffDays > 0) return `In ${diffDays} days`;
    if (diffDays < 0) return `${Math.abs(diffDays)} days ago`;
    return "Today";
  };

  const getUrgencyColor = (urgencyLevel: string) => {
    switch (urgencyLevel.toLowerCase()) {
      case 'high':
      case 'critical':
        return 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200';
      case 'medium':
        return 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200';
      case 'low':
        return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
      default:
        return 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200';
    }
  };

  return (
    <div className="space-y-3">
      {/* AI Deadline Suggestions Dropdown */}
      {aiSuggestions.length > 0 && (
        <div className="relative" ref={dropdownRef}>
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-200">
              AI-Suggested Deadlines
            </label>
          </div>
          
          <div className="relative">
            <button
              type="button"
              onClick={() => setShowAIDropdown(!showAIDropdown)}
              disabled={disabled}
              className="w-full flex items-center justify-between p-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-900 dark:text-white">
                  {deadline ? formatDate(deadline) : "Select AI deadline suggestion"}
                </span>
                {deadline && (
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {getDaysUntilDeadline(deadline)}
                  </span>
                )}
              </div>
              <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            {showAIDropdown && (
              <div className="absolute z-20 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg">
                <div className="p-2">
                  <div className="space-y-1 max-h-32 overflow-y-auto" style={{ maxHeight: '8rem' }}>
                    {aiSuggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        onClick={(e) => handleSuggestionSelect(suggestion.value, e)}
                        disabled={disabled}
                        className="w-full text-left p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-gray-900 dark:text-white">
                              {suggestion.label}
                            </span>
                            <span className={`text-xs px-2 py-1 rounded ${getUrgencyColor(suggestion.urgency || 'medium')}`}>
                              {suggestion.urgency || 'medium'}
                            </span>
                            <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-1.5 py-0.5 rounded">
                              AI
                            </span>
                          </div>
                          <div className="text-right">
                            <div className="text-sm font-medium text-gray-900 dark:text-white">
                              {formatDate(suggestion.value)}
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              {getDaysUntilDeadline(suggestion.value)}
                            </div>
                          </div>
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-300 line-clamp-1">
                          {suggestion.description}
                        </div>
                        {suggestion.confidence && (
                          <div className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                            Confidence: {Math.round(suggestion.confidence * 100)}%
                          </div>
                        )}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Deadline Input */}
      <div className="flex gap-2">
        <input
          type="date"
          value={deadline}
          onChange={(e) => onDeadlineChange(e.target.value)}
          className="flex-1 border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          disabled={disabled}
        />
        

        
        <button
          type="button"
          onClick={() => onDeadlineChange("")}
          disabled={disabled || !deadline}
          className="px-3 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 disabled:opacity-50"
        >
          Clear
        </button>
      </div>



      {/* Current Deadline Display */}
      {deadline && (
        <div className="p-3 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800 rounded-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <div>
                <div className="text-sm font-medium text-indigo-800 dark:text-indigo-200">
                  Selected Deadline: {formatDate(deadline)}
                </div>
                <div className="text-xs text-indigo-600 dark:text-indigo-300">
                  {getDaysUntilDeadline(deadline)}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DeadlineSuggestion; 