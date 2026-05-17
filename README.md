# MCQ Generator

A modular Python application that generates multiple choice questions (MCQs) from PDF study materials using Google's Gemini AI.

## Features

- **PDF Processing**: Extract text from PDF files
- **Content Summarization**: Summarize study material using Gemini AI
- **MCQ Generation**: Generate 5 MCQs for a given topic
- **Modular Architecture**: Clean separation of concerns with dedicated modules

## Project Structure

```
MCQ_Generator/
├── __init__.py              # Package initialization
├── main.py                  # Entry point
├── config.py                # Configuration settings
├── models.py                # Model initialization
├── pdf_processor.py         # PDF reading and extraction
├── chains.py                # LangChain chains
├── utils.py                 # Utility functions
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Installation

1. Clone or navigate to the project directory:
```bash
cd MCQ_Generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Streamlit UI (Recommended)

Run the Streamlit application:

```bash
cd MCQ_Generator
streamlit run streamlit_app.py
```

The application will open in your browser with:
- **Left Panel**: PDF upload, topic input, and save button
- **Right Panel**: Scrollable MCQ display area

### Option 2: Command Line

Run the application from the parent directory:

```bash
python -m MCQ_Generator.main
```

Or from within the MCQ_Generator directory:

```bash
python main.py
```

### CLI Interactive Flow

1. **API Configuration**: Enter your Gemini API key
2. **Model Initialization**: The application initializes the Gemini model
3. **Load Study Material**: Provide the path to your PDF file
4. **Content Processing**: The application summarizes the PDF content
5. **MCQ Generation**: Enter a topic to generate 5 MCQs
6. **Save Results** (Optional): Save the summary and MCQs to files

## Configuration

Edit `config.py` to customize:

- Model name and parameters
- Temperature settings
- API retry behavior
- Default paths and domains

## Modules

### config.py
- API key retrieval
- File path management
- Model configuration

### models.py
- Gemini model initialization
- Model parameter setup

### pdf_processor.py
- PDF file reading
- Text extraction

### chains.py
- Summary generation chain
- MCQ generation chain

### utils.py
- Output formatting
- File saving utilities

### main.py
- Application orchestration
- User interaction flow

## Requirements

- Python 3.8+
- Google Gemini API key
- Dependencies listed in `requirements.txt`

## API Key

To get a Gemini API key:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Provide it when prompted by the application

## Error Handling

The application includes error handling for:
- Missing or invalid PDF files
- API connection issues
- Invalid topic inputs

## Output

The application provides:
- Console output of summaries and MCQs
- Optional save to text files with timestamp

## License

MIT License
