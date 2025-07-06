import React, { useState, useRef, useEffect } from "react";
import { useCategories } from "@/contexts/CategoriesContext";

interface CategoryDropdownProps {
  value: string;
  onChange: (value: string) => void;
  onCreateNewCategory?: () => void;
  disabled?: boolean;
  className?: string;
}

const MAX_VISIBLE = 5;

const CategoryDropdown: React.FC<CategoryDropdownProps> = ({ 
  value, 
  onChange, 
  onCreateNewCategory, 
  disabled = false,
  className = ''
}) => {
  const { categories } = useCategories();
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
      setOpen(false);
    }
  };

  React.useEffect(() => {
    if (open) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  const selected = categories.find(cat => cat.id === value);

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      <button
        type="button"
        className={`
          w-full px-4 py-2 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 
          rounded-xl text-left transition-all duration-200
          ${disabled 
            ? 'opacity-50 cursor-not-allowed' 
            : 'hover:bg-white dark:hover:bg-slate-700 hover:border-slate-300 dark:hover:border-slate-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent'
          }
          ${open ? 'ring-2 ring-blue-500 border-transparent' : ''}
        `}
        onClick={() => !disabled && setOpen(v => !v)}
        disabled={disabled}
      >
        <div className="flex items-center justify-between">
          <span className={`${selected ? 'text-slate-900 dark:text-white' : 'text-slate-500 dark:text-slate-400'}`}>
            {selected ? selected.name : "Select a category"}
          </span>
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
            {categories.length === 0 ? (
              <div className="px-3 py-2 text-sm text-slate-500 dark:text-slate-400">
                No categories available
              </div>
            ) : (
              categories.map(cat => (
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
              ))
            )}
            
            {onCreateNewCategory && (
              <button
                className="w-full text-left px-3 py-2 rounded-lg text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 transition-all duration-200 border-t border-slate-200 dark:border-slate-700 mt-1"
                onClick={() => { 
                  setOpen(false); 
                  onCreateNewCategory(); 
                }}
              >
                <div className="flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <span className="font-medium">Create new category</span>
                </div>
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CategoryDropdown; 