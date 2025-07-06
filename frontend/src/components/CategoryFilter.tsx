import React, { useState, useRef, useEffect } from "react";
import { useCategories } from "@/contexts/CategoriesContext";

interface CategoryFilterProps {
  value: string | "All";
  onChange: (value: string | "All") => void;
}

const CategoryFilter: React.FC<CategoryFilterProps> = ({ value, onChange }) => {
  const { categories } = useCategories();
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setOpen(false);
    }
  };

  useEffect(() => {
    if (open) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  const selectedCategory = value === "All" ? null : categories.find(cat => cat.id === value);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        type="button"
        className={`
          w-full px-4 py-2 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 
          rounded-xl text-left transition-all duration-200
          hover:bg-white dark:hover:bg-slate-700 hover:border-slate-300 dark:hover:border-slate-500 
          focus:ring-2 focus:ring-blue-500 focus:border-transparent
          ${open ? 'ring-2 ring-blue-500 border-transparent' : ''}
        `}
        onClick={() => setOpen(v => !v)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <span className={`${selectedCategory ? 'text-slate-900 dark:text-white' : 'text-slate-500 dark:text-slate-400'}`}>
              {selectedCategory ? selectedCategory.name : "All Categories"}
            </span>
          </div>
          <svg 
            className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${open ? 'rotate-180' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>
      
      {open && (
        <div className="absolute z-[9999] mt-2 w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 rounded-xl shadow-lg max-h-48 overflow-y-auto">
          <div className="p-1">
            {/* All Categories Option */}
            <button
              className={`
                w-full text-left px-3 py-2 rounded-lg transition-all duration-200
                ${value === "All" 
                  ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300' 
                  : 'hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300'
                }
              `}
              onClick={() => { 
                onChange("All"); 
                setOpen(false); 
              }}
            >
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
                <span className="font-medium">All Categories</span>
              </div>
            </button>
            
            {/* Category Options */}
            {categories.map(cat => (
              <button
                key={cat.id}
                className={`
                  w-full text-left px-3 py-2 rounded-lg transition-all duration-200
                  ${value === cat.id 
                    ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300' 
                    : 'hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300'
                  }
                `}
                onClick={() => { 
                  onChange(cat.id); 
                  setOpen(false); 
                }}
              >
                <div className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  <span className="font-medium">{cat.name}</span>
                </div>
              </button>
            ))}
            
            {categories.length === 0 && (
              <div className="px-3 py-2 text-sm text-slate-500 dark:text-slate-400">
                No categories available
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CategoryFilter;