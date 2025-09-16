# Lead Scoring API

A Flask-based API for scoring and ranking B2B leads using rule-based algorithms and AI-powered intent classification via Google's Gemini API.

## Features

- **Lead Management**: Store and manage prospect information
- **Offer Management**: Define value propositions and ideal customer profiles
- **Automated Scoring**: Combine rule-based scoring with AI-powered intent analysis
- **Results Retrieval**: Get ranked results for specific offers
- **PostgreSQL Integration**: Robust database management with automated schema creation


## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create virtual environment in base directory**
   ```bash
   python -m venv venv
   ```

3. **Activate the environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Create .env file with contents of .env.example in base directory**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your actual configuration:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://127.0.0.1:5000`
