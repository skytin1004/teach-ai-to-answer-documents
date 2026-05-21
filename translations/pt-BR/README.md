# Ensine IA a Responder Perguntas Baseadas em Seus Documentos

Este repositório reúne uma série de blogs de 2026 sobre a construção de sistemas de IA fundamentados em documentos com RAG, serviços de IA da Azure, alternativas de código aberto e fluxos de trabalho orientados à avaliação.

## Contexto

Em 2023, trabalhei em um par de tutoriais sobre como ensinar o ChatGPT a responder perguntas a partir de documentos em PDF usando Azure AI Search e Azure OpenAI. A ideia de “ChatGPT nos seus dados” ainda parecia nova na época, e o objetivo era mostrar um fluxo prático: armazenar documentos, indexá-los, recuperar conteúdo relevante e gerar respostas a partir desse contexto recuperado.

Em 2026, o ecossistema RAG é muito maior. Azure AI Search suporta padrões modernos de recuperação vetorial e híbrida, Azure OpenAI faz parte do ecossistema mais amplo de Modelos Microsoft Foundry, e ferramentas de código aberto como LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama e vLLM se tornaram escolhas práticas para sistemas reais.

Por isso quis revisitar este tema. A pergunta já não é apenas “Como construir RAG?” Agora há muitas maneiras de construí-lo, e a questão mais importante é “Qual arquitetura devo escolher para minha situação?”

Esta série parte dessa camada de decisão. Antes de aprofundar na implementação, ela analisa por que os serviços de IA precisam de recuperação, quando faz sentido usar serviços gerenciados baseados na Azure, quando alternativas de código aberto são mais adequadas e onde o fine-tuning se encaixa.

## Artigos

1. [Série 1: RAG, Azure vs Alternativas Open-Source, e Quando o Fine-Tuning Faz Sentido](./series-1-rag-azure-open-source-fine-tuning.md)

## Suporte Multilíngue

### Suportado pelo Co-op Translator (Automatizado e Sempre Atualizado)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Árabe](../ar/README.md) | [Bengali](../bn/README.md) | [Búlgaro](../bg/README.md) | [Birmanês (Myanmar)](../my/README.md) | [Chinês (Simplificado)](../zh-CN/README.md) | [Chinês (Tradicional, Hong Kong)](../zh-HK/README.md) | [Chinês (Tradicional, Macau)](../zh-MO/README.md) | [Chinês (Tradicional, Taiwan)](../zh-TW/README.md) | [Croata](../hr/README.md) | [Tcheco](../cs/README.md) | [Dinamarquês](../da/README.md) | [Holandês](../nl/README.md) | [Estoniano](../et/README.md) | [Finlandês](../fi/README.md) | [Francês](../fr/README.md) | [Alemão](../de/README.md) | [Grego](../el/README.md) | [Hebraico](../he/README.md) | [Hindi](../hi/README.md) | [Húngaro](../hu/README.md) | [Indonésio](../id/README.md) | [Italiano](../it/README.md) | [Japonês](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Coreano](../ko/README.md) | [Lituano](../lt/README.md) | [Malaio](../ms/README.md) | [Malaiala](../ml/README.md) | [Marata](../mr/README.md) | [Nepali](../ne/README.md) | [Pidgin Nigeriano](../pcm/README.md) | [Norueguês](../no/README.md) | [Persa (Farsi)](../fa/README.md) | [Polonês](../pl/README.md) | [Português (Brasil)](./README.md) | [Português (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Romeno](../ro/README.md) | [Russo](../ru/README.md) | [Sérvio (Cirílico)](../sr/README.md) | [Eslovaco](../sk/README.md) | [Esloveno](../sl/README.md) | [Espanhol](../es/README.md) | [Suaíli](../sw/README.md) | [Sueco](../sv/README.md) | [Tagalo (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Tailandês](../th/README.md) | [Turco](../tr/README.md) | [Ucraniano](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamita](../vi/README.md)

> **Prefere Clonar Localmente?**
>
> Este repositório inclui traduções para mais de 50 idiomas, o que aumenta significativamente o tamanho do download. Para clonar sem traduções, use checkout esparso:
>
> **Bash / macOS / Linux:**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows):**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Isso oferece tudo que você precisa para completar o curso com um download muito mais rápido.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido usando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos pela precisão, por favor, esteja ciente de que traduções automatizadas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->