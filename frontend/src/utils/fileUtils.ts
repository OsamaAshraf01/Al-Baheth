import { FileType } from '../types';

export const getFileTypeFromExtension = (filename: string): FileType => {
  const extension = filename.split('.').pop()?.toLowerCase() || '';
  
  switch (extension) {
    case 'pdf':
      return 'pdf';
    case 'doc':
    case 'docx':
      return 'doc';
    case 'txt':
      return 'txt';
    case 'ppt':
    case 'pptx':
      return 'ppt';
    case 'xls':
    case 'xlsx':
      return 'xls';
    case 'csv':
      return 'csv';
    default:
      return 'unknown';
  }
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const mockSearchResults = [
  {
    id: '1',
    title: 'Annual Report 2024.pdf',
    fileType: 'pdf',
    excerpt: 'The company showed significant growth in Q3, with a 25% increase in revenue compared to last year...',
    matchCount: 12,
    lastModified: '2024-05-10',
    size: '4.2 MB'
  },
  {
    id: '2',
    title: 'Project Requirements.docx',
    fileType: 'doc',
    excerpt: 'The new search functionality must include document previews and support multiple file formats...',
    matchCount: 8,
    lastModified: '2024-05-15',
    size: '257 KB'
  },
  {
    id: '3',
    title: 'Conference Notes.txt',
    fileType: 'txt',
    excerpt: 'The keynote speaker discussed the future of AI in document search and retrieval systems...',
    matchCount: 5,
    lastModified: '2024-05-01',
    size: '45 KB'
  },
  {
    id: '4',
    title: 'Quarterly Presentation.pptx',
    fileType: 'ppt',
    excerpt: 'Slide 15 contains the exact metrics you were searching for regarding user engagement...',
    matchCount: 3,
    lastModified: '2024-04-28',
    size: '3.8 MB'
  },
  {
    id: '5',
    title: 'Financial Data.xlsx',
    fileType: 'xls',
    excerpt: 'The spreadsheet contains detailed financial projections for the next fiscal year...',
    matchCount: 10,
    lastModified: '2024-05-12',
    size: '1.2 MB'
  }
];