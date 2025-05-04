from enum import Enum


class ResponseEnum(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_uploaded_successfully"
    FILE_UPLOAD_FAILED = "file_uploading_failed"
    FILE_ALREADY_EXISTS = "file_already_exists"

    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILED = "processing_failed"
    FILE_NOT_FOUND = "file_not_found"

    INVALID_ID = "invalid_file_id"

    INVALID_QUERY = "invalid_query"
    SEARCH_ERROR = "search_error"
    SEARCH_SUCCESS = "search_success"
