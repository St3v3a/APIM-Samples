# Lindex - Local Index Search Application

## Overview

Llama Index is used to demonstrate a local file indexing and search application that uses vector embeddings to enable semantic search capabilities for your local files.

**Fork this repo if you wish to make changes - code is provided as is without warrenty**

This application is configured to use Azure API Management (APIM) Gateway API (OpenAI 2024-10-21 spec) to demonstrate integration with Azure OpenAI services through APIM.

The application:

- Uses APIM API endpoints and keys configured in `.env`
- Uses models defined in `app.py` (these can be optionally moved to `.env`)
- Processes documents from the `\data` folder and creates vector embeddings  (add / remove content here)
- Provides an interactive interface for asking questions about the processed documents
- Maintains persistent vector storage for quick subsequent access

## Features

- Local file indexing with vector embeddings
- Interactive question-answering interface
- Semantic search capabilities
- Configurable file type support
- Persistent vector storage
- Clean interface with formatted output
- Option to reset vector storage

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Azure APIM subscription with OpenAI services configured

### Setup

1. Clone the repository:

```bash
git clone [repository-url]
cd lindex
```

2. Create and activate a virtual environment (conda, venv, UV etc.)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your environment variables (see Environment Variables section)

### Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit the `.env` file and update the following variables with your values:

```plaintext
API-KEY=<your apim api key>
AZURE-APIM-URL=<Azure APIM URL>  # e.g. https://xxxxx.azure-api.net/our-oai-1
API-VERSION=<apim openai api version>  # e.g. 2024-10-21
```

Note: Do not use quotes in any of the environment variables.

### Data Preparation

1. Create a `data` directory in the project root (if it doesn't exist)
2. Place your documents in the `data` directory
3. Supported file types include: txt, pdf, md, etc.

## Usage

### Running the Application

1. Start the application:

```bash
python app.py
```

2. Vector Storage Management:

   - On startup, you'll be asked if you want to remove existing vector storage
   - Choose 'yes' to start fresh (useful if your data has changed)
   - Choose 'no' to use existing vectors (faster if data hasn't changed)
3. The application will then:

   - Load existing index (if available and you chose 'no')
   - Or create a new index by processing documents in the `data/` directory
4. Interactive Usage:

   - Enter your questions when prompted
   - View the sources and formatted answers for each question
   - Press Enter to ask another question
   - Press Ctrl+C to exit the application

### Vector Storage

The application stores vector embeddings in a local vector database:

- Location: `./vectors/` directory
- Contents:
  - Vector embeddings
  - Document metadata
  - Index configuration
  - Search optimization data

### Azure OpenAI Integration

The application uses Azure OpenAI through APIM for:

- Text embeddings (Ada 002)
- Query processing (GPT-4)

All Azure OpenAI configuration is managed through environment variables in your `.env` file.

## Performance Considerations

- First-time indexing may take longer as documents are processed
- Subsequent runs are faster using stored vectors
- Vector storage can be reset if document content changes
- Query response time depends on:
  - Document size
  - Query complexity
  - Azure OpenAI service response time

## Troubleshooting

Common issues and solutions:

1. Environment Variables:

   - Ensure `.env` file exists and contains all required variables
   - Check for any typos in API keys or URLs
   - Don't use quotes in variable values
2. Data Processing:

   - Ensure documents are in the `data/` directory
   - Check file permissions
   - Verify supported file formats
3. Vector Storage:

   - If results seem incorrect, try removing existing vectors
   - Ensure enough disk space for vector storage
   - Check write permissions in the vectors directory
