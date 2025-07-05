import React from "react";

interface AITaskSuggestionsProps {
  analysisResult: any;
  onRegenerate: () => void;
  isRegenerating: boolean;
}

const AITaskSuggestions: React.FC<AITaskSuggestionsProps> = ({
  analysisResult,
  onRegenerate,
  isRegenerating
}) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          AI Analysis Results
        </h3>
        <button
          onClick={onRegenerate}
          disabled={isRegenerating}
          className="text-sm bg-purple-600 text-white px-3 py-1 rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center gap-1"
        >
          {isRegenerating ? (
            <>
              <div className="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin"></div>
              Regenerating...
            </>
          ) : (
            <>
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Regenerate
            </>
          )}
        </button>
      </div>

      <div className="space-y-4">
        {/* Urgency Assessment */}
        {analysisResult.urgency_level && (
          <div className="border border-orange-200 dark:border-orange-800 rounded-lg p-3 bg-orange-50 dark:bg-orange-900/20">
            <h4 className="font-medium text-orange-800 dark:text-orange-200 mb-1">
              Urgency Assessment
            </h4>
            <p className="text-sm text-orange-700 dark:text-orange-300">
              <span className="font-medium">{analysisResult.urgency_level}</span> priority based on context analysis
            </p>
          </div>
        )}

        {/* Key Insights */}
        {analysisResult.insights && analysisResult.insights.length > 0 && (
          <div className="border border-blue-200 dark:border-blue-800 rounded-lg p-3 bg-blue-50 dark:bg-blue-900/20">
            <h4 className="font-medium text-blue-800 dark:text-blue-200 mb-2">
              Key Insights
            </h4>
            <ul className="space-y-1">
              {analysisResult.insights.map((insight: string, index: number) => (
                <li key={index} className="text-sm text-blue-700 dark:text-blue-300 flex items-start gap-2">
                  <span className="text-blue-500 mt-1">•</span>
                  {insight}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Suggested Actions */}
        {analysisResult.suggested_actions && analysisResult.suggested_actions.length > 0 && (
          <div className="border border-purple-200 dark:border-purple-800 rounded-lg p-3 bg-purple-50 dark:bg-purple-900/20">
            <h4 className="font-medium text-purple-800 dark:text-purple-200 mb-2">
              Suggested Actions
            </h4>
            <ul className="space-y-1">
              {analysisResult.suggested_actions.map((action: string, index: number) => (
                <li key={index} className="text-sm text-purple-700 dark:text-purple-300 flex items-start gap-2">
                  <span className="text-purple-500 mt-1">•</span>
                  {action}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Task Enhancement Suggestions */}
        {analysisResult.enhanced_task && (
          <div className="border border-green-200 dark:border-green-800 rounded-lg p-3 bg-green-50 dark:bg-green-900/20">
            <h4 className="font-medium text-green-800 dark:text-green-200 mb-2">
              Enhanced Task Suggestions
            </h4>
            <div className="space-y-2 text-sm text-green-700 dark:text-green-300">
              {analysisResult.enhanced_task.title && (
                <div>
                  <strong>Enhanced Title:</strong> {analysisResult.enhanced_task.title}
                </div>
              )}
              {analysisResult.enhanced_task.description && (
                <div>
                  <strong>Enhanced Description:</strong> {analysisResult.enhanced_task.description}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Priority Suggestion */}
        {analysisResult.suggested_priority && (
          <div className="border border-yellow-200 dark:border-yellow-800 rounded-lg p-3 bg-yellow-50 dark:bg-yellow-900/20">
            <h4 className="font-medium text-yellow-800 dark:text-yellow-200 mb-1">
              Priority Suggestion
            </h4>
            <p className="text-sm text-yellow-700 dark:text-yellow-300">
              AI suggests <span className="font-medium">{analysisResult.suggested_priority}</span> priority based on context urgency and importance
            </p>
          </div>
        )}

        {/* Deadline Suggestion */}
        {analysisResult.suggested_deadline && (
          <div className="border border-indigo-200 dark:border-indigo-800 rounded-lg p-3 bg-indigo-50 dark:bg-indigo-900/20">
            <h4 className="font-medium text-indigo-800 dark:text-indigo-200 mb-1">
              Deadline Suggestion
            </h4>
            <p className="text-sm text-indigo-700 dark:text-indigo-300">
              Suggested deadline: <span className="font-medium">{analysisResult.suggested_deadline}</span>
            </p>
          </div>
        )}

        {/* Category Suggestion */}
        {analysisResult.suggested_category && (
          <div className="border border-teal-200 dark:border-teal-800 rounded-lg p-3 bg-teal-50 dark:bg-teal-900/20">
            <h4 className="font-medium text-teal-800 dark:text-teal-200 mb-1">
              Category Suggestion
            </h4>
            <p className="text-sm text-teal-700 dark:text-teal-300">
              Suggested category: <span className="font-medium">{analysisResult.suggested_category.name}</span>
              {analysisResult.suggested_category.confidence && (
                <span className="ml-2 text-xs">({analysisResult.suggested_category.confidence}% confidence)</span>
              )}
            </p>
          </div>
        )}

        {/* Context Summary */}
        <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-3 bg-gray-50 dark:bg-gray-700">
          <h4 className="font-medium text-gray-800 dark:text-gray-200 mb-2">
            Analysis Summary
          </h4>
          <div className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
            {analysisResult.extracted_tasks && (
              <p><strong>Tasks Identified:</strong> {analysisResult.extracted_tasks.length}</p>
            )}
            {analysisResult.insights && (
              <p><strong>Key Insights:</strong> {analysisResult.insights.length}</p>
            )}
            {analysisResult.suggested_actions && (
              <p><strong>Suggested Actions:</strong> {analysisResult.suggested_actions.length}</p>
            )}
            <p><strong>Analysis Confidence:</strong> High</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AITaskSuggestions; 