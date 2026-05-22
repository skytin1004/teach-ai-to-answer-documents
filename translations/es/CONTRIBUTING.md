# Contribuir

Este repositorio está organizado como una serie de blog más ejemplos de notebooks ejecutables.

## Antes de abrir un Pull Request

Ejecute el script local de validación:

```powershell
python scripts\verify_notebooks.py
```

Para cambios de implementación o notebooks, ejecute la ejecución local segura del notebook:

```powershell
python scripts\verify_notebooks.py --execute
```

## Directrices para Notebooks

- Mantenga los notebooks legibles y enfocados en el artículo relacionado.
- No comprometa las salidas guardadas del notebook ni los conteos de ejecución.
- Use datos de muestra pequeños de `sample_data/` a menos que el artículo requiera un recurso externo específico.
- Registre los resultados de verificación en el artículo relacionado cuando cambie el comportamiento.

## Secretos y Credenciales

- No comprometa claves API, tokens, contraseñas, endpoints privados ni archivos `.env`.
- Use `.env.example` solo para valores de marcador de posición.
- Use variables de entorno para experimentos opcionales locales con Ollama.

## Documentación

- Mantenga actualizados los enlaces de navegación del artículo.
- Actualice `README.md` al agregar un nuevo artículo, notebook, archivo de requerimientos o archivo de datos de muestra.
- Actualice `CHANGELOG.md` antes de publicar una actualización visible del repositorio.

## Verificación

El flujo de trabajo de GitHub Actions ejecuta:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

El material en borrador bajo `drafts/` es omitido por la verificación del repositorio hasta que esté listo para la indexación pública.

## Problemas

Use la plantilla de comentarios para artículos para correcciones de artículos y la plantilla de problemas para notebooks para problemas de ejecución del notebook.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->