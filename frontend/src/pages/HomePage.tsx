import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Search, Loader, X, ExternalLink, AlertCircle } from 'lucide-react';
import SearchBar from '../components/SearchBar';
import FileUploader from '../components/FileUploader';
import FileTypeIcon from '../components/FileTypeIcon';
import PageTransition from '../components/PageTransition';
import BackgroundLight from '../components/BackgroundLight';
import { SearchResult } from '../types';
import { getFileTypeFromExtension } from '../utils/fileUtils';
import { apiService } from '../utils/api';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [showUploader, setShowUploader] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiAvailable, setApiAvailable] = useState<boolean | null>(null);

  // Check API availability on component mount
  useEffect(() => {
    const checkAPI = async () => {
      try {
        const isAvailable = await apiService.checkAPIStatus();
        setApiAvailable(isAvailable);
      } catch (err) {
        setApiAvailable(false);
        console.error('Failed to check API status:', err);
      }
    };
    
    checkAPI();
  }, []);

  const handleSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    
    setQuery(searchQuery);
    setIsLoading(true);
    setShowResults(false);
    setShowUploader(false);
    setError(null);

    console.log("Starting search for:", searchQuery);

    try {
      const searchResults = await apiService.searchDocuments(searchQuery);
      console.log("Search results:", searchResults);
      
      setResults(searchResults);
      setShowResults(true);
      
      // Exit loading state even if no results
      setIsLoading(false);
      
      // Show no results message if applicable
      if (searchResults.length === 0) {
        console.log("No results found for the search query");
        setError(`No results found for "${searchQuery}". Try a different search term.`);
      }
    } catch (err: any) {
      console.error('Search error:', err);
      let errorMessage = 'Error searching documents. ';
      if (err.message) {
        errorMessage += err.message;
      }
      if (err.response) {
        errorMessage += ` (Status: ${err.response.status})`;
        console.error('Response data:', err.response.data);
      }
      setError(errorMessage);
      setIsLoading(false);
    }
  };

  const handleFileSelect = async (file: File) => {
    setIsLoading(true);
    setShowUploader(false);
    setError(null);
    
    try {
      await apiService.uploadDocument(file);
      // After successful upload, search for the newly uploaded file
      const searchResults = await apiService.searchDocuments(file.name.split('.')[0]);
      setResults(searchResults);
      setShowResults(true);
    } catch (err) {
      console.error('File upload error:', err);
      setError('Error uploading file. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setShowResults(false);
    setResults([]);
    setQuery('');
    setError(null);
  };

  const toggleUploader = () => {
    setShowUploader(!showUploader);
    if (showResults) {
      setShowResults(false);
    }
    setError(null);
  };

  // Animation variants for staggered animations
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { 
        staggerChildren: 0.1,
        delayChildren: 0.3
      }
    }
  };
  
  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { type: "spring", stiffness: 300, damping: 30 }
    }
  };

  return (
    <PageTransition className="min-h-screen pt-16 pb-8 relative">
      {/* Background Lights - positioned to affect the header/navbar */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {/* Top light positioned higher to affect the header */}
        <BackgroundLight position="top" color="primary" intensity="high" />
        <BackgroundLight position="center" color="accent" intensity="high" />
      </div>
      
      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={false}
          animate={{ y: showResults ? 0 : 100 }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          className="max-w-4xl mx-auto"
        >
          {/* API Status Indicator */}
          {apiAvailable === false && (
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-4 p-3 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center text-red-700 dark:text-red-300"
            >
              <AlertCircle size={18} className="mr-2" />
              <span>API is unavailable. Please check your backend server.</span>
            </motion.div>
          )}
          
          {/* Logo and Title */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center mb-8"
          >
            <motion.div 
              className="inline-flex items-center justify-center p-3 bg-primary-100 dark:bg-primary-900/30 rounded-xl mb-4"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Search size={32} className="text-primary-600 dark:text-primary-400" />
            </motion.div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              Al Baheth
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Search documents intelligently
            </p>
          </motion.div>

          {/* Search Bar */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            whileHover={{ boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)" }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-soft p-6"
          >
            <SearchBar
              onSearch={handleSearch}
              onUpload={toggleUploader}
              placeholder="Search documents..."
              autoFocus
            />
            
            <AnimatePresence>
              {showUploader && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mt-4 overflow-hidden"
                >
                  <FileUploader onFileSelect={handleFileSelect} />
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          {/* Error Message */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="mt-4 p-3 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center text-red-700 dark:text-red-300"
              >
                <AlertCircle size={18} className="mr-2" />
                <span>{error}</span>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results Area */}
          <AnimatePresence>
            {(showResults || isLoading) && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                className="mt-6 bg-white dark:bg-gray-800 rounded-2xl shadow-soft"
              >
                {/* Results Header */}
                <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                  <div className="flex items-center">
                    <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                      {isLoading ? 'Searching...' : `${results.length} results found`}
                    </h2>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => navigate('/results', { state: { results, query } })}
                      className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                      aria-label="View full results"
                    >
                      <ExternalLink size={20} className="text-gray-600 dark:text-gray-400" />
                    </motion.button>
                    
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={clearResults}
                      className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                      aria-label="Clear results"
                    >
                      <X size={20} className="text-gray-600 dark:text-gray-400" />
                    </motion.button>
                  </div>
                </div>

                {/* Results Content */}
                <div className="p-4">
                  {isLoading ? (
                    <div className="flex items-center justify-center py-12">
                      <motion.div
                        animate={{ 
                          rotate: 360,
                          transition: { 
                            duration: 1,
                            repeat: Infinity,
                            ease: "linear"
                          }
                        }}
                      >
                        <Loader size={32} className="text-primary-600 dark:text-primary-400" />
                      </motion.div>
                    </div>
                  ) : (
                    <motion.div 
                      className="space-y-4"
                      variants={containerVariants}
                      initial="hidden"
                      animate="visible"
                    >
                      {results.length > 0 ? (
                        results.map((result, index) => {
                          const fileType = getFileTypeFromExtension(result.title);
                          return (
                            <motion.div
                              key={result.id}
                              variants={itemVariants}
                              whileHover={{ 
                                scale: 1.02,
                                boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)"
                              }}
                              className="flex items-start space-x-4 p-4 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                            >
                              <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg">
                                <FileTypeIcon fileType={fileType} size={24} />
                              </div>
                              
                              <div className="flex-1 min-w-0">
                                <h3 className="font-medium text-gray-900 dark:text-white mb-1">
                                  {result.title}
                                </h3>
                                <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
                                  {result.excerpt}
                                </p>
                                <div className="mt-2 flex items-center text-xs text-gray-500 dark:text-gray-400">
                                  <span>{result.lastModified}</span>
                                  <span className="mx-2">•</span>
                                  <span>{result.size}</span>
                                  <span className="mx-2">•</span>
                                  <span>{result.matchCount} matches</span>
                                </div>
                              </div>
                            </motion.div>
                          );
                        })
                      ) : (
                        <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                          No results found for "{query}". Try a different search term.
                        </div>
                      )}
                    </motion.div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </PageTransition>
  );
};

export default HomePage;