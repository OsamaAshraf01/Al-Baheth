import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { motion } from 'framer-motion';
import { useTheme } from '../context/ThemeContext';

const ThemeToggle: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  
  return (
    <motion.button
      onClick={toggleTheme}
      className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors duration-200"
      aria-label={theme === 'dark' ? "Switch to light mode" : "Switch to dark mode"}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      layout
    >
      {theme === 'dark' ? (
        <motion.div
          initial={{ rotate: -180, opacity: 0 }}
          animate={{ rotate: 0, opacity: 1 }}
          exit={{ rotate: 180, opacity: 0 }}
          transition={{ duration: 0.5, type: "spring" }}
          key="sun-icon"
        >
          <Sun size={20} className="text-yellow-400" />
        </motion.div>
      ) : (
        <motion.div
          initial={{ rotate: 180, opacity: 0 }}
          animate={{ rotate: 0, opacity: 1 }}
          exit={{ rotate: -180, opacity: 0 }}
          transition={{ duration: 0.5, type: "spring" }}
          key="moon-icon"
        >
          <Moon size={20} className="text-primary-600" />
        </motion.div>
      )}
    </motion.button>
  );
};

export default ThemeToggle;