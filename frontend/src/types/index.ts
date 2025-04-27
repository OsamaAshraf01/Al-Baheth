export interface SearchResult {
  id: string;
  title: string;
  fileType: string;
  excerpt: string;
  matchCount: number;
  lastModified: string;
  size: string;
}

export type FileType = 'pdf' | 'doc' | 'docx' | 'txt' | 'ppt' | 'pptx' | 'xls' | 'xlsx' | 'csv' | 'unknown';

export interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
}