import React, { useState } from "react";
import ContextAnalysisForm from "./ContextAnalysisForm";
import AITaskSuggestions from "./AITaskSuggestions";
import { aiAnalyzeContext, aiHealthCheck } from "@/services/api";

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
      console.log('Starting context analysis...');
      
      // Check AI service health first
      try {
        const healthCheck = await aiHealthCheck();
        console.log('AI health check:', healthCheck);
        
        if (!healthCheck.ai_health?.services_available) {
          throw new Error('AI services are not available. Please check your GEMINI_API_KEY configuration.');
        }
      } catch (healthError) {
        console.error('AI health check failed:', healthError);
        throw new Error('AI services are not available. Please check your configuration.');
      }
      
      // Structure the context data properly for AI analysis
      const contextDataForAI = {
        content: contextData,
        source: "manual_input",
        timestamp: new Date().toISOString()
      };
      
      console.log('Sending context data:', contextDataForAI);
      
      const result = await aiAnalyzeContext(contextDataForAI);
      
      console.log('Received analysis result:', result);
      
      setAnalysisResult(result.analysis);
      setShowForm(true);
    } catch (err) {
      console.error('Context analysis error:', err);
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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      <div className="max-w-7xl mx-auto p-6">
        {/* Enhanced Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent mb-4">
            Intelligent Context Analysis
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Analyze your context and create AI-enhanced tasks automatically with advanced natural language processing
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Side - Context Input */}
          <div className="space-y-6">
            {/* Enhanced Context Input Section */}
            <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-white/20 dark:border-slate-700/50">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
                  Context Input
                </h2>
              </div>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
                    Context Data (emails, messages, notes, etc.)
                  </label>
                  <textarea
                    value={contextData}
                    onChange={(e) => setContextData(e.target.value)}
                    placeholder="Paste your context data here... (emails, messages, meeting notes, etc.)"
                    className="w-full px-4 py-4 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none"
                    rows={8}
                    disabled={isAnalyzing}
                  />
                </div>
                
                <div className="flex gap-4">
                  <button
                    onClick={handleAnalyzeContext}
                    disabled={!contextData.trim() || isAnalyzing}
                    className="flex-1 px-6 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 disabled:opacity-50 disabled:transform-none flex items-center justify-center gap-3"
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        Analyze Context
                      </>
                    )}
                  </button>
                  
                  <button
                    onClick={clearAll}
                    disabled={!contextData && !analysisResult}
                    className="px-6 py-4 bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-xl hover:bg-slate-300 dark:hover:bg-slate-600 disabled:opacity-50 transition-all duration-200 font-medium"
                  >
                    Clear
                  </button>
                </div>
              </div>
            </div>

            {/* Enhanced Error Display */}
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-2xl p-6">
                <div className="flex items-start gap-4">
                  <div className="p-2 bg-red-100 dark:bg-red-900/50 rounded-lg">
                    <svg className="w-5 h-5 text-red-600 dark:text-red-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-red-800 dark:text-red-200 mb-2">
                      Analysis Error
                    </h3>
                    <p className="text-red-700 dark:text-red-300">
                      {error}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Enhanced Sample Context Data */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-200 dark:border-blue-800 rounded-2xl p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg">
                  <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-blue-800 dark:text-blue-200">
                  Sample Context Data
                </h3>
              </div>
              <div className="space-y-3 text-sm text-blue-700 dark:text-blue-300">
                <div className="p-3 bg-white/50 dark:bg-blue-900/30 rounded-lg">
                  <strong>Email:</strong> "Hi team, we have a client meeting tomorrow at 2 PM. Please prepare the quarterly sales report and have the new product demo ready."
                </div>
                <div className="p-3 bg-white/50 dark:bg-blue-900/30 rounded-lg">
                  <strong>Meeting Notes:</strong> "Project deadline moved to Friday. Need to finish the backend API integration and update documentation."
                </div>
                <div className="p-3 bg-white/50 dark:bg-blue-900/30 rounded-lg">
                  <strong>Slack:</strong> "Hey team, just got an email from the client. They want to move the project deadline to this Friday instead of next week."
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - Analysis Results & Form */}
          <div className="space-y-6">
            {/* Enhanced AI Analysis Results */}
            {analysisResult && (
              <div className="card-hover">
                <AITaskSuggestions 
                  analysisResult={analysisResult}
                  onRegenerate={handleRegenerateData}
                  isRegenerating={isAnalyzing}
                />
              </div>
            )}

            {/* Enhanced Extracted Tasks Display */}
            {analysisResult?.extracted_tasks && analysisResult.extracted_tasks.length > 0 && (
              <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl shadow-xl p-6 border border-white/20 dark:border-slate-700/50">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100">
                    Extracted Tasks ({analysisResult.extracted_tasks.length})
                  </h3>
                </div>
                <div className="space-y-4">
                  {analysisResult.extracted_tasks.map((task: any, index: number) => (
                    <div key={index} className="p-4 bg-gradient-to-r from-slate-50 to-blue-50 dark:from-slate-700 dark:to-slate-600 border border-slate-200 dark:border-slate-600 rounded-xl">
                      <h4 className="font-semibold text-slate-900 dark:text-slate-100 mb-2">{task.title}</h4>
                      {task.description && (
                        <p className="text-sm text-slate-600 dark:text-slate-400 mb-3 leading-relaxed">{task.description}</p>
                      )}
                      {task.priority && (
                        <span className="inline-block px-3 py-1 text-xs bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 rounded-full font-medium">
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

        {/* Enhanced Slide-out Form */}
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