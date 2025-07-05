"use client";
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { fetchCategories } from '@/services/api';

interface Category {
  id: string;
  name: string;
  usage_frequency: number;
}

interface CategoriesContextType {
  categories: Category[];
  refreshCategories: () => Promise<void>;
  isLoading: boolean;
}

const CategoriesContext = createContext<CategoriesContextType | undefined>(undefined);

export const useCategories = () => {
  const context = useContext(CategoriesContext);
  if (context === undefined) {
    throw new Error('useCategories must be used within a CategoriesProvider');
  }
  return context;
};

interface CategoriesProviderProps {
  children: ReactNode;
}

export const CategoriesProvider: React.FC<CategoriesProviderProps> = ({ children }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const refreshCategories = async () => {
    try {
      setIsLoading(true);
      const data = await fetchCategories();
      setCategories(data);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshCategories();
  }, []);

  return (
    <CategoriesContext.Provider value={{ categories, refreshCategories, isLoading }}>
      {children}
    </CategoriesContext.Provider>
  );
}; 