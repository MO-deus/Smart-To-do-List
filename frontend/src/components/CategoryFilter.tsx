import React from "react";

const categories = ["All", "Work", "Personal", "Urgent"];

interface CategoryFilterProps {
  value: string;
  onChange: (value: string) => void;
}

const CategoryFilter: React.FC<CategoryFilterProps> = ({ value, onChange }) => {
  return (
    <div className="flex items-center gap-2">
      <label htmlFor="category" className="text-sm font-medium text-gray-700 dark:text-gray-200">Category:</label>
      <select
        id="category"
        className="border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {categories.map((cat) => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>
    </div>
  );
};

export default CategoryFilter; 