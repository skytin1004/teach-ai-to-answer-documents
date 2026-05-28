# Enseñar a la IA a Responder Preguntas Basadas en Tus Documentos - Plan de la Serie

Este plan realiza un seguimiento de la publicación pública de la Serie 1 y la Serie 2. Más adelante, el trabajo con Azure y la evaluación se mantendrá como borradores hasta que los ejemplos estén completamente integrados y verificados.

No cometas ni subas cambios hasta que se indique explícitamente.

## Alcance Público

Publicación pública actual:

- Artículo de la Serie 1: decisiones de arquitectura RAG, compensaciones entre Azure y código abierto, y dónde encaja el ajuste fino.
- Artículo de la Serie 2: tutorial local de RAG de código abierto.
- Cuaderno de la Serie 2: laboratorio local RAG ejecutable con FastEmbed, Qdrant, Ollama y Phi-4-mini.
- Datos de muestra: archivos Markdown de política escolar y guía de IA del curso.

Borradores pero aún no en el índice público:

- Reconstrucción de Azure AI Search y Azure OpenAI.
- Evaluación y comprobaciones de regresión de RAG.

## Escenario del Tutorial

El escenario compartido es un asistente de política escolar.

El asistente responde a esta pregunta a partir de documentos locales:

```text
Can I use generative AI for my final assignment?
```

El comportamiento esperado es:

1. Cargar documentos Markdown locales.
2. Analizarlos y fragmentarlos por encabezados.
3. Crear embeddings locales y almacenar representaciones buscables con metadatos.
4. Recuperar la sección de política relevante.
5. Reordenar cuando sea necesario.
6. Generar o componer una respuesta fundamentada.
7. Devolver las citas.
8. Registrar los resultados de la verificación.

## Estructura Pública Actual

```text
.
├── README.md
├── SERIES_PLAN.md
├── articles/
│   ├── README.md
│   ├── series-1-rag-azure-open-source-fine-tuning.md
│   └── series-2-open-source-rag-end-to-end.md
├── notebooks/
│   ├── README.md
│   └── series-2-open-source-rag.ipynb
├── sample_data/
│   ├── README.md
│   ├── course_ai_guidance.md
│   └── school_ai_policy.md
├── requirements/
│   ├── README.md
│   ├── all.txt
│   └── open-source-rag.txt
└── scripts/
    ├── README.md
    └── verify_notebooks.py
```

El material en borrador se almacena bajo `drafts/` y es omitido por la verificación del repositorio hasta que esté listo para el índice público.

## Verificación de la Serie 2

Verificado en Windows con Python 3.12.6.

- Se instalaron correctamente los `requirements/open-source-rag.txt`.
- Se ejecutó `notebooks/series-2-open-source-rag.ipynb` con `nbclient`.
- Verificación local aprobada: se cargaron 2 documentos de muestra, se crearon 8 fragmentos, FastEmbed generó embeddings locales de 384 dimensiones, se inicializó la colección en memoria de Qdrant y se insertaron 8 vectores.
- Pregunta de prueba: "¿Puedo usar IA generativa para mi trabajo final?"
- Fuente principal recuperada después del reordenamiento ligero: `school_ai_policy.md`.
- Sección principal recuperada después del reordenamiento ligero: `Final Assignments`.
- Ruta de respuesta predeterminada: compositor de respuesta transparente local.
- Ollama instalado a través de winget; `phi4-mini:3.8b` descargado con éxito.
- Ruta de generación de respuestas Ollama: completada con `phi4-mini:3.8b`.
- Tamaño del archivo del modelo Ollama: aprox. 2.49GB en disco.
- Tamaño del modelo cargado en Ollama: 3.3GB reportado por `ollama ps`.
- Descarga a GPU: 100% de GPU reportado por `ollama ps` en GPU portátil RTX 3060.
- Memoria GPU observada tras la generación: aprox. 3.5GB de 6GB.
- Ejecución del cuaderno con modelo FastEmbed en caché y generación Ollama habilitada aprobada en unos 34 segundos mediante el script de verificación.
- Observación: una pasada temprana de carga de documentos incluyó accidentalmente `sample_data/README.md`; ahora el cuaderno carga explícitamente solo los dos documentos de muestra previstos.

## Verificación del Repositorio

- `scripts/verify_notebooks.py` valida enlaces Markdown locales, JSON de cuadernos, limpieza de salida de los cuadernos y patrones de secretos de alto riesgo.
- `scripts/verify_notebooks.py --execute` ejecuta cuadernos públicos desde la raíz del repositorio.
- El material en borrador bajo `drafts/` es omitido intencionadamente.

## Próximo Trabajo

- Reconstruir el mismo escenario con Azure AI Search y Azure OpenAI como parte futura de la serie.
- Agregar evaluación de recuperación y respuestas una vez que las implementaciones locales y de Azure sean estables.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->