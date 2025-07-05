import React, { useState } from "react";
import ContextAnalysisForm from "./ContextAnalysisForm";
import AITaskSuggestions from "./AITaskSuggestions";
import { aiAnalyzeContext } from "@/services/api";

interface ContextAnalysisPageProps {
  onTaskCreated?: (task: any) => void;
}

const ContextAnalysisPage: React.FC<ContextAnalysisPageProps> = ({ onTaskCreated }) => {
  const [contextData, setContextData] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyzeContext = async () => {
    if (!contextData.trim()) return;
    
    setIsAnalyzing(true);
    setError(null);
    
    try {
      // Structure the context data properly for AI analysis
      const contextDataForAI = {
        content: contextData,
        source: "manual_input",
        timestamp: new Date().toISOString()
      };
      
      const result = await aiAnalyzeContext(contextDataForAI);
      
      setAnalysisResult(result.context_analysis);
      setShowForm(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRegenerateData = async () => {
    if (!contextData.trim()) return;
    await handleAnalyzeContext();
  };

  const handleTaskCreated = (task: any) => {
    if (onTaskCreated) {
      onTaskCreated(task);
    }
    setShowForm(false);
    setContextData("");
    setAnalysisResult(null);
  };

  const clearAll = () => {
    setContextData("");
    setAnalysisResult(null);
    setError(null);
    setShowForm(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Intelligent Context Analysis
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Analyze your context and create AI-enhanced tasks automatically
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Side - Context Input */}
          <div className="space-y-6">
            {/* Context Input Section */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                Context Input
              </h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
                    Context Data (emails, messages, notes, etc.)
                  </label>
                  <textarea
                    value={contextData}
                    onChange={(e) => setContextData(e.target.value)}
                    placeholder="Paste your context data here... (emails, messages, meeting notes, etc.)"
                    className="w-full border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                    rows={8}
                    disabled={isAnalyzing}
                  />
                </div>
                
                <div className="flex gap-3">
                  <button
                    onClick={handleAnalyzeContext}
                    disabled={!contextData.trim() || isAnalyzing}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        Analyze Context
                      </>
                    )}
                  </button>
                  
                  <button
                    onClick={clearAll}
                    disabled={!contextData && !analysisResult}
                    className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 disabled:opacity-50"
                  >
                    Clear
                  </button>
                </div>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <div className="flex">
                  <svg className="w-5 h-5 text-red-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                      Analysis Error
                    </h3>
                    <p className="text-sm text-red-700 dark:text-red-300 mt-1">
                      {error}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Sample Context Data */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">
                Sample Context Data
              </h3>
              <div className="space-y-2 text-sm text-blue-700 dark:text-blue-300">
                <p><strong>Email:</strong> "Hi team, we have a client meeting tomorrow at 2 PM. Please prepare the quarterly sales report and have the new product demo ready."</p>
                <p><strong>Meeting Notes:</strong> "Project deadline moved to Friday. Need to finish the backend API integration and update documentation."</p>
                <p><strong>Slack:</strong> "Hey team, just got an email from the client. They want to move the project deadline to this Friday instead of next week."</p>
              </div>
            </div>
          </div>

          {/* Right Side - Analysis Results & Form */}
          <div className="space-y-6">
            {/* AI Analysis Results */}
            {analysisResult && (
              <AITaskSuggestions 
                analysisResult={analysisResult}
                onRegenerate={handleRegenerateData}
                isRegenerating={isAnalyzing}
              />
            )}

            {/* Extracted Tasks Display */}
            {analysisResult?.extracted_tasks && analysisResult.extracted_tasks.length > 0 && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                  Extracted Tasks ({analysisResult.extracted_tasks.length})
                </h3>
                <div className="space-y-3">
                  {analysisResult.extracted_tasks.map((task: any, index: number) => (
                    <div key={index} className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-700">
                      <h4 className="font-medium text-gray-900 dark:text-white">{task.title}</h4>
                      {task.description && (
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{task.description}</p>
                      )}
                      {task.priority && (
                        <span className="inline-block mt-2 px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded">
                          Priority: {task.priority}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Slide-out Form */}
        {showForm && analysisResult && (
          <ContextAnalysisForm
            analysisResult={analysisResult}
            contextData={contextData}
            onClose={() => setShowForm(false)}
            onTaskCreated={handleTaskCreated}
            onRegenerateData={handleRegenerateData}
            isRegenerating={isAnalyzing}
          />
        )}
      </div>
    </div>
  );
};

export default ContextAnalysisPage; 