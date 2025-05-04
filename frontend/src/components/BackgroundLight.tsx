// filepath: d:\University\Year 2\Semester 2\Information Retrieval\Project\frontend\project\src\components\BackgroundLight.tsx
import React from 'react';
import {motion} from 'framer-motion';

interface BackgroundLightProps {
  color?: 'primary' | 'accent';
  intensity?: 'low' | 'medium' | 'high';
  position?: 'top' | 'center' | 'bottom';
  animated?: boolean;
}

const BackgroundLight: React.FC<BackgroundLightProps> = ({
  color = 'primary',
  intensity = 'medium',
  position = 'top',
  animated = true,
}) => {
  // Get the color values based on the theme
  const getColorValue = () => {
    if (color === 'primary') {
      return {
        light: 'rgba(99, 102, 241, 0.4)', // primary-500 with reduced opacity
        dark: 'rgba(79, 70, 229, 0.4)', // primary-600 with reduced opacity
      };
    } else {
      return {
        light: 'rgba(16, 185, 129, 0.4)', // accent-500 with reduced opacity
        dark: 'rgba(5, 150, 105, 0.4)', // accent-600 with reduced opacity
      };
    }
  };

  // Configure size based on intensity
  const getSize = () => {
    switch (intensity) {
      case 'low':
        return { width: '500px', height: '500px' };
      case 'medium':
        return { width: '800px', height: '800px' };
      case 'high':
        return { width: '1200px', height: '1200px' };
      default:
        return { width: '800px', height: '800px' };
    }
  };

  // Configure position
  const getPosition = () => {
    switch (position) {
      case 'top':
        return { top: '-15%', left: '50%', transform: 'translateX(-50%)' };
      case 'center':
        return { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' };
      case 'bottom':
        return { bottom: '-25%', left: '50%', transform: 'translateX(-50%)' };
      default:
        return { top: '0', left: '50%', transform: 'translateX(-50%)' };
    }
  };

  const colors = getColorValue();
  const size = getSize();
  const pos = getPosition();

  // Animation variants for the blob
  const blobVariants = {
    initial: { scale: 0.8, opacity: 0.4 },
    animate: {
      scale: [0.8, 1.1, 0.9, 1.05, 0.95, 1],
      opacity: [0.4, 0.6, 0.5, 0.55, 0.6, 0.5],
      transition: {
        duration: 15,
        ease: "easeInOut",
        repeat: Infinity,
        repeatType: "reverse" as const,
      }
    }
  };

  const lightStyle = {
    position: 'absolute' as const,
    ...pos,
    width: size.width,
    height: size.height,
    borderRadius: '50%',
    background: `radial-gradient(circle, ${colors.light} 0%, rgba(255,255,255,0) 70%)`,
    filter: 'blur(60px)',
    zIndex: 0,
    pointerEvents: 'none' as const,
  };

  const darkStyle = {
    position: 'absolute' as const,
    ...pos,
    width: size.width,
    height: size.height,
    borderRadius: '50%',
    background: `radial-gradient(circle, ${colors.dark} 0%, rgba(0,0,0,0) 70%)`,
    filter: 'blur(60px)',
    zIndex: 0,
    pointerEvents: 'none' as const,
  };

  // Use a system that works in both light and dark modes
  return (
    <>
      <motion.div
        className="light-mode-only"
        style={lightStyle}
        initial="initial"
        animate={animated ? "animate" : "initial"}
        variants={blobVariants}
      />
      <motion.div
        className="dark-mode-only"
        style={darkStyle}
        initial="initial"
        animate={animated ? "animate" : "initial"}
        variants={blobVariants}
      />
    </>
  );
};

export default BackgroundLight;