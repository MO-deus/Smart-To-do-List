import React from "react";
import { useCategories } from "@/contexts/CategoriesContext";

interface CategoryFilterProps {
  value: string | "All";
  onChange: (value: string | "All") => void;
}

const CategoryFilter: React.FC<CategoryFilterProps> = ({ value, onChange }) => {
  const { categories } = useCategories();

  return (
    <div className="flex items-center gap-2">
      <label htmlFor="category" className="text-sm font-medium text-gray-700 dark:text-gray-200">Category:</label>
      <select
        id="category"
        className="border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
        value={value}
        onChange={e => {
          const val = e.target.value;
          onChange(val === "All" ? "All" : val);
        }}
      >
        <option value="All">All</option>
        {categories.map(cat => (
          <option key={cat.id} value={cat.id}>{cat.name}</option>
        ))}
      </select>
    </div>
  );
};

export default CategoryFilter;