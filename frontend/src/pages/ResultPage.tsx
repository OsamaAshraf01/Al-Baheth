import React, {useEffect, useState} from 'react';
import {useNavigate, useParams, useSearchParams} from 'react-router-dom';
import {motion} from 'framer-motion';
import {ArrowLeft, Download, ExternalLink, Printer, Share2} from 'lucide-react';
import SearchBar from '../components/SearchBar';
import FileTypeIcon from '../components/FileTypeIcon';
import PageTransition from '../components/PageTransition';
import {getFileTypeFromExtension, mockSearchResults} from '../utils/fileUtils';

const ResultPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const query = searchParams.get('query') || '';
  const navigate = useNavigate();
  
  const [result, setResult] = useState(
    mockSearchResults.find(r => r.id === id) || mockSearchResults[0]
  );

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading document
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);
    
    return () => clearTimeout(timer);
  }, [id]);

  const fileType = getFileTypeFromExtension(result.title);

  const handleSearch = (searchQuery: string) => {
    // Navigate back to home with search results
    navigate(`/?query=${encodeURIComponent(searchQuery)}`);
  };

  const handleGoBack = () => {
    navigate(-1);
  };
  
  // Animation variants for buttons
  const buttonVariants = {
    initial: { opacity: 0, y: 20 },
    animate: (index: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: 0.5 + (index * 0.1),
        duration: 0.3
      }
    }),
    hover: { 
      scale: 1.05,
      boxShadow: "0 5px 15px rgba(0, 0, 0, 0.1)"
    },
    tap: { scale: 0.95 }
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
                <span>Back to results</span>
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
          
          {/* Document header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="bg-white dark:bg-gray-800 shadow-soft rounded-xl p-6 mb-6"
          >
            <div className="flex items-start gap-4">
              <motion.div 
                className="p-4 bg-gray-100 dark:bg-gray-700 rounded-lg"
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.2, type: "spring" }}
              >
                <FileTypeIcon fileType={fileType} size={36} />
              </motion.div>
              
              <div className="flex-1">
                <motion.h1 
                  className="text-2xl font-medium text-gray-900 dark:text-white mb-2"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  {result.title}
                </motion.h1>
                
                <motion.div 
                  className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-gray-500 dark:text-gray-400"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  <div>Last modified: {result.lastModified}</div>
                  <div className="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-600"></div>
                  <div>{result.size}</div>
                  <div className="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-600"></div>
                  <div>{result.matchCount} search matches</div>
                </motion.div>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-3 mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
              <motion.button 
                className="btn btn-secondary flex items-center space-x-2"
                variants={buttonVariants}
                initial="initial"
                animate="animate"
                whileHover="hover"
                whileTap="tap"
                custom={0}
              >
                <Download size={18} />
                <span>Download</span>
              </motion.button>
              
              <motion.button 
                className="btn btn-secondary flex items-center space-x-2"
                variants={buttonVariants}
                initial="initial"
                animate="animate"
                whileHover="hover"
                whileTap="tap"
                custom={1}
              >
                <Share2 size={18} />
                <span>Share</span>
              </motion.button>
              
              <motion.button 
                className="btn btn-secondary flex items-center space-x-2"
                variants={buttonVariants}
                initial="initial"
                animate="animate"
                whileHover="hover"
                whileTap="tap"
                custom={2}
              >
                <Printer size={18} />
                <span>Print</span>
              </motion.button>
              
              <motion.button 
                className="btn btn-secondary flex items-center space-x-2"
                variants={buttonVariants}
                initial="initial"
                animate="animate"
                whileHover="hover"
                whileTap="tap"
                custom={3}
              >
                <ExternalLink size={18} />
                <span>Open</span>
              </motion.button>
            </div>
          </motion.div>
          
          {/* Document content */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white dark:bg-gray-800 shadow-soft rounded-xl p-6"
          >
            {loading ? (
              <div className="animate-pulse space-y-4">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
              </div>
            ) : (
              <motion.div 
                className="prose dark:prose-invert max-w-none"
                initial="hidden"
                animate="visible"
                variants={{
                  hidden: { opacity: 0 },
                  visible: {
                    opacity: 1,
                    transition: {
                      staggerChildren: 0.1,
                      delayChildren: 0.2
                    }
                  }
                }}
              >
                <motion.h2 
                  variants={{
                    hidden: { opacity: 0, y: 10 },
                    visible: { opacity: 1, y: 0 }
                  }}
                >Document Preview</motion.h2>
                
                <motion.p 
                  className="bg-yellow-50 dark:bg-yellow-900/30 p-2 border-l-4 border-yellow-500 text-gray-800 dark:text-gray-200 my-4"
                  variants={{
                    hidden: { opacity: 0, x: -20 },
                    visible: { opacity: 1, x: 0 }
                  }}
                >
                  <strong>Search match:</strong> {result.excerpt}
                </motion.p>
                
                <motion.p
                  variants={{
                    hidden: { opacity: 0, y: 10 },
                    visible: { opacity: 1, y: 0 }
                  }}
                >Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, vel ultricies nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, vel ultricies nisl nisl sit amet nisl.</motion.p>
                
                <motion.p
                  variants={{
                    hidden: { opacity: 0, y: 10 },
                    visible: { opacity: 1, y: 0 }
                  }}
                >Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, vel ultricies nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, vel ultricies nisl nisl sit amet nisl.</motion.p>
                
                <motion.h3
                  variants={{
                    hidden: { opacity: 0, y: 10 },
                    visible: { opacity: 1, y: 0 }
                  }}
                >Section 1</motion.h3>
                
                <motion.p
                  variants={{
                    hidden: { opacity: 0, y: 10 },
                    visible: { opacity: 1, y: 0 }
                  }}
                >Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, vel ultricies nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, vel ultricies nisl nisl sit amet nisl.</motion.p>
                
                <motion.ul
                  variants={{
                    hidden: { opacity: 0 },
                    visible: { opacity: 1 }
                  }}
                >
                  <motion.li
                    variants={{
                      hidden: { opacity: 0, x: -10 },
                      visible: { opacity: 1, x: 0 }
                    }}
                  >Lorem ipsum dolor sit amet</motion.li>
                  <motion.li
                    variants={{
                      hidden: { opacity: 0, x: -10 },
                      visible: { opacity: 1, x: 0 }
                    }}
                  >Consectetur adipiscing elit</motion.li>
                  <motion.li
                    variants={{
                      hidden: { opacity: 0, x: -10 },
                      visible: { opacity: 1, x: 0 }
                    }}
                  >Sed do eiusmod tempor incididunt</motion.li>
                </motion.ul>
                
                <motion.p 
                  className="bg-yellow-50 dark:bg-yellow-900/30 p-2 border-l-4 border-yellow-500 text-gray-800 dark:text-gray-200 my-4"
                  variants={{
                    hidden: { opacity: 0, x: -20 },
                    visible: { opacity: 1, x: 0 }
                  }}
                >
                  <strong>Search match:</strong> Another relevant excerpt from the document matching your search query.
                </motion.p>
                
                <motion.p
                  variants={{
                    hidden: { opacity: 0, y: 10 },
                    visible: { opacity: 1, y: 0 }
                  }}
                >Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, vel ultricies nisl nisl sit amet nisl. Sed euismod, nisl vel ultricies lacinia, nisl nisl aliquam nisl, vel ultricies nisl nisl sit amet nisl.</motion.p>
              </motion.div>
            )}
          </motion.div>
        </div>
      </div>
    </PageTransition>
  );
};

export default ResultPage;