import React from 'react';
import {Search} from 'lucide-react';
import {motion} from 'framer-motion';
import ThemeToggle from './ThemeToggle';
import {Link} from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <motion.header 
      className="fixed top-0 left-0 right-0 z-20 bg-white/20 dark:bg-gray-900/20 backdrop-blur-sm"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <motion.div 
            className="p-1.5 bg-primary-600 rounded-lg"
            whileHover={{ scale: 1.1, rotate: 5 }}
            whileTap={{ scale: 0.9 }}
          >
            <Search size={20} className="text-white" />
          </motion.div>
          <motion.span 
            className="text-xl font-semibold text-gray-900 dark:text-white"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            Al Baheth
          </motion.span>
        </Link>
        
        <motion.div 
          className="flex items-center space-x-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <ThemeToggle />
        </motion.div>
      </div>
      <motion.div 
        className="h-px bg-gradient-to-r from-transparent via-primary-500/30 to-transparent"
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
      />
    </motion.header>
  );
};

export default Header;