# Registro de cambios

## No lanzado

Alcance de la versión pública inicial para **Enseñar a la IA a responder preguntas basándose en tus documentos**.

### Añadido

- Artículo de la serie 1 sobre decisiones de arquitectura RAG, compensaciones entre Azure y código abierto, y dónde encaja el ajuste fino.
- Artículo y cuaderno de la serie 2 para un flujo de trabajo RAG local de código abierto usando el modo local de Qdrant, incrustaciones locales FastEmbed, reordenamiento ligero, Ollama y Phi-4-mini.
- Formato tutorial paso a paso de la serie 2 de extremo a extremo con fragmentos de Python y notas de verificación del cuaderno ejecutado.
- Ruta opcional de generación de respuestas de la serie 2 con Ollama y Phi-4-mini manteniendo la recuperación local amigable con CPU como ruta predeterminada.
- Verificación local de Ollama para la serie 2 usando `phi4-mini:3.8b` en GPU RTX 3060 Laptop.
- Datos de muestra para políticas escolares y orientación de IA para cursos.
- Archivos de requisitos para el cuaderno público y la verificación a nivel de repositorio.
- Script de verificación del repositorio para enlaces Markdown locales y validación/ejecución del cuaderno.
- Flujo de trabajo de GitHub Actions para la verificación del cuaderno.
- `.env.example` para configuración opcional de generación local Ollama sin comprometer configuración local.
- Archivos README a nivel de carpeta para artículos, cuadernos, requisitos, datos de muestra y scripts.
- Lista de verificación de publicación para seguridad pública y verificación.
- Espacio de trabajo borrador para contenido futuro de Azure y evaluación.

### Verificado

- La validación local de enlaces Markdown pasa correctamente.
- El cuaderno de la serie 2 se valida con éxito.
- El cuaderno de la serie 2 se ejecuta con éxito en el entorno local de verificación.
- Los archivos del cuaderno se mantienen sin salidas guardadas ni conteos de ejecución.
- No se comprometen secretos reales.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->