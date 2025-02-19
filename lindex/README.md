# Lindex - Local Index Search Application

## Overview
Lindex is a local file indexing and search application that uses vector embeddings to enable semantic search capabilities for your local files.

## Features
- Local file indexing
- Semantic search using vector embeddings
- Configurable file type support
- Fast search results

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup
1. Clone the repository:
```bash
git clone [repository-url]
cd lindex
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Vector Storage
The application stores vector embeddings in a local vector database within the project directory:

- **Storage Location**: `./vectors/` (in project root)
- **Storage Files**:
  - `default__vector_store.json`: Contains the vector embeddings
  - `docstore.json`: Document metadata and content
  - `index_store.json`: Index configuration and metadata
  - `graph_store.json`: Graph relationships
  - `image__vector_store.json`: Image vector data (if applicable)

### Environment Variables
Create a `.env` file in the project root with the following:
```
API-KEY=your_azure_openai_api_key
```

### Azure OpenAI Configuration
The application uses Azure OpenAI for:
- Text embeddings (Ada 002)
- Query processing (GPT-4)

Configure the endpoints in `app.py`:
```python
azure_endpoint = "https://apimeuw1.azure-api.net/sa-works-oai-1/"
api_version = "2024-10-21"
```

### Tuning Parameters

#### Indexing Parameters
- `chunk_size`: 512 (number of tokens per text chunk)
- `overlap_size`: 50 (number of overlapping tokens between chunks)
- `batch_size`: 32 (batch size for vector processing)

#### Search Parameters
- `top_k`: 5 (number of results to return)
- `similarity_threshold`: 0.7 (minimum similarity score for results)

#### Vector Embedding
- Model: SentenceTransformers
- Embedding Dimension: 384
- Distance Metric: Cosine Similarity

## Usage

### Running the Application
```bash
# Run the application
python app.py

# The application will:
# 1. Create a vectors/ directory if it doesn't exist
# 2. Load existing index if available, or create new one
# 3. Process the documents in data/ directory
# 4. Save vectors for future use
```

### Basic Commands
```bash
# Index files in a directory
lindex index /path/to/directory

# Search through indexed files
lindex search "your search query"

# List indexed files
lindex list

# Remove files from index
lindex remove /path/to/file
```

### Advanced Configuration
You can customize the behavior by modifying `config.yaml`:

```yaml
storage:
  vector_path: "./vectors"
  metadata_path: "./metadata.db"

indexing:
  chunk_size: 512
  overlap_size: 50
  batch_size: 32
  file_types: [".txt", ".md", ".py", ".js", ".html", ".csv"]

search:
  top_k: 5
  similarity_threshold: 0.7
```

## Performance Considerations
- The application uses FAISS for efficient similarity search
- Memory usage scales with the number of indexed documents
- Recommended hardware: 8GB RAM minimum for optimal performance

## Contributing
Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License
[Specify License]
