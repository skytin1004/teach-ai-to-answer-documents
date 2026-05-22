# Enseña a la IA a Responder Preguntas Basadas en Tus Documentos

![Resumen del sistema de IA RAG basado en documentos](../../assets/images/readme-hero.svg)

Este repositorio recopila una serie de blogs de 2026 sobre la construcción de sistemas de IA basados en documentos con RAG, servicios de Azure AI, alternativas de código abierto y flujos de trabajo orientados a la evaluación.

## Antecedentes

En 2023, trabajé en un par de tutoriales sobre cómo enseñar a ChatGPT a responder preguntas a partir de documentos PDF utilizando Azure AI Search y Azure OpenAI. La idea de "ChatGPT en tus datos" aún parecía nueva entonces, y el objetivo era mostrar un flujo de trabajo práctico: almacenar documentos, indexarlos, recuperar contenido relevante y generar respuestas a partir de ese contexto recuperado.

En 2026, el ecosistema RAG es mucho más amplio. Azure AI Search soporta patrones modernos de recuperación vectorial e híbrida, Azure OpenAI forma parte del ecosistema más amplio de Microsoft Foundry Models, y herramientas de código abierto como LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama y vLLM se han convertido en opciones prácticas para sistemas reales.

Por eso quería volver a abordar este tema. La pregunta ya no es solo "¿Cómo construyo RAG?" Ahora hay muchas formas de construirlo, y la pregunta más importante es "¿Qué arquitectura debería elegir para mi situación?"

Esta serie comienza desde esa capa de toma de decisiones y luego la transforma en tutoriales prácticos. La primera vía de implementación construye un sistema RAG local de código abierto que cualquiera puede ejecutar con datos de ejemplo, Qdrant, Ollama y Phi-4-mini.

## Artículos

Consulta [articles/README.md](./articles/README.md) para el índice de artículos.

1. [Serie 1: RAG, Azure vs Alternativas de Código Abierto y Cuándo Tiene Sentido el Fine-Tuning](./articles/series-1-rag-azure-open-source-fine-tuning.md)
2. [Serie 2: Construye un Sistema RAG Local de Código Abierto de Principio a Fin](./articles/series-2-open-source-rag-end-to-end.md)

Próximamente:

- Reconstruir el mismo sistema RAG con Azure AI Search y Azure OpenAI.
- Añadir evaluación y chequeos de regresión más allá de una respuesta de demostración.

## Notebooks

Los artículos de implementación usan notebooks para que los pasos de recuperación y evaluación puedan ser inspeccionados directamente. Consulta [notebooks/README.md](./notebooks/README.md) para orientación a nivel de carpeta.

> [!TIP]
> Comienza con la Serie 2 si quieres el camino más rápido. Se ejecuta localmente con datos de muestra, embeddings compatibles con CPU, modo local de Qdrant y sin credenciales de nube.

| Serie | Notebook | Requisitos | Verificación local |
| --- | --- | --- | --- |
| Serie 2 | [Notebook RAG de código abierto](./notebooks/series-2-open-source-rag.ipynb) | [open-source-rag.txt](../../requirements/open-source-rag.txt) | Verificado modo local de Qdrant, recuperación, reranking y conexión de fuentes |

Para ejecutar un notebook localmente, crea un entorno virtual e instala el archivo de requisitos correspondiente. Por ejemplo:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

## Datos de Ejemplo

Los notebooks usan un pequeño corpus local en [sample_data](../../sample_data) para que los ejemplos puedan ejecutarse sin documentos privados ni credenciales en la nube. Consulta [sample_data/README.md](./sample_data/README.md) para más detalles.

- [school_ai_policy.md](./sample_data/school_ai_policy.md)
- [course_ai_guidance.md](./sample_data/course_ai_guidance.md)

## Resumen de Verificación Local

Los resultados de verificación se registran en cada artículo y en [SERIES_PLAN.md](./SERIES_PLAN.md).

| Área | Resultado |
| --- | --- |
| Ruta de código abierto Serie 2 | FastEmbed generó embeddings locales de 384 dimensiones, Qdrant insertó 8 vectores en la colección en memoria, el reranking ligero recuperó la sección esperada; la generación opcional con Ollama se completó con `phi4-mini:3.8b` |

El notebook local evita intencionadamente secretos codificados.

## Generación Local con Ollama

El notebook de la Serie 2 es seguro para uso local por defecto. Para habilitar la generación local con Ollama, copia [.env.example](../../.env.example) a `.env` y completa los valores de la Serie 2.

Para la generación Serie 2 con Ollama, descomenta:

```text
SERIES2_OLLAMA_BASE_URL=http://localhost:11434
SERIES2_OLLAMA_MODEL=phi4-mini:3.8b
```

El notebook de la Serie 2 carga automáticamente `.env` desde la raíz del repositorio usando `python-dotenv`.

> [!IMPORTANT]
> No subas archivos `.env`, claves API, endpoints privados o valores específicos de tenant. El repositorio intencionadamente mantiene los secretos fuera de los archivos Markdown y notebooks.

Los archivos de requisitos están documentados en [requirements/README.md](./requirements/README.md).

Para validar enlaces, estructura del notebook, limpieza de la salida del notebook y patrones de secretos de alto riesgo:

```powershell
python -m venv .venv-verify
.\.venv-verify\Scripts\activate
python -m pip install -r requirements\all.txt
python scripts\verify_notebooks.py
```

Los scripts de verificación están documentados en [scripts/README.md](./scripts/README.md).

Para ejecutar todos los notebooks seguros localmente en el mismo entorno:

```powershell
python scripts\verify_notebooks.py --execute
```

El mismo flujo de verificación se ejecuta en GitHub Actions en pushes, pull requests y despachos manuales de workflow. Los artículos y notebooks en borrador están intencionadamente excluidos de la ruta de verificación pública.

Antes de publicar actualizaciones, usa [PUBLISHING_CHECKLIST.md](./PUBLISHING_CHECKLIST.md).

Consulta [CHANGELOG.md](./CHANGELOG.md) para el resumen actual de cambios no publicados.

Para pautas de contribución y limpieza de notebooks, consulta [CONTRIBUTING.md](./CONTRIBUTING.md).

## Soporte Multilingüe

### Compatible vía Co-op Translator (Automatizado y Siempre Actualizado)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Árabe](../ar/README.md) | [Bengalí](../bn/README.md) | [Búlgaro](../bg/README.md) | [Birmano (Myanmar)](../my/README.md) | [Chino (Simplificado)](../zh-CN/README.md) | [Chino (Tradicional, Hong Kong)](../zh-HK/README.md) | [Chino (Tradicional, Macao)](../zh-MO/README.md) | [Chino (Tradicional, Taiwán)](../zh-TW/README.md) | [Croata](../hr/README.md) | [Checo](../cs/README.md) | [Danés](../da/README.md) | [Holandés](../nl/README.md) | [Estonio](../et/README.md) | [Finlandés](../fi/README.md) | [Francés](../fr/README.md) | [Alemán](../de/README.md) | [Griego](../el/README.md) | [Hebreo](../he/README.md) | [Hindi](../hi/README.md) | [Húngaro](../hu/README.md) | [Indonesio](../id/README.md) | [Italiano](../it/README.md) | [Japonés](../ja/README.md) | [Canarés](../kn/README.md) | [Jemer](../km/README.md) | [Coreano](../ko/README.md) | [Lituano](../lt/README.md) | [Malayo](../ms/README.md) | [Malayalam](../ml/README.md) | [Maratí](../mr/README.md) | [Nepalí](../ne/README.md) | [Pidgin Nigeriano](../pcm/README.md) | [Noruego](../no/README.md) | [Persa (Farsi)](../fa/README.md) | [Polaco](../pl/README.md) | [Portugués (Brasil)](../pt-BR/README.md) | [Portugués (Portugal)](../pt-PT/README.md) | [Punjabi (Gurmukhi)](../pa/README.md) | [Rumano](../ro/README.md) | [Ruso](../ru/README.md) | [Serbio (Cirílico)](../sr/README.md) | [Eslovaco](../sk/README.md) | [Esloveno](../sl/README.md) | [Español](./README.md) | [Swahili](../sw/README.md) | [Sueco](../sv/README.md) | [Tagalo (Filipino)](../tl/README.md) | [Tamil](../ta/README.md) | [Telugu](../te/README.md) | [Tailandés](../th/README.md) | [Turco](../tr/README.md) | [Ucraniano](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamita](../vi/README.md)

> **¿Prefieres Clonar Localmente?**
>
> Este repositorio incluye más de 50 traducciones de idiomas, lo que incrementa significativamente el tamaño de la descarga. Para clonar sin las traducciones, usa sparse checkout:
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
> Esto te proporciona todo lo necesario para completar el curso con una descarga mucho más rápida.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->