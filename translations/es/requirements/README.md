# Requisitos

Cada artículo de implementación tiene un archivo de requisitos enfocado.

| Archivo | Usado por |
| --- | --- |
| [open-source-rag.txt](../../../requirements/open-source-rag.txt) | Cuaderno RAG de código abierto de la Serie 2, incluyendo asistentes opcionales de generación Ollama |
| [all.txt](../../../requirements/all.txt) | Verificación a nivel de repositorio y CI |

Use el archivo enfocado al ejecutar un cuaderno. Use `all.txt` al validar todo el repositorio.

`open-source-rag.txt` y `all.txt` incluyen `fastembed` para embeddings locales y `python-dotenv` para que la Serie 2 pueda habilitar opcionalmente la generación Ollama desde `.env` sin cambiar la pipeline de recuperación.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->