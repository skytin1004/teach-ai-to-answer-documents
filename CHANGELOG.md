# Changelog

## Unreleased

Initial public release scope for **Teach AI to Answer Questions Based on Your Documents**.

### Added

- Series 1 article on RAG architecture decisions, Azure vs open-source tradeoffs, and where fine-tuning fits.
- Series 2 article and notebook for a local open-source RAG workflow using Qdrant local mode, FastEmbed local embeddings, lightweight reranking, Ollama, and Phi-4-mini.
- Series 2 step-by-step end-to-end tutorial format with Python snippets and verification notes from the executed notebook.
- Optional Series 2 answer-generation path with Ollama and Phi-4-mini while keeping local CPU-friendly retrieval as the default path.
- Local Ollama verification for Series 2 using `phi4-mini:3.8b` on RTX 3060 Laptop GPU.
- Sample data for school policy and course AI guidance.
- Requirements files for the public notebook and repository-level verification.
- Repository verification script for local Markdown links and notebook validation/execution.
- GitHub Actions workflow for notebook verification.
- `.env.example` for optional local Ollama generation setup without committing local configuration.
- Folder-level README files for articles, notebooks, requirements, sample data, and scripts.
- Publishing checklist for public safety and verification.
- Draft workspace for future Azure and evaluation content.

### Verified

- Local Markdown link validation passes.
- Series 2 notebook validates successfully.
- Series 2 notebook executes successfully in the local verification environment.
- Notebook files are kept without saved outputs or execution counts.
- No real secrets are committed.
