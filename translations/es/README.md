# Enseña a la IA a Responder Preguntas Basadas en Tus Documentos

Este repositorio recopila una serie de blogs de 2026 sobre la construcción de sistemas de IA fundamentados en documentos con RAG, servicios de Azure AI, alternativas de código abierto y flujos de trabajo orientados a la evaluación.

## Antecedentes

En 2023, trabajé en un par de tutoriales sobre cómo enseñar a ChatGPT a responder preguntas a partir de documentos PDF usando Azure AI Search y Azure OpenAI. La idea de "ChatGPT sobre tus datos" todavía parecía nueva en ese momento, y el objetivo era mostrar un flujo de trabajo práctico: almacenar documentos, indexarlos, recuperar contenido relevante y generar respuestas a partir de ese contexto recuperado.

En 2026, el ecosistema RAG es mucho más amplio. Azure AI Search admite patrones modernos de recuperación vectorial e híbrida, Azure OpenAI es parte del ecosistema más amplio de Microsoft Foundry Models, y herramientas de código abierto como LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama y vLLM se han convertido en opciones prácticas para sistemas reales.

Por eso quise revisar este tema nuevamente. La pregunta ya no es solo "¿Cómo construyo RAG?" Ahora hay muchas formas de construirlo, y la pregunta más importante es "¿Qué arquitectura debo elegir para mi situación?"

Esta serie parte de esa capa de toma de decisiones. Antes de profundizar en la implementación, analiza por qué los servicios de IA necesitan recuperación, cuándo tienen sentido los servicios gestionados basados en Azure, cuándo las alternativas de código abierto son una mejor opción y dónde encaja el ajuste fino.

## Artículos

1. [Serie 1: RAG, Azure vs Alternativas de Código Abierto y Cuándo Tiene Sentido el Ajust Fino](./series-1-rag-azure-open-source-fine-tuning.md)

## Soporte Multilingüe

### Soportado a través de Co-op Translator (Automatizado y Siempre Actualizado)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Árabe](../ar/README.md) | [Bengalí](../bn/README.md) | [Búlgaro](../bg/README.md) | [Birmano (Myanmar)](../my/README.md) | [Chino (Simplificado)](../zh-CN/README.md) | [Chino (Tradicional, Hong Kong)](../zh-HK/README.md) | [Chino (Tradicional, Macao)](../zh-MO/README.md) | [Chino (Tradicional, Taiwán)](../zh-TW/README.md) | [Croata](../hr/README.md) | [Checo](../cs/README.md) | [Danés](../da/README.md) | [Neerlandés](../nl/README.md) | [Estonio](../et/README.md) | [Finlandés](../fi/README.md) | [Francés](../fr/README.md) | [Alemán](../de/README.md) | [Griego](../el/README.md) | [Hebreo](../he/README.md) | [Hindi](../hi/README.md) | [Húngaro](../hu/README.md) | [Indonesio](../id/README.md) | [Italiano](../it/README.md) | [Japonés](../ja/README.md) | [Canarés](../kn/README.md) | [Jemer](../km/README.md) | [Coreano](../ko/README.md) | [Lituano](../lt/README.md) | [Malayo](../ms/README.md) | [Malabar](../ml/README.md) | [Maratí](../mr/README.md) | [Nepalí](../ne/README.md) | [Pidgin Nigeriano](../pcm/README.md) | [Noruego](../no/README.md) | [Persa (Farsi)](../fa/README.md) | [Polaco](../pl/README.md) | [Portugués (Brasil)](../pt-BR/README.md) | [Portugués (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumano](../ro/README.md) | [Ruso](../ru/README.md) | [Serbio (Cirílico)](../sr/README.md) | [Eslovaco](../sk/README.md) | [Esloveno](../sl/README.md) | [Español](./README.md) | [Swahili](../sw/README.md) | [Sueco](../sv/README.md) | [Tagalo (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Tailandés](../th/README.md) | [Turco](../tr/README.md) | [Ucraniano](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamita](../vi/README.md)

> **¿Prefieres Clonar Localmente?**
>
> Este repositorio incluye más de 50 traducciones que aumentan significativamente el tamaño de descarga. Para clonar sin traducciones, usa sparse checkout:
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
> Esto te da todo lo que necesitas para completar el curso con una descarga mucho más rápida.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->