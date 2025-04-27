import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import SearchBar from '../components/SearchBar';
import ResultItem from '../components/ResultItem';
import PageTransition from '../components/PageTransition';
import { SearchResult } from '../types';

interface LocationState {
  results: SearchResult[];
  query: string;
}

const ResultsPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { results = [], query = '' } = (location.state as LocationState) || {};

  const handleSearch = (searchQuery: string) => {
    // Navigate back to home with search results
    navigate(`/?query=${encodeURIComponent(searchQuery)}`);
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  // Remove navigation to details page
  // const handleSelectResult = (id: string) => {
  //   navigate(`/result/${id}?query=${encodeURIComponent(query)}`);
  // };

  // Animation variants for staggered animations
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { 
        staggerChildren: 0.07,
        delayChildren: 0.2
      }
    }
  };

  return (
    <PageTransition className="min-h-screen pt-16 pb-8">
      <div className="container mx-auto px-4">
        <div className="max-w-5xl mx-auto">
          {/* Top navigation */}
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <motion.button
                onClick={handleGoBack}
                className="flex items-center text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400"
                whileHover={{ x: -5 }}
                whileTap={{ scale: 0.95 }}
              >
                <ArrowLeft size={20} className="mr-1" />
                <span>Back to home</span>
              </motion.button>
              
              <motion.div 
                className="w-1/2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
              >
                <SearchBar
                  onSearch={handleSearch}
                  initialQuery={query}
                  placeholder="Search again..."
                />
              </motion.div>
            </div>
          </div>
          
          {/* Results header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="bg-white dark:bg-gray-800 shadow-soft rounded-xl p-6 mb-6"
          >
            <h1 className="text-2xl font-medium text-gray-900 dark:text-white">
              Results for <motion.span 
                className="text-primary-600 dark:text-primary-400"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3, type: "spring" }}
              >"{query}"</motion.span>
            </h1>
            <p className="text-gray-500 dark:text-gray-400 mt-2">
              Found {results.length} documents matching your search
            </p>
          </motion.div>
          
          {/* Results list */}
          <motion.div 
            className="space-y-4"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {results.length > 0 ? (
              results.map((result, index) => (
                <ResultItem 
                  key={result.id} 
                  result={result} 
                  onClick={() => {}} 
                  delay={index}
                />
              ))
            ) : (
              <motion.div 
                className="bg-white dark:bg-gray-800 shadow-soft rounded-xl p-12 text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <p className="text-gray-500 dark:text-gray-400">
                  No results found. Try a different search query.
                </p>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>
    </PageTransition>
  );
};

export default ResultsPage;