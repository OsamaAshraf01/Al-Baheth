import React from 'react';
import {motion} from 'framer-motion';
import {Calendar, Search} from 'lucide-react';
import {SearchResult} from '../types';
import FileTypeIcon from './FileTypeIcon';
import {getFileTypeFromExtension} from '../utils/fileUtils';

interface ResultItemProps {
  result: SearchResult;
  onClick: (id: string) => void;
  delay?: number;
}

const ResultItem: React.FC<ResultItemProps> = ({ result, onClick, delay = 0 }) => {
  const fileType = getFileTypeFromExtension(result.title);
  
  // Enhanced animation variants
  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        type: "spring", 
        stiffness: 300, 
        damping: 30, 
        delay: delay * 0.1 
      }
    },
    hover: { 
      scale: 1.02, 
      boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
      transition: { 
        type: "spring", 
        stiffness: 400, 
        damping: 25 
      }
    },
    tap: { scale: 0.98 }
  };
  
  const iconVariants = {
    hidden: { scale: 0.8, opacity: 0 },
    visible: { 
      scale: 1, 
      opacity: 1,
      transition: { 
        delay: (delay * 0.1) + 0.1,
        type: "spring",
        stiffness: 500
      }
    }
  };
  
  const contentVariants = {
    hidden: { opacity: 0, x: -10 },
    visible: { 
      opacity: 1, 
      x: 0,
      transition: { 
        delay: (delay * 0.1) + 0.2,
        type: "spring",
        stiffness: 500,
        damping: 30
      }
    }
  };
  
  return (
    <motion.div
      variants={itemVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
      whileTap="tap"
      className="card hover-card cursor-pointer"
      onClick={() => onClick(result.id)}
      layout
    >
      <div className="flex items-start gap-4">
        <motion.div 
          className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg"
          variants={iconVariants}
        >
          <FileTypeIcon fileType={fileType} size={24} />
        </motion.div>
        
        <motion.div 
          className="flex-1 min-w-0"
          variants={contentVariants}
        >
          <h3 className="text-lg font-medium text-gray-900 dark:text-white truncate">
            {result.title}
          </h3>
          
          <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mt-1">
            <div className="flex items-center">
              <Calendar size={14} className="mr-1" />
              {result.lastModified}
            </div>
            <div className="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-600"></div>
            <div>{result.size}</div>
            <div className="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-600"></div>
            <div className="flex items-center">
              <Search size={14} className="mr-1" />
              {result.matchCount} matches
            </div>
          </div>
          
          <motion.p 
            className="mt-2 text-sm text-gray-600 dark:text-gray-300 line-clamp-2"
            initial={{ opacity: 0 }}
            animate={{ 
              opacity: 1,
              transition: { delay: (delay * 0.1) + 0.3 }
            }}
          >
            {result.excerpt}
          </motion.p>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default ResultItem;