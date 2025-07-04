import React, { useEffect, useState } from "react";
import { fetchCategories } from "@/services/api";

interface CategoryFilterProps {
  value: string;
  onChange: (value: string) => void;
}

const CategoryFilter: React.FC<CategoryFilterProps> = ({ value, onChange }) => {
  const [categories, setCategories] = useState<string[]>(["All"]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories()
      .then((data) => {
        setCategories(["All", ...data.map((cat: any) => cat.name)]);
      })
      .catch(() => setCategories(["All"]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex items-center gap-2">
      <label htmlFor="category" className="text-sm font-medium text-gray-700 dark:text-gray-200">Category:</label>
      <select
        id="category"
        className="border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={loading}
      >
        {categories.map((cat) => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>
    </div>
  );
};

export default CategoryFilter; 