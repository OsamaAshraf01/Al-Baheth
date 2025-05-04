import React from 'react';
import {File as FilePpt, FileCog, FileSpreadsheet, FileTerminal, FileText, FileType} from 'lucide-react';
import {FileType as FileTypeEnum} from '../types';

interface FileTypeIconProps {
  fileType: FileTypeEnum;
  size?: number;
  className?: string;
}

const FileTypeIcon: React.FC<FileTypeIconProps> = ({ 
  fileType, 
  size = 24, 
  className = ''
}) => {
  const getIconByType = () => {
    switch (fileType) {
      case 'pdf':
        return <FileText size={size} className={`text-red-500 ${className}`} />;
      case 'doc':
        return <FileType size={size} className={`text-blue-500 ${className}`} />;
      case 'txt':
        return <FileTerminal size={size} className={`text-gray-500 ${className}`} />;
      case 'ppt':
        return <FilePpt size={size} className={`text-orange-500 ${className}`} />;
      case 'xls':
      case 'csv':
        return <FileSpreadsheet size={size} className={`text-green-500 ${className}`} />;
      default:
        return <FileCog size={size} className={`text-gray-400 ${className}`} />;
    }
  };

  return getIconByType();
};

export default FileTypeIcon;