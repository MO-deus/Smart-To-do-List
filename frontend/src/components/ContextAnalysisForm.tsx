import React, { useState, useEffect } from "react";
import { createCategory, createTask, fetchCategories } from "@/services/api";
import CategoryDropdown from "@/components/CategoryDropdown";
import { useCategories } from "@/contexts/CategoriesContext";
import SmartCategorySelector from "@/components/SmartCategorySelector";
import TaskPriorityIndicator from "./TaskPriorityIndicator";
import DeadlineSuggestion from "./DeadlineSuggestion";

interface ContextAnalysisFormProps {
  analysisResult: any;
  contextData: string;
  onClose: () => void;
  onTaskCreated: (task: any) => void;
  onRegenerateData: () => void;
  isRegenerating: boolean;
}

const ContextAnalysisForm: React.FC<ContextAnalysisFormProps> = ({
  analysisResult,
  contextData,
  onClose,
  onTaskCreated,
  onRegenerateData,
  isRegenerating
}) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState<string>("");
  const [priority, setPriority] = useState(2);
  const [deadline, setDeadline] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [showNewCategory, setShowNewCategory] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [currentTaskIndex, setCurrentTaskIndex] = useState(0);
  const { refreshCategories } = useCategories();

  // Auto-fill form with AI suggestions
  useEffect(() => {
    if (analysisResult) {
      updateFormWithTask(currentTaskIndex);
    }
  }, [analysisResult, currentTaskIndex]);

  const updateFormWithTask = (taskIndex: number) => {
    if (analysisResult?.extracted_tasks && analysisResult.extracted_tasks.length > 0) {
      const task = analysisResult.extracted_tasks[taskIndex];
      
      // Set title from extracted task
      if (task.title && task.title.trim() && task.title !== 'Task from Context Analysis') {
        setTitle(task.title.trim());
      } else if (analysisResult.context_summary) {
        const summary = analysisResult.context_summary;
        const words = summary.split(' ').slice(0, 5).join(' ');
        setTitle(words + (words.endsWith('.') ? '' : '...'));
      }
      
      // Set description from extracted task
      if (task.description && task.description.trim()) {
        setDescription(task.description.trim());
      }
      
      // Set priority from priority insights
      if (analysisResult.priority_insights?.urgency_level) {
        const insights = analysisResult.priority_insights;
        const priorityMap: { [key: string]: number } = {
          'high': 3,
          'medium': 2,
          'low': 1
        };
        setPriority(priorityMap[insights.urgency_level.toLowerCase()] || 2);
      }

      // Set deadline from temporal data or workload analysis
      const deadlineSuggestions = 
        analysisResult.workload_analysis?.suggested_deadlines ||
        analysisResult.detailed_analysis?.deadline_suggestion?.suggested_deadlines ||
        analysisResult.deadline_suggestions ||
        [];
      
      if (deadlineSuggestions.length > 0) {
        // Use the highest confidence deadline
        const bestDeadline = deadlineSuggestions[0];
        setDeadline(bestDeadline.date);
      }

      // Set category from context analysis
      if (analysisResult.context_summary) {
        // Try to extract category from context summary
        const summary = analysisResult.context_summary.toLowerCase();
        if (summary.includes('work') || summary.includes('project') || summary.includes('meeting')) {
          setNewCategoryName('Work');
          setShowNewCategory(true);
        } else if (summary.includes('personal') || summary.includes('home') || summary.includes('family')) {
          setNewCategoryName('Personal');
          setShowNewCategory(true);
        } else if (summary.includes('health') || summary.includes('exercise') || summary.includes('fitness')) {
          setNewCategoryName('Health');
          setShowNewCategory(true);
        }
      }
    }
  };

  const navigateToTask = (direction: 'prev' | 'next') => {
    if (!analysisResult?.extracted_tasks) return;
    
    const totalTasks = analysisResult.extracted_tasks.length;
    if (totalTasks === 0) return;
    
    if (direction === 'prev') {
      setCurrentTaskIndex(prev => prev > 0 ? prev - 1 : totalTasks - 1);
    } else {
      setCurrentTaskIndex(prev => prev < totalTasks - 1 ? prev + 1 : 0);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowLeft') {
      e.preventDefault();
      navigateToTask('prev');
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      navigateToTask('next');
    }
  };

  const handleCreateCategory = async () => {
    if (!newCategoryName.trim()) return;
    
    try {
      setIsLoading(true);
      const newCat = await createCategory(newCategoryName.trim());
      await refreshCategories();
      setCategory(newCat.id);
      setShowNewCategory(false);
      setNewCategoryName("");
    } catch (error) {
      console.error("Failed to create category:", error);
      alert("Failed to create category. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsLoading(true);
    try {
      let finalCategory = category;

      // Check if category is a name (AI suggestion) or ID
      const categories = await fetchCategories();
      const existingCategory = categories.data.find((cat: any) => cat.id === category);
      const isCategoryName = category && !existingCategory; // If not found by ID, it's likely a name
      
      if (isCategoryName && category) {
        // This is an AI-suggested category name, create it
        const newCat = await createCategory(category);
        await refreshCategories();
        finalCategory = newCat.id;
      } else if (!finalCategory && newCategoryName.trim()) {
        // Create the manually entered category
        const newCat = await createCategory(newCategoryName.trim());
        await refreshCategories();
        finalCategory = newCat.id;
      } else if (!finalCategory) {
        // Use a default category or create one
        const defaultCategoryName = 'General';
        const existingGeneral = categories.data.find((cat: any) => cat.name.toLowerCase() === defaultCategoryName.toLowerCase());
        
        if (existingGeneral) {
          finalCategory = existingGeneral.id;
        } else {
          const newCat = await createCategory(defaultCategoryName);
          await refreshCategories();
          finalCategory = newCat.id;
        }
      }
      
      const newTask = await createTask({
        title: title.trim(),
        description: description.trim(),
        category: finalCategory,
        priority,
        deadline: deadline || undefined,
        status: 'Pending'
      });
      
      onTaskCreated(newTask);
    } catch (error) {
      console.error("Failed to create task:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = () => {
    onRegenerateData();
  };

  const extractedTasks = analysisResult?.extracted_tasks || [];
  const totalTasks = extractedTasks.length;
  const currentTask = extractedTasks[currentTaskIndex];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-end bg-black/50 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-800 h-full w-full max-w-2xl shadow-2xl overflow-y-auto border-l border-white/20 dark:border-slate-700/50">
        {/* Enhanced Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-white/20 rounded-lg">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold">
                AI-Enhanced Task Creation
              </h2>
            </div>
            <button
              onClick={onClose}
              className="text-white/80 hover:text-white transition-colors duration-200 p-2 hover:bg-white/10 rounded-lg"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p className="text-blue-100 text-sm">
            Review and customize the AI-generated task details
          </p>
        </div>

        {/* Task Navigation Header */}
        {totalTasks > 1 && (
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 border-b border-indigo-200 dark:border-indigo-800 p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <h3 className="text-lg font-semibold text-indigo-800 dark:text-indigo-200">
                  Task {currentTaskIndex + 1} of {totalTasks}
                </h3>
                {currentTask && (
                  <span className="text-sm text-indigo-600 dark:text-indigo-300 bg-indigo-100 dark:bg-indigo-900/50 px-3 py-1 rounded-full">
                    {currentTask.title?.substring(0, 30) || 'Untitled Task'}...
                  </span>
                )}
              </div>
              
              {/* Navigation Controls */}
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => navigateToTask('prev')}
                  className="p-2 bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-300 rounded-lg hover:bg-indigo-200 dark:hover:bg-indigo-800 transition-all duration-200"
                  title="Previous task (←)"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                
                <span className="text-sm text-indigo-600 dark:text-indigo-300 px-2">
                  {currentTaskIndex + 1} / {totalTasks}
                </span>
                
                <button
                  type="button"
                  onClick={() => navigateToTask('next')}
                  className="p-2 bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-300 rounded-lg hover:bg-indigo-200 dark:hover:bg-indigo-800 transition-all duration-200"
                  title="Next task (→)"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
            
            {/* Keyboard Navigation Hint */}
            <div className="mt-2 text-xs text-indigo-500 dark:text-indigo-400">
              💡 Use ← → arrow keys to navigate between tasks
            </div>
          </div>
        )}

        {/* Enhanced AI Analysis Summary */}
        <div className="p-6 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-b border-blue-200 dark:border-blue-800">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg">
              <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-blue-800 dark:text-blue-200">
              AI Analysis Summary
            </h3>
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            {analysisResult.priority_insights?.urgency_level && (
              <div className="p-3 bg-white/50 dark:bg-blue-900/30 rounded-lg">
                <div className="font-medium text-blue-700 dark:text-blue-300">Urgency</div>
                <div className="text-blue-800 dark:text-blue-200">{analysisResult.priority_insights.urgency_level}</div>
              </div>
            )}
            {analysisResult.extracted_tasks && (
              <div className="p-3 bg-white/50 dark:bg-blue-900/30 rounded-lg">
                <div className="font-medium text-blue-700 dark:text-blue-300">Tasks Found</div>
                <div className="text-blue-800 dark:text-blue-200">{analysisResult.extracted_tasks.length}</div>
              </div>
            )}
            {analysisResult.workload_analysis?.workload_level && (
              <div className="p-3 bg-white/50 dark:bg-blue-900/30 rounded-lg">
                <div className="font-medium text-blue-700 dark:text-blue-300">Workload</div>
                <div className="text-blue-800 dark:text-blue-200">{analysisResult.workload_analysis.workload_level}</div>
              </div>
            )}
            {analysisResult.category_suggestions && (
              <div className="p-3 bg-white/50 dark:bg-blue-900/30 rounded-lg">
                <div className="font-medium text-blue-700 dark:text-blue-300">Categories</div>
                <div className="text-blue-800 dark:text-blue-200">{analysisResult.category_suggestions.length}</div>
              </div>
            )}
          </div>
        </div>

        {/* Enhanced Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6" onKeyDown={handleKeyDown}>
          {/* Title */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
              Task Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-3 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              placeholder="Enter task title..."
              required
              disabled={isLoading}
            />
          </div>

          {/* Description */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              className="w-full px-4 py-3 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none"
              placeholder="Add task description..."
              disabled={isLoading}
            />
          </div>

          {/* Smart Category Selection */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
              Category
            </label>
            <SmartCategorySelector
              analysisResult={analysisResult}
              selectedCategory={category}
              onCategoryChange={setCategory}
              onCreateNewCategory={() => setShowNewCategory(true)}
              disabled={isLoading}
            />
            
            {showNewCategory && (
              <div className="flex gap-2 mt-3">
                <input
                  type="text"
                  value={newCategoryName}
                  onChange={(e) => setNewCategoryName(e.target.value)}
                  placeholder="New category name"
                  className="flex-1 px-4 py-2 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 rounded-lg text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  required
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={handleCreateCategory}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-all duration-200 font-medium"
                  disabled={!newCategoryName.trim() || isLoading}
                >
                  Add
                </button>
                <button
                  type="button"
                  onClick={() => setShowNewCategory(false)}
                  className="px-4 py-2 bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-lg hover:bg-slate-300 dark:hover:bg-slate-600 transition-all duration-200 font-medium"
                  disabled={isLoading}
                >
                  Cancel
                </button>
              </div>
            )}
          </div>

          {/* Priority with AI Suggestion */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
              Priority
            </label>
            <TaskPriorityIndicator
              priority={priority}
              onPriorityChange={setPriority}
              suggestedPriority={analysisResult.suggested_priority}
              disabled={isLoading}
            />
          </div>

          {/* Deadline Suggestion */}
          <div className="space-y-2">
            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
              Deadline
            </label>
            <DeadlineSuggestion
              deadline={deadline}
              onDeadlineChange={setDeadline}
              suggestedDeadline={analysisResult.suggested_deadline}
              aiDeadlineSuggestions={
                // Try multiple possible locations for deadline suggestions
                analysisResult.workload_analysis?.suggested_deadlines ||
                analysisResult.detailed_analysis?.deadline_suggestion?.suggested_deadlines ||
                analysisResult.deadline_suggestions ||
                []
              }
              contextData={contextData}
              disabled={isLoading}
            />
          </div>

          {/* Enhanced Action Buttons */}
          <div className="flex gap-4 pt-6 border-t border-slate-200 dark:border-slate-700">
            <button
              type="button"
              onClick={handleRegenerate}
              disabled={isRegenerating}
              className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 disabled:opacity-50 disabled:transform-none flex items-center justify-center gap-3"
            >
              {isRegenerating ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Regenerating...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Regenerate Data
                </>
              )}
            </button>
            
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-3 bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-xl hover:bg-slate-300 dark:hover:bg-slate-600 transition-all duration-200 font-medium"
              disabled={isLoading}
            >
              Cancel
            </button>
            
            <button
              type="submit"
              className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 transition-all duration-200 font-medium shadow-lg hover:shadow-xl"
              disabled={isLoading || !title.trim()}
            >
              {isLoading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Creating...
                </div>
              ) : (
                "Create Task"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ContextAnalysisForm; 