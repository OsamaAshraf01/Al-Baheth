import React, { useState, useEffect, useRef } from 'react';
import { Search, Upload, X } from 'lucide-react';
import { motion } from 'framer-motion';

interface SearchBarProps {
  onSearch: (query: string) => void;
  onUpload?: () => void;
  initialQuery?: string;
  placeholder?: string;
  autoFocus?: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({ 
  onSearch, 
  onUpload,
  initialQuery = '', 
  placeholder = 'Search documents...', 
  autoFocus = false 
}) => {
  const [query, setQuery] = useState(initialQuery);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocus]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  const clearSearch = () => {
    setQuery('');
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <motion.form 
      onSubmit={handleSubmit}
      className="w-full"
      initial={{ scale: 0.95 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      <div className="relative flex items-center">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Search size={20} className="text-gray-400" />
        </div>
        
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="w-full py-4 pl-12 pr-32 rounded-xl bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 text-gray-900 dark:text-gray-100 placeholder-gray-400 shadow-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
          aria-label="Search"
        />
        
        <div className="absolute right-2 flex items-center space-x-1">
          {query && (
            <button
              type="button"
              onClick={clearSearch}
              className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600"
              aria-label="Clear search"
            >
              <X size={18} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
            </button>
          )}
          
          {onUpload && (
            <>
              <div className="w-px h-6 bg-gray-200 dark:bg-gray-600 mx-1"></div>
              
              <button
                type="button"
                onClick={onUpload}
                className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600"
                aria-label="Upload document"
              >
                <Upload size={18} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
              </button>
            </>
          )}
        </div>
      </div>
    </motion.form>
  );
};

export default SearchBar;