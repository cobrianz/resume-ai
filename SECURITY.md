# Resume AI - Security & Data Handling

## Implemented Security Measures

### 1. CORS Configuration
- Added CORS middleware to control cross-origin requests
- Currently set to allow all origins (development mode)
- **Production**: Update `allow_origins` to specific domains

### 2. File Upload Security
- **File Type Validation**: Only PDF and DOCX allowed
- **Size Limit**: 10MB max upload size (configurable in `config.py`)
- **Temporary Storage**: Files saved with UUID filenames to prevent collisions
- **Auto-Cleanup**: Files deleted immediately after processing (in `finally` block)

### 3. Data Privacy
- **No Persistent Storage**: Resumes are NOT stored in database
- **In-Memory Processing**: All data processed in memory and discarded
- **No Training**: User data is never used for model training

### 4. Request Validation
- Pydantic models validate all input data
- FastAPI automatic validation prevents injection attacks
- Structured error responses (no sensitive info leakage)

## Recommendations for Production

1. **Environment Variables**: Move sensitive config to `.env`
2. **Rate Limiting**: Add rate limiting middleware (e.g., `slowapi`)
3. **Authentication**: Implement JWT tokens if user accounts needed
4. **HTTPS**: Deploy behind reverse proxy with SSL/TLS
5. **Logging**: Sanitize logs to remove PII
6. **Input Sanitization**: Additional validation for text inputs
