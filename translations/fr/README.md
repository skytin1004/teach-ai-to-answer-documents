# Enseigner à l'IA à répondre aux questions basées sur vos documents

Ce référentiel rassemble une série de blogs de 2026 sur la construction de systèmes d'IA basés sur des documents avec RAG, les services Azure AI, des alternatives open-source, et des workflows orientés évaluation.

## Contexte

En 2023, j'ai travaillé sur une paire de tutoriels sur l'enseignement à ChatGPT de répondre aux questions à partir de documents PDF en utilisant Azure AI Search et Azure OpenAI. L'idée de "ChatGPT sur vos données" semblait encore nouvelle à l'époque, et le but était de montrer un workflow pratique : stocker les documents, les indexer, récupérer le contenu pertinent, et générer des réponses à partir de ce contexte récupéré.

En 2026, l'écosystème RAG est beaucoup plus vaste. Azure AI Search supporte des schémas modernes de récupération vectorielle et hybride, Azure OpenAI fait partie de l'écosystème plus large Microsoft Foundry Models, et des outils open-source tels que LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama, et vLLM sont devenus des choix pratiques pour des systèmes réels.

C'est pourquoi je voulais revisiter ce sujet. La question n'est plus seulement "Comment construire un RAG ?" Il existe désormais de nombreuses façons de le construire, et la question la plus importante est "Quelle architecture devrais-je choisir pour ma situation ?"

Cette série commence à partir de cette couche de prise de décision. Avant de plonger profondément dans l'implémentation, elle examine pourquoi les services IA ont besoin de récupération, quand les services managés basés sur Azure ont du sens, quand les alternatives open-source sont mieux adaptées, et où le fine-tuning s'insère.

## Articles

1. [Série 1 : RAG, Azure vs Alternatives Open-Source, et Quand le Fine-Tuning A du Sens](./series-1-rag-azure-open-source-fine-tuning.md)

## Support Multilingue

### Pris en charge via Co-op Translator (Automatisé et Toujours à Jour)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabe](../ar/README.md) | [Bengali](../bn/README.md) | [Bulgare](../bg/README.md) | [Birman (Myanmar)](../my/README.md) | [Chinois (Simplifié)](../zh-CN/README.md) | [Chinois (Traditionnel, Hong Kong)](../zh-HK/README.md) | [Chinois (Traditionnel, Macao)](../zh-MO/README.md) | [Chinois (Traditionnel, Taïwan)](../zh-TW/README.md) | [Croate](../hr/README.md) | [Tchèque](../cs/README.md) | [Danois](../da/README.md) | [Néerlandais](../nl/README.md) | [Estonien](../et/README.md) | [Finnois](../fi/README.md) | [Français](./README.md) | [Allemand](../de/README.md) | [Grec](../el/README.md) | [Hébreu](../he/README.md) | [Hindi](../hi/README.md) | [Hongrois](../hu/README.md) | [Indonésien](../id/README.md) | [Italien](../it/README.md) | [Japonais](../ja/README.md) | [Kannada](../kn/README.md) | [Khmer](../km/README.md) | [Coréen](../ko/README.md) | [Lituanien](../lt/README.md) | [Malais](../ms/README.md) | [Malayalam](../ml/README.md) | [Marathi](../mr/README.md) | [Népalais](../ne/README.md) | [Pidgin Nigérian](../pcm/README.md) | [Norvégien](../no/README.md) | [Persan (Farsi)](../fa/README.md) | [Polonais](../pl/README.md) | [Portugais (Brésil)](../pt-BR/README.md) | [Portugais (Portugal)](../pt-PT/README.md) | [Pendjabi (Gurmukhi)](../pa/README.md) | [Roumain](../ro/README.md) | [Russe](../ru/README.md) | [Serbe (Cyrillique)](../sr/README.md) | [Slovaque](../sk/README.md) | [Slovène](../sl/README.md) | [Espagnol](../es/README.md) | [Swahili](../sw/README.md) | [Suédois](../sv/README.md) | [Tagalog (Philippin)](../tl/README.md) | [Tamoul](../ta/README.md) | [Télougou](../te/README.md) | [Thaï](../th/README.md) | [Turc](../tr/README.md) | [Ukrainien](../uk/README.md) | [Ourdou](../ur/README.md) | [Vietnamien](../vi/README.md)

> **Préférez cloner localement ?**
>
> Ce référentiel inclut plus de 50 traductions ce qui augmente considérablement la taille du téléchargement. Pour cloner sans les traductions, utilisez le sparse checkout :
>
> **Bash / macOS / Linux :**
> ```bash
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone '/*' '!translations' '!translated_images'
> ```
>
> **CMD (Windows) :**
> ```cmd
> git clone --filter=blob:none --sparse https://github.com/skytin1004/teach-ai-to-answer-documents.git
> cd teach-ai-to-answer-documents
> git sparse-checkout set --no-cone "/*" "!translations" "!translated_images"
> ```
>
> Cela vous donne tout ce dont vous avez besoin pour compléter le cours avec un téléchargement beaucoup plus rapide.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Avertissement** :
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforçions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue native doit être considéré comme la source faisant autorité. Pour les informations critiques, il est recommandé de recourir à une traduction professionnelle réalisée par un humain. Nous ne saurions être tenus responsables des malentendus ou erreurs d'interprétation découlant de l'utilisation de cette traduction.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->