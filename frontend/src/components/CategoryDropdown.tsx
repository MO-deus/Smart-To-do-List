import React, { useState, useRef } from "react";
import { useCategories } from "@/contexts/CategoriesContext";

interface CategoryDropdownProps {
  value: string;
  onChange: (value: string) => void;
  onCreateNewCategory?: () => void;
  disabled?: boolean;
}

const MAX_VISIBLE = 5;

const CategoryDropdown: React.FC<CategoryDropdownProps> = ({ value, onChange, onCreateNewCategory, disabled }) => {
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
    <div className="relative" ref={dropdownRef}>
      <button
        type="button"
        className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-left"
        onClick={() => setOpen(v => !v)}
        disabled={disabled}
      >
        {selected ? selected.name : "Select a category"}
      </button>
      {open && (
        <div className="absolute z-10 mt-1 w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded shadow max-h-48 overflow-y-auto" style={{ maxHeight: `${MAX_VISIBLE * 2.5}rem` }}>
          {categories.map(cat => (
            <div
              key={cat.id}
              className={`px-3 py-2 cursor-pointer hover:bg-blue-100 dark:hover:bg-blue-900 ${value === cat.id ? "bg-blue-50 dark:bg-blue-900" : ""}`}
              onClick={() => { onChange(cat.id); setOpen(false); }}
            >
              {cat.name}
            </div>
          ))}
          <div
            className="px-3 py-2 cursor-pointer text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900 border-t border-gray-200 dark:border-gray-700"
            onClick={() => { setOpen(false); onCreateNewCategory && onCreateNewCategory(); }}
          >
            + Create new category
          </div>
        </div>
      )}
    </div>
  );
};

export default CategoryDropdown; 