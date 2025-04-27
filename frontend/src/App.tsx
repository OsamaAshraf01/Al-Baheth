import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';

// AnimatePresence requires the location from useLocation
// which is only available inside a router context
const AnimatedRoutes = () => {
  const location = useLocation();
  
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<HomePage />} />
        <Route path="/results" element={<ResultsPage />} />
      </Routes>
    </AnimatePresence>
  );
};

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
          <Header />
          <AnimatedRoutes />
        </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;