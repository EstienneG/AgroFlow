# AgroFlow: AI-Powered Agricultural Advisory System

## Overview

AgroFlow is an intelligent advisory system designed to empower French farmers ("agriculteurs") with a simple and intuitive tool for addressing a wide range of agricultural challenges. This project leverages artificial intelligence to provide specialized assistance across multiple domains of agricultural interest, from crop disease diagnosis to weather management and market insights.

## Project Architecture

AgriAssist employs a hub-and-spoke architecture:

1. **Central Routing System**: A fine-tuned small LLM classifier acts as the system's brain, analyzing user queries to efficiently route them to the most appropriate specialized agent.

2. **Specialized Agents**: Five domain-specific agents provide expert responses:
   - **Policy Advisor**: Uses Retrieval-Augmented Generation (RAG) to answer regulatory and compliance questions
   - **Market Analyst**: Uses web search to provide current market data and trends
   - **General Agriculture Assistant**: Uses web search to answer various agricultural queries
   - **Weather Manager**: Integrates with weather APIs to provide forecasts and cultivation recommendations
   - **Plant Disease Diagnostician**: Employs a Convolutional Neural Network (CNN) to identify plant diseases from images

```
                 ┌─────────────────┐
                 │                 │
User Query ──────▶  LLM Classifier │
                 │                 │
                 └────────┬────────┘
                          │
                          ▼
        ┌───────────────────┐─────────────┐────────────────┐
        │                   │             │                │
┌───────▼──────┐  ┌─────────▼──────┐  ┌──▼───────────┐  ┌──▼───────────┐
│              │  │                │  │              │  │              │
│ RAG-powered  │  │  Web Search    │  │ CNN Disease  │  │ Weather      │
│    Policy    │  │  for Market    │  │  Diagnosis   │  │  Expert   │
│   Advisor    │  │  & General     │  │              │  │              │
│              │  │   Queries      │  │              │  │              │
└──────────────┘  └────────────────┘  └──────────────┘  └──────────────┘
                                                                ▲
                                            ┌────────────────┐  │
                                            │                │  │
                                            │ Weather API    │──┘
                                            │                │
                                            └────────────────┘
```

## Key Components

### 1. Query Classification System

Located in `/src/finetuning/`, this component uses a fine-tuned language model to analyze user queries and categorize them into one of five themes:
- `market_question`: Market-related queries
- `policy_help`: Regulatory and compliance questions
- `disease_diagnosis`: Plant health and disease identification
- `weather_management`: Weather forecasts and related advice
- `other`: General agricultural inquiries

### 2. Policy Advisor (RAG)

Located in `/src/RAG/`, this component uses Retrieval-Augmented Generation to provide accurate information about agricultural policies and regulations. It leverages:
- Document embeddings stored as vectors in a Qdrant vector database
- BM25 search for enhanced retrieval performance
- Technical reports as knowledge sources

### 3. Plant Disease Diagnosis System

Located in `/src/integration/plant_disease/`, this component uses a CNN model to identify plant diseases from images:
- Supports multiple crops including tomatoes, potatoes, and peppers
- Detects various diseases such as early blight, late blight, bacterial spot, etc.
- Returns confidence scores and alternative diagnoses

### 4. Weather Management System

This component integrates with external weather APIs to provide:
- Current weather conditions
- Agricultural recommendations based on weather predictions

### 5. Market & General Information System

These components leverage web search capabilities to retrieve up-to-date information on:
- Market trends and prices
- Production statistics
- Agricultural innovations
- Best practices


## Usage

The system is designed to be accessed through a simple interface where farmers can:
1. Type natural language questions in French
2. Upload images for disease diagnosis
3. Receive specialized responses based on their query type

Example queries:
- "Quelle est la production de tournesol en 2024 ?" (Market query)
- "Quelle est la largeur minimale requise pour une bande tampon le long d'un cours d'eau ?" (Policy query)
- "Comment savoir si ma tomate est malade ?" (Disease diagnosis query)
- "Dois-je récolter ma tomate aujourd'hui ou puis-je attendre la semaine prochaine ?" (Weather management query)

## Technologies

- **LLM Integration**: Mistral AI for query routing and response generation
- **Vector Database**: Qdrant for efficient document retrieval
- **Image Processing**: PyTorch for CNN-based disease diagnosis
- **Search**: DuckDuckGo Search API for web retrieval
- **Other**: LlamaIndex, Rank-BM25, WandB for training monitoring

---

*AgroFlow: Empowering French farmers with AI-driven agricultural intelligence*
