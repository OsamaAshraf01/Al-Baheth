import React, { useState, useEffect } from 'react';

interface SearchTypewriterProps {
  phrases: string[];
  typingSpeed?: number;
  deletingSpeed?: number;
  delayBetweenPhrases?: number;
}

const SearchTypewriter: React.FC<SearchTypewriterProps> = ({
  phrases,
  typingSpeed = 100,
  deletingSpeed = 50,
  delayBetweenPhrases = 2000,
}) => {
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0);
  const [currentText, setCurrentText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    let timeout: NodeJS.Timeout;
    const currentPhrase = phrases[currentPhraseIndex];

    if (isDeleting) {
      if (currentText === '') {
        setIsDeleting(false);
        setCurrentPhraseIndex((prevIndex) =>
          prevIndex === phrases.length - 1 ? 0 : prevIndex + 1
        );
        timeout = setTimeout(() => {}, delayBetweenPhrases);
      } else {
        timeout = setTimeout(() => {
          setCurrentText(currentPhrase.substring(0, currentText.length - 1));
        }, deletingSpeed);
      }
    } else {
      if (currentText === currentPhrase) {
        timeout = setTimeout(() => {
          setIsDeleting(true);
        }, delayBetweenPhrases);
      } else {
        timeout = setTimeout(() => {
          setCurrentText(currentPhrase.substring(0, currentText.length + 1));
        }, typingSpeed);
      }
    }

    return () => clearTimeout(timeout);
  }, [currentText, currentPhraseIndex, isDeleting, phrases, typingSpeed, deletingSpeed, delayBetweenPhrases]);

  return (
    <span className="inline-block">
      {currentText}
      <span className="animate-pulse-slow">|</span>
    </span>
  );
};

export default SearchTypewriter;