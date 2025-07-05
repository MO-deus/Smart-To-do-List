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
  const { refreshCategories } = useCategories();

  // Auto-fill form with AI suggestions
  useEffect(() => {
    if (analysisResult) {
      // Set title from extracted tasks
      if (analysisResult.extracted_tasks && analysisResult.extracted_tasks.length > 0) {
        const firstTask = analysisResult.extracted_tasks[0];
        if (firstTask.title && firstTask.title.trim() && firstTask.title !== 'Task from Context Analysis') {
          setTitle(firstTask.title.trim());
        }
      }
      
      // If no good title from extracted tasks, try to create one from context
      if (!title && analysisResult.context_summary) {
        const summary = analysisResult.context_summary;
        // Extract a simple title from the summary
        const words = summary.split(' ').slice(0, 5).join(' ');
        setTitle(words + (words.endsWith('.') ? '' : '...'));
      }
      
      // Set description from extracted tasks
      if (analysisResult.extracted_tasks && analysisResult.extracted_tasks.length > 0) {
        const firstTask = analysisResult.extracted_tasks[0];
        if (firstTask.description && firstTask.description.trim()) {
          setDescription(firstTask.description.trim());
        }
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
      if (analysisResult.workload_analysis?.suggested_deadlines) {
        const deadlines = analysisResult.workload_analysis.suggested_deadlines;
        if (deadlines.length > 0) {
          // Use the highest confidence deadline
          const bestDeadline = deadlines[0];
          setDeadline(bestDeadline.date);
        }
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
  }, [analysisResult]);

  const handleCreateCategory = async () => {
    if (!newCategoryName.trim()) return;
    
    try {
      setIsLoading(true);
      const newCat = await createCategory(newCategoryName.trim());
      await refreshCategories();
      setCategory(newCat.id);
      setShowNewCategory(false);
    } catch (error) {
      console.error("Failed to create category:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    
    try {
      setIsLoading(true);
      
      // Handle category selection
      let finalCategory = category;
      
      // If an AI-suggested category is selected, find or create it
      if (category && !category.includes('-')) { // AI-suggested categories don't have UUIDs
        const categories = await fetchCategories();
        const existingCategory = categories.find((cat: any) => cat.name.toLowerCase() === category.toLowerCase());
        
        if (existingCategory) {
          finalCategory = existingCategory.id;
        } else {
          // Create the AI-suggested category
          const newCat = await createCategory(category);
          await refreshCategories();
          finalCategory = newCat.id;
        }
      } else if (!finalCategory && newCategoryName.trim()) {
        // Create the manually entered category
        const newCat = await createCategory(newCategoryName.trim());
        await refreshCategories();
        finalCategory = newCat.id;
      } else if (!finalCategory) {
        // Use a default category or create one
        const defaultCategoryName = 'General';
        const categories = await fetchCategories();
        const existingGeneral = categories.find((cat: any) => cat.name.toLowerCase() === defaultCategoryName.toLowerCase());
        
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

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-end bg-black bg-opacity-60">
      <div className="bg-white dark:bg-gray-900 h-full w-full max-w-2xl shadow-2xl overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              AI-Enhanced Task Creation
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* AI Analysis Summary */}
          <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">
              AI Analysis Summary
            </h3>
            <div className="space-y-2 text-sm text-blue-700 dark:text-blue-300">
              {analysisResult.priority_insights?.urgency_level && (
                <p><strong>Urgency:</strong> {analysisResult.priority_insights.urgency_level}</p>
              )}
              {analysisResult.extracted_tasks && (
                <p><strong>Tasks Found:</strong> {analysisResult.extracted_tasks.length}</p>
              )}
              {analysisResult.workload_analysis?.workload_level && (
                <p><strong>Workload Level:</strong> {analysisResult.workload_analysis.workload_level}</p>
              )}
              {analysisResult.category_suggestions && (
                <p><strong>Category Suggestions:</strong> {analysisResult.category_suggestions.length}</p>
              )}
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
                Task Title
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                required
                disabled={isLoading}
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
                Description
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={4}
                className="w-full border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                disabled={isLoading}
              />
            </div>

            {/* Smart Category Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
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
                <div className="flex gap-2 mt-2">
                  <input
                    type="text"
                    value={newCategoryName}
                    onChange={(e) => setNewCategoryName(e.target.value)}
                    placeholder="New category name"
                    className="flex-1 border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                    required
                    disabled={isLoading}
                  />
                  <button
                    type="button"
                    onClick={handleCreateCategory}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                    disabled={!newCategoryName.trim()}
                  >
                    Add
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowNewCategory(false)}
                    className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600"
                    disabled={isLoading}
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>

            {/* Priority with AI Suggestion */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
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
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
                Deadline
              </label>
              <DeadlineSuggestion
                deadline={deadline}
                onDeadlineChange={setDeadline}
                suggestedDeadline={analysisResult.suggested_deadline}
                aiDeadlineSuggestions={analysisResult.workload_analysis?.suggested_deadlines}
                contextData={contextData}
                disabled={isLoading}
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
              <button
                type="button"
                onClick={handleRegenerate}
                disabled={isRegenerating}
                className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isRegenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Regenerating...
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Regenerate Data
                  </>
                )}
              </button>
              
              <button
                type="button"
                onClick={onClose}
                className="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600"
                disabled={isLoading}
              >
                Cancel
              </button>
              
              <button
                type="submit"
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                disabled={isLoading || !title.trim()}
              >
                {isLoading ? "Creating..." : "Create Task"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ContextAnalysisForm; 