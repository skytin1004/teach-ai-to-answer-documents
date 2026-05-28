# Scripts

Esta carpeta contiene scripts de verificación del repositorio.

## `verify_notebooks.py`

Valida enlaces Markdown locales, JSON de notebooks, limpieza de la salida de notebooks y patrones de secretos de alto riesgo:

```powershell
python scripts\verify_notebooks.py
```

Ejecuta todos los notebooks públicos seguros locales:

```powershell
python scripts\verify_notebooks.py --execute
```

El flujo de trabajo de GitHub Actions usa el mismo script.

El material borrador en `drafts/` se omite hasta que esté listo para el índice público.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->