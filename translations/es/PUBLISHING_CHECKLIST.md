# Lista de verificación de publicación

Utilice esta lista de verificación antes de confirmar o enviar actualizaciones públicas.

## Seguridad

- Confirme que no hay claves API, tokens, contraseñas o puntos finales privados escritos en archivos Markdown, cuadernos, datos de muestra o scripts.
- Mantenga las credenciales en variables de entorno o identidad gestionada, no en archivos confirmados.
- No confirme archivos `.env` ni archivos de salida de cuadernos ejecutados.
- Mantenga `.env.example` solo como marcador de posición.

## Verificación

Ejecute el script de verificación del repositorio:

```powershell
python scripts\verify_notebooks.py
```

Ejecute la ejecución completa y segura localmente del cuaderno antes de publicar cambios de implementación:

```powershell
python scripts\verify_notebooks.py --execute
```

Verificaciones esperadas:

- pasan los enlaces Markdown locales
- pasa la validación JSON del cuaderno
- los cuadernos no contienen salidas guardadas ni conteos de ejecución
- pasa el escaneo de patrones de secretos de alto riesgo
- los cuadernos públicos se ejecutan localmente
- el material en borrador bajo `drafts/` se omite intencionadamente

## Revisión

- Confirme que los enlaces de los artículos README apuntan a los archivos previstos.
- Confirme que cada artículo tiene navegación del repositorio y enlaces a cuadernos relacionados.
- Confirme que los borradores no están enlazados desde índices públicos a menos que estén listos para publicar.
- Confirme que las plantillas de problemas y solicitudes de extracción de GitHub aún coinciden con el flujo de trabajo del repositorio.
- Confirme que los resultados de verificación en el artículo coinciden con la salida más reciente del cuaderno.
- Confirme que el flujo de trabajo de GitHub Actions se ejecuta después del push.
- Confirme que `CHANGELOG.md` refleja la actualización que se publica.
- Confirme que `CONTRIBUTING.md` aún coincide con el flujo de trabajo del repositorio.

## Git

- Revise `git status --short --branch`.
- Revise `git diff --stat`.
- Confirme y envíe solo cuando esté explícitamente listo.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Descargo de responsabilidad**:
Este documento ha sido traducido utilizando el servicio de traducción automática [Co-op Translator](https://github.com/Azure/co-op-translator). Aunque nos esforzamos por la precisión, tenga en cuenta que las traducciones automatizadas pueden contener errores o inexactitudes. El documento original en su idioma nativo debe considerarse la fuente autorizada. Para información crítica, se recomienda una traducción profesional humana. No somos responsables de cualquier malentendido o interpretación errónea que surja del uso de esta traducción.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->