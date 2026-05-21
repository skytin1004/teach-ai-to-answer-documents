# Teach AI to Answer Questions Based on Your Documents

This repository collects a 2026 blog series about building document-grounded AI systems with RAG, Azure AI services, open-source alternatives, and evaluation-oriented workflows.

## Background

In 2023, I worked on a pair of tutorials about teaching ChatGPT to answer questions from PDF documents using Azure AI Search and Azure OpenAI. The idea of "ChatGPT on your data" still felt new then, and the goal was to show a practical workflow: store documents, index them, retrieve relevant content, and generate answers from that retrieved context.

In 2026, the RAG ecosystem is much larger. Azure AI Search supports modern vector and hybrid retrieval patterns, Azure OpenAI is part of the broader Microsoft Foundry Models ecosystem, and open-source tools such as LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, and vLLM have become practical choices for real systems.

That is why I wanted to revisit this topic. The question is no longer only "How do I build RAG?" There are now many ways to build it, and the more important question is "Which architecture should I choose for my situation?"

This series starts from that decision-making layer. Before going deep into implementation, it looks at why AI services need retrieval, when Azure-based managed services make sense, when open-source alternatives are a better fit, and where fine-tuning fits.

## Articles

1. [Series 1: RAG, Azure vs Open-Source Alternatives, and When Fine-Tuning Makes Sense](./series-1-rag-azure-open-source-fine-tuning.md)
