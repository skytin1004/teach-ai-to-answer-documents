# Cuadernos

Estos cuadernos apoyan la serie de artículos con ejemplos ejecutables.

| Cuaderno | Artículo | Propósito |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [Serie 2](../articles/series-2-open-source-rag-end-to-end.md) | RAG de código abierto con FastEmbed, modo local Qdrant, recuperación, reranking, generación opcional con Ollama y referencias a fuentes |

## Ejecutar localmente

Instala los requisitos para el cuaderno que quieres ejecutar:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

O instala todas las dependencias:

```powershell
python -m pip install -r requirements\all.txt
```

## Verificar

Desde la raíz del repositorio:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

La Serie 2 puede leer la configuración de Ollama desde un archivo `.env` en la raíz del repositorio. Comienza desde [../.env.example](../../../.env.example), que está agrupado por series.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->