import React, { useState, useRef, useEffect } from "react";
import { useCategories } from "@/contexts/CategoriesContext";

interface SmartCategorySelectorProps {
  analysisResult: any;
  selectedCategory: string;
  onCategoryChange: (categoryId: string) => void;
  onCreateNewCategory: () => void;
  disabled?: boolean;
}

interface CategorySuggestion {
  name: string;
  reason: string;
  confidence: number;
  relevance: string;
}

const SmartCategorySelector: React.FC<SmartCategorySelectorProps> = ({
  analysisResult,
  selectedCategory,
  onCategoryChange,
  onCreateNewCategory,
  disabled = false
}) => {
  const { categories } = useCategories();
  const [showSuggestions, setShowSuggestions] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Get AI-suggested categories from analysis result
  const getAISuggestedCategories = (): CategorySuggestion[] => {
    if (analysisResult?.category_suggestions && Array.isArray(analysisResult.category_suggestions)) {
      return analysisResult.category_suggestions;
    }
    return [];
  };

  const aiSuggestedCategories = getAISuggestedCategories();

  const handleCategorySelect = (categoryName: string, event?: React.MouseEvent) => {
    // Prevent form submission
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    
    // Check if this category already exists
    const existingCategory = categories.find(cat => cat.name.toLowerCase() === categoryName.toLowerCase());
    
    if (existingCategory) {
      // Use existing category ID
      onCategoryChange(existingCategory.id);
    } else {
      // For new AI-suggested categories, we'll need to create them
      // For now, pass the name and let the parent handle creation
      onCategoryChange(categoryName);
    }
    
    setShowSuggestions(false);
  };

  const getSelectedCategoryName = () => {
    if (!selectedCategory) return "Select a category";
    
    // Check existing categories
    const existingCategory = categories.find(cat => cat.id === selectedCategory);
    if (existingCategory) {
      return existingCategory.name;
    }
    
    // Check AI-suggested categories
    const aiCategory = aiSuggestedCategories.find(cat => cat.name === selectedCategory);
    if (aiCategory) {
      return aiCategory.name;
    }
    
    return selectedCategory; // Return the name if it's a new category
  };

  const getRelevanceColor = (relevance: string) => {
    switch (relevance.toLowerCase()) {
      case 'high':
        return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
      case 'medium':
        return 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200';
      case 'low':
        return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200';
      default:
        return 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200';
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Main Category Dropdown */}
      <div className="flex gap-2">
        <select
          value={selectedCategory}
          onChange={(e) => onCategoryChange(e.target.value)}
          className="flex-1 border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          disabled={disabled}
        >
          <option value="">Select a category</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>
        
        <button
          type="button"
          onClick={() => setShowSuggestions(!showSuggestions)}
          disabled={disabled || aiSuggestedCategories.length === 0}
          className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-1"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          AI
        </button>
        
        <button
          type="button"
          onClick={onCreateNewCategory}
          disabled={disabled}
          className="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          +
        </button>
      </div>

      {/* AI Suggestions Dropdown */}
      {showSuggestions && aiSuggestedCategories.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg z-10">
          <div className="p-2">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 px-2">
              AI-Suggested Categories
            </h4>
            <div className="space-y-1 max-h-48 overflow-y-auto">
              {aiSuggestedCategories.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={(e) => handleCategorySelect(suggestion.name, e)}
                  className="w-full text-left p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700"
                >
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {suggestion.name}
                      </span>
                      <span className={`text-xs px-2 py-1 rounded ${getRelevanceColor(suggestion.relevance)}`}>
                        {suggestion.relevance}
                      </span>
                      <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-1.5 py-0.5 rounded">
                        AI
                      </span>
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {Math.round(suggestion.confidence * 100)}%
                    </span>
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-300 line-clamp-1">
                    {suggestion.reason}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Selected Category Display */}
      {selectedCategory && (
        <div className="mt-2 p-2 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-700 dark:text-gray-300">
              Selected: <span className="font-medium">{getSelectedCategoryName()}</span>
            </span>
            {aiSuggestedCategories.some(cat => cat.name === selectedCategory) && (
              <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                AI Suggested
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SmartCategorySelector; 