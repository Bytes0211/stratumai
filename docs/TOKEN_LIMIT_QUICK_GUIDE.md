# Token Limit Quick Reference Guide

## Token Capacity by Model

| Provider | Model | Context Window | Estimated File Size |
|----------|-------|----------------|---------------------|
| OpenAI | gpt-4o | 128k tokens | ~512 KB |
| OpenAI | o1, o3-mini | 200k tokens | ~800 KB |
| Anthropic | Claude Sonnet 4.5 | 200k tokens | ~800 KB |
| Anthropic | Claude Opus 4.5 | 1M tokens* | ~4 MB* |
| Google | Gemini 2.5 Pro/Flash | 1M tokens | ~4 MB |
| OpenRouter | Grok 4.1 Fast | 1.8M tokens | ~7.2 MB |

*Note: Claude Opus 4.5 has 200k API input limit despite 1M context window

## Six Solutions for Large Files

### 1. Smart Chunking (Best for: Large documents)
**Problem**: 2 MB file exceeds 128k token limit  
**Solution**: Split into chunks, summarize each, combine summaries  
**Savings**: 94% cost reduction  
**Command**: `stratumai upload file.txt --chunked --chunk-size 50000`

### 2. Intelligent Extraction (Best for: CSV, JSON, Logs)
**Problem**: 10 MB CSV file  
**Solution**: Extract schema + sample + stats instead of full data  
**Savings**: 99%+ token reduction  
**Command**: `stratumai analyze data.csv --extract-mode schema`

### 3. Long-Context Models (Best for: Need full context)
**Problem**: 3 MB file needs full analysis  
**Solution**: Auto-select Gemini 2.5 Pro (1M context)  
**Savings**: Fits in context (vs. failing with smaller models)  
**Command**: `stratumai upload file.txt --auto-select-model`

### 4. Prompt Caching (Best for: Multiple queries on same file)
**Problem**: Re-analyzing same 2 MB file 10 times  
**Solution**: Cache file context, subsequent queries 90% cheaper  
**Savings**: 90% on queries 2-10  
**Command**: `stratumai interactive-cached file.txt --provider anthropic`

### 5. RAG/Vector DB (Best for: Massive datasets >10 MB)
**Problem**: 50 MB documentation, only need relevant sections  
**Solution**: Create vector DB, semantic search relevant chunks only  
**Savings**: 95%+ token reduction  
**Implementation**: Requires ChromaDB/Pinecone integration

### 6. Compression (Best for: Repetitive data)
**Problem**: Logs with duplicate entries  
**Solution**: De-duplicate, extract errors only  
**Savings**: 70-90% token reduction  
**Command**: `stratumai analyze log.txt --compress deduplicate`

## Decision Tree

```
Is file < 500 KB?
├─ YES → Use current upload (no optimization needed)
└─ NO → Is file size known?
    ├─ < 4 MB → Use Solution 3: Long-context models
    ├─ 4-10 MB → Multiple queries? 
    │   ├─ YES → Use Solution 4: Prompt caching
    │   └─ NO → Use Solution 1: Chunking + summarization
    └─ > 10 MB → Use Solution 5: RAG/Vector DB

File type specific:
├─ CSV/JSON → Use Solution 2: Schema extraction
├─ Logs → Use Solution 2: Error extraction
├─ Code → Use Solution 2: Function/class extraction
└─ Documents → Use Solution 1: Chunking + summarization
```

## Implementation Priority

### Immediate (Week 1)
1. Token count estimation before upload
2. Warning when file exceeds model context
3. Basic chunking implementation

### Short-term (Week 2-3)
4. Intelligent extraction for CSV/JSON/logs
5. Auto-model selection based on file size
6. Enhanced file upload UI

### Medium-term (Week 4+)
7. Prompt caching support
8. File compression utilities
9. RAG/vector DB integration (optional)

## Example Scenarios

### Scenario 1: Analyzing Large CSV
```bash
# Problem: 5 MB CSV with 1M rows
stratumai analyze sales_data.csv --extract-mode schema

# Result: 
# - Extracted schema: 200 bytes
# - Sample 100 rows: ~20 KB
# - Statistics: ~5 KB
# Total: ~25 KB (99.5% reduction!)
```

### Scenario 2: Multiple Queries on Same Document
```bash
# Problem: Need to query 2 MB research paper 10 times
stratumai interactive-cached paper.pdf --provider anthropic

# Cost comparison:
# Without caching: 10 queries × $1.50 = $15.00
# With caching: $3.38 + 9 × $0.15 = $4.73 (68% savings)
```

### Scenario 3: Processing Large Log File
```bash
# Problem: 10 MB log file, need to find errors
stratumai analyze server.log --extract errors

# Result:
# - Total lines: 500,000
# - Errors extracted: 234 errors
# - Token reduction: 500k → 5k (99% reduction)
```

### Scenario 4: Very Large Document
```bash
# Problem: 8 MB documentation file
stratumai upload docs.txt --auto-select-model

# Result:
# - Auto-selected: google/gemini-2.5-pro (1M context)
# - File size: 8 MB ≈ 2M tokens (too large!)
# - Fallback: chunking + summarization
```

## Cost Comparison Table

| Approach | 2MB File | Cost (GPT-4o) | Cost (Claude Sonnet) | Notes |
|----------|----------|---------------|----------------------|-------|
| **Direct upload** | 500k tokens | $1.25 | $1.50 | May exceed limit |
| **Chunking + summary** | 10k tokens | $0.08 | $0.10 | 94% savings |
| **Schema extraction** | 5k tokens | $0.01 | $0.02 | 99% savings |
| **Long-context model** | 500k tokens | $0.63 (Gemini) | $1.50 | Fits in context |
| **Caching (2nd query)** | 500k cached | $0.13 | $0.15 | 90% savings |

## Best Practices

### DO:
✅ Estimate tokens before upload (chars ÷ 4)  
✅ Use long-context models when you need full file  
✅ Use caching for multiple queries on same file  
✅ Extract schema/sample for structured data  
✅ Chunk and summarize large documents  
✅ Show token count warnings to users  

### DON'T:
❌ Upload full 5 MB CSV when schema suffices  
❌ Re-upload same large file without caching  
❌ Use expensive models for simple summarization  
❌ Ignore token limits (requests will fail)  
❌ Upload binary files without conversion  

## Token Calculation Examples

```python
# Simple estimation
text = file.read_text()
estimated_tokens = len(text) // 4

# More accurate (requires tiktoken)
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
token_count = len(enc.encode(text))

# Check against model limits
context_window = 128000  # GPT-4o
if token_count > context_window * 0.8:
    print("Warning: File may exceed model context!")
```

## CLI Commands Quick Reference

```bash
# Current upload (with warnings)
stratumai interactive --file large.txt

# Auto-select model for file size
stratumai upload large.txt --auto-select-model

# Chunk large file
stratumai upload huge.txt --chunked --chunk-size 50000

# Extract schema from CSV
stratumai analyze data.csv --extract-mode schema

# Extract errors from logs
stratumai analyze server.log --extract errors

# Interactive with caching
stratumai interactive-cached report.pdf --provider anthropic

# Compress before upload
stratumai upload logs.txt --compress deduplicate
```

## Support Matrix

| Solution | Implemented | Tested | Documented |
|----------|-------------|--------|------------|
| File size warnings | ✅ | ✅ | ✅ |
| Token truncation | ✅ | ✅ | ✅ |
| Long-context models | ✅ | ✅ | ✅ |
| Chunking | ❌ | ❌ | ✅ |
| Smart extraction | ❌ | ❌ | ✅ |
| Model auto-select | ❌ | ❌ | ✅ |
| Prompt caching | ⚠️ Partial | ⚠️ Partial | ✅ |
| RAG/Vector DB | ❌ | ❌ | ✅ |
| Compression | ❌ | ❌ | ✅ |

Legend: ✅ Complete | ⚠️ Partial | ❌ Not implemented

## Next Steps

1. **Review** docs/LARGE_FILE_STRATEGIES.md for detailed implementation
2. **Test** current file upload with large files
3. **Implement** priority features based on use cases
4. **Monitor** token usage and costs in production
5. **Iterate** based on user feedback

## Resources

- Full guide: `docs/LARGE_FILE_STRATEGIES.md`
- Auth error handling: `docs/AUTH_ERROR_HANDLING.md`
- CLI usage: `docs/cli-usage.md`
- API reference: `docs/API-REFERENCE.md`
