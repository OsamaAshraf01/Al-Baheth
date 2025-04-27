import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, AlertCircle, Check } from 'lucide-react';
import { UploadedFile } from '../types';
import { formatFileSize } from '../utils/fileUtils';
import { motion, AnimatePresence } from 'framer-motion';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onFileSelect }) => {
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Define accepted file types
  const acceptedFileTypes = {
    'application/pdf': ['.pdf'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'application/msword': ['.doc'],
    'text/plain': ['.txt'],
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
    'application/vnd.ms-powerpoint': ['.ppt'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    'application/vnd.ms-excel': ['.xls'],
  };

  const onDrop = useCallback((acceptedFiles: File[], fileRejections: any[]) => {
    // Reset previous states
    setErrorMessage(null);
    setUploadStatus('idle');
    
    // Handle file rejections
    if (fileRejections.length > 0) {
      const rejection = fileRejections[0];
      if (rejection.errors[0].code === 'file-too-large') {
        setErrorMessage('File is too large. Maximum size is 5MB.');
      } else if (rejection.errors[0].code === 'file-invalid-type') {
        setErrorMessage('File type not supported. Please upload PDF, DOCX, TXT, PPT, or XLS files.');
      } else {
        setErrorMessage('Invalid file. Please try again.');
      }
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      
      // Create the file preview
      setUploadedFile({
        id: Math.random().toString(36).substring(2, 9),
        name: file.name,
        size: file.size,
        type: file.type
      });
      
      setUploadStatus('uploading');
      
      // Trigger the parent component's upload handler
      try {
        onFileSelect(file);
        setUploadStatus('success');
      } catch (error) {
        console.error('Upload error:', error);
        setUploadStatus('error');
        setErrorMessage('Error uploading file. Please try again.');
      }
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({ 
    onDrop,
    multiple: false,
    noClick: true,
    maxSize: 5 * 1024 * 1024, // 5MB max size
    accept: acceptedFileTypes
  });

  const removeFile = () => {
    setUploadedFile(null);
    setUploadStatus('idle');
    setErrorMessage(null);
  };

  return (
    <div className="w-full">
      {/* Error message */}
      <AnimatePresence>
        {errorMessage && (
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-3 p-2 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center text-red-700 dark:text-red-300 text-sm"
          >
            <AlertCircle size={16} className="mr-2 flex-shrink-0" />
            <span>{errorMessage}</span>
          </motion.div>
        )}
      </AnimatePresence>
    
      {!uploadedFile ? (
        <div 
          {...getRootProps()} 
          className={`border-2 border-dashed rounded-xl p-6 text-center transition-all duration-200
            ${isDragActive 
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
              : 'border-gray-300 dark:border-gray-700 hover:border-primary-400 dark:hover:border-primary-500'
            }`}
        >
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center justify-center space-y-3">
            <Upload 
              size={32} 
              className={`${isDragActive ? 'text-primary-500' : 'text-gray-400'}`} 
            />
            
            <div>
              {isDragActive ? (
                <p className="text-primary-500 font-medium">Drop your file here</p>
              ) : (
                <>
                  <p className="text-gray-600 dark:text-gray-300 mb-2">
                    Drag & drop file or <button type="button" onClick={open} className="text-primary-600 dark:text-primary-400 font-medium hover:text-primary-700 dark:hover:text-primary-300">browse</button>
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Supported formats: PDF, DOCX, TXT, PPT, XLS (Max: 5MB)
                  </p>
                </>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="animate-fade-in border rounded-xl p-4 bg-white dark:bg-gray-800 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-lg ${
                uploadStatus === 'success' 
                  ? 'bg-green-100 dark:bg-green-900/30' 
                  : uploadStatus === 'error'
                    ? 'bg-red-100 dark:bg-red-900/30'
                    : 'bg-primary-100 dark:bg-primary-900/30'
              }`}>
                {uploadStatus === 'success' ? (
                  <Check size={24} className="text-green-600 dark:text-green-400" />
                ) : uploadStatus === 'error' ? (
                  <AlertCircle size={24} className="text-red-600 dark:text-red-400" />
                ) : (
                  <File size={24} className="text-primary-600 dark:text-primary-400" />
                )}
              </div>
              
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                  {uploadedFile.name}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  {formatFileSize(uploadedFile.size)}
                  {uploadStatus === 'uploading' && (
                    <span className="ml-2 text-primary-500 dark:text-primary-400">Uploading...</span>
                  )}
                  {uploadStatus === 'success' && (
                    <span className="ml-2 text-green-500 dark:text-green-400">Upload complete</span>
                  )}
                  {uploadStatus === 'error' && (
                    <span className="ml-2 text-red-500 dark:text-red-400">Upload failed</span>
                  )}
                </p>
              </div>
            </div>
            
            <button 
              onClick={removeFile}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
              aria-label="Remove file"
            >
              <X size={18} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUploader;