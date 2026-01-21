# Resume AI - Test Suite

## Test Organization

### Unit Tests
- `test_parsing.py` - Resume parser edge cases
- `test_matching.py` - Matching engine scenarios
- `test_tailoring.py` - Tailoring service logic

### Integration Tests
- `test_integration.py` - End-to-end API flow
- `test_job.py` - Job analysis endpoint
- `test_upload.py` - Resume upload endpoint

### Edge Case Tests
- `test_edge_cases.py` - Malformed files, empty inputs, etc.

## Running Tests

```bash
# Run all tests
.\venv\Scripts\python -m pytest tests/

# Run specific test
.\venv\Scripts\python tests/test_integration.py

# Run with coverage (if pytest-cov installed)
.\venv\Scripts\python -m pytest tests/ --cov=app
```

## Test Coverage

Current test files:
- ✅ Resume parsing (PDF/DOCX extraction)
- ✅ Job analysis (skill extraction)
- ✅ Embedding & retrieval
- ✅ Matching engine (perfect vs irrelevant)
- ✅ Tailoring suggestions
- ✅ End-to-end integration

## Quality Metrics

- All core endpoints tested
- Edge cases covered (empty files, invalid types)
- Integration flow verified
- No data leakage (temp files cleaned)
