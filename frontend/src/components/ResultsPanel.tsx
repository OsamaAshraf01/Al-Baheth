import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Maximize2, Minimize2, ArrowLeft, Search } from 'lucide-react';
import { SearchResult } from '../types';
import ResultItem from './ResultItem';

interface ResultsPanelProps {
  results: SearchResult[];
  isOpen: boolean;
  isFullScreen: boolean;
  onClose: () => void;
  onToggleFullScreen: () => void;
  onSelectResult: (id: string) => void;
  searchQuery: string;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({
  results,
  isOpen,
  isFullScreen,
  onClose,
  onToggleFullScreen,
  onSelectResult,
  searchQuery,
}) => {
  // Animation variants
  const panelVariants = {
    hidden: { x: '100%', opacity: 0 },
    visible: { 
      x: 0, 
      opacity: 1,
      transition: { 
        type: 'spring', 
        damping: 25, 
        stiffness: 200,
        when: "beforeChildren",
        staggerChildren: 0.07
      }
    },
    exit: { 
      x: '100%', 
      opacity: 0,
      transition: { 
        type: 'spring', 
        damping: 25, 
        stiffness: 200 
      }
    }
  };

  const fullscreenVariants = {
    compact: { 
      width: 'calc(100% - 4rem)', 
      height: 'calc(100% - 8rem)', 
      right: '2rem', 
      bottom: '2rem', 
      top: '6rem',
      borderRadius: '0.75rem',
      transition: { type: 'spring', damping: 30, stiffness: 300 }
    },
    fullscreen: { 
      width: '100%', 
      height: '100%', 
      right: 0, 
      bottom: 0, 
      top: 0,
      borderRadius: 0,
      transition: { type: 'spring', damping: 30, stiffness: 300 }
    }
  };

  const headerVariants = {
    hidden: { opacity: 0, y: -20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        delay: 0.2, 
        duration: 0.4, 
        type: "spring", 
        stiffness: 500, 
        damping: 30 
      }
    }
  };

  const buttonVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { 
        delay: 0.3, 
        duration: 0.3, 
        type: "spring" 
      }
    },
    hover: { 
      scale: 1.1,
      transition: { 
        type: "spring", 
        stiffness: 500, 
        damping: 20 
      }
    },
    tap: { scale: 0.9 }
  };

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

  // If panel is closed, don't render anything
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          key="results-panel"
          initial="hidden"
          animate="visible"
          exit="exit"
          variants={panelVariants}
          className="fixed z-30 bg-white dark:bg-gray-900 shadow-xl overflow-hidden flex flex-col"
          animate={isFullScreen ? 'fullscreen' : 'compact'}
          variants={fullscreenVariants}
        >
          {/* Panel header */}
          <motion.div 
            className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800"
            variants={headerVariants}
          >
            <div className="flex items-center">
              {isFullScreen && (
                <motion.button 
                  onClick={onClose}
                  className="mr-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                  variants={buttonVariants}
                  whileHover="hover"
                  whileTap="tap"
                >
                  <ArrowLeft size={20} className="text-gray-600 dark:text-gray-300" />
                </motion.button>
              )}
              <motion.h2 
                className="text-xl font-medium"
                initial={{ opacity: 0 }}
                animate={{ 
                  opacity: 1,
                  transition: { delay: 0.3 }
                }}
              >
                Results for <motion.span 
                  className="text-primary-600 dark:text-primary-400"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ 
                    opacity: 1, 
                    scale: 1,
                    transition: { 
                      delay: 0.5,
                      type: "spring"
                    }
                  }}
                >"{searchQuery}"</motion.span>
              </motion.h2>
            </div>
            
            <div className="flex space-x-2">
              <motion.button
                onClick={onToggleFullScreen}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                aria-label={isFullScreen ? "Minimize" : "Maximize"}
                variants={buttonVariants}
                whileHover="hover"
                whileTap="tap"
              >
                {isFullScreen ? (
                  <Minimize2 size={20} className="text-gray-600 dark:text-gray-300" />
                ) : (
                  <Maximize2 size={20} className="text-gray-600 dark:text-gray-300" />
                )}
              </motion.button>
              
              {!isFullScreen && (
                <motion.button
                  onClick={onClose}
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                  aria-label="Close results"
                  variants={buttonVariants}
                  whileHover="hover"
                  whileTap="tap"
                >
                  <X size={20} className="text-gray-600 dark:text-gray-300" />
                </motion.button>
              )}
            </div>
          </motion.div>
          
          {/* Results content */}
          <motion.div 
            className="flex-1 overflow-y-auto p-4"
            initial={{ opacity: 0 }}
            animate={{ 
              opacity: 1,
              transition: { delay: 0.2 }
            }}
          >
            {results.length > 0 ? (
              <motion.div 
                className="space-y-4"
                variants={containerVariants}
                initial="hidden"
                animate="visible"
              >
                {results.map((result, index) => (
                  <ResultItem 
                    key={result.id} 
                    result={result} 
                    onClick={() => {}} 
                    delay={index}
                  />
                ))}
              </motion.div>
            ) : (
              <motion.div 
                className="flex flex-col items-center justify-center h-full text-center"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ 
                  opacity: 1, 
                  scale: 1,
                  transition: { 
                    delay: 0.3,
                    type: "spring",
                    stiffness: 300,
                    damping: 30
                  }
                }}
              >
                <motion.div 
                  className="rounded-full bg-gray-100 dark:bg-gray-800 p-4 mb-4"
                  initial={{ scale: 0.7 }}
                  animate={{ 
                    scale: 1,
                    transition: { 
                      delay: 0.4,
                      type: "spring",
                      stiffness: 500
                    }
                  }}
                >
                  <Search size={32} className="text-gray-400" />
                </motion.div>
                <motion.h3 
                  className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ 
                    opacity: 1, 
                    y: 0,
                    transition: { delay: 0.5 }
                  }}
                >
                  No results found
                </motion.h3>
                <motion.p 
                  className="text-gray-500 dark:text-gray-400 max-w-md"
                  initial={{ opacity: 0 }}
                  animate={{ 
                    opacity: 1,
                    transition: { delay: 0.6 }
                  }}
                >
                  We couldn't find any documents matching your search query. 
                  Try using different keywords or uploading a document.
                </motion.p>
              </motion.div>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default ResultsPanel;