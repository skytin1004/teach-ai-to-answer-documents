# Naučite umetno inteligenco odgovarjati na vprašanja na podlagi vaših dokumentov

Ta repozitorij zbira serijo blogov iz leta 2026 o gradnji inteligentnih sistemov, podprtih z dokumenti, z uporabo RAG, Azure AI storitev, odprtokodnih alternativ in delovnih procesov, usmerjenih v evalvacijo.

## Ozadje

Leta 2023 sem delal na paru vodičev o tem, kako naučiti ChatGPT odgovarjati na vprašanja iz PDF dokumentov z uporabo Azure AI Search in Azure OpenAI. Ideja "ChatGPT na vaših podatkih" je takrat še delovala nova, cilj pa je bil pokazati praktičen delovni proces: shranjevanje dokumentov, indeksiranje, pridobivanje relevantne vsebine in generiranje odgovorov iz pridobljenega konteksta.

Leta 2026 je RAG ekosistem veliko večji. Azure AI Search podpira sodobne vzorce pridobivanja vektorjev in hibridnega iskanja, Azure OpenAI je del širšega ekosistema Microsoft Foundry Models, odprtokodna orodja kot so LangGraph, LlamaIndex, Haystack, Qdrant, Milvus, Weaviate, Chroma, Ollama in vLLM pa so postala praktične izbire za resnične sisteme.

Zato sem želel to temo ponovno obravnavati. Vprašanje ni več samo "Kako zgradim RAG?" Obstaja namreč mnogo načinov za gradnjo, pomembneje pa je vprašanje "Katero arhitekturo naj izberem za svojo situacijo?"

Ta serija se začne pri tej plasti odločanja. Preden se poglobite v implementacijo, si ogleda, zakaj AI storitve potrebujejo iskanje, kdaj so Azure-jeve upravljane storitve smiselne, kdaj so odprtokodne alternative bolj primerne in kje je smiselno fino urjenje.

## Članki

1. [Serija 1: RAG, Azure proti odprtokodnim alternativam in kdaj je fino urjenje smiselno](./series-1-rag-azure-open-source-fine-tuning.md)

## Podpora za več jezikov

### Podprto prek Co-op Translator (avtomatizirano in vedno posodobljeno)

<!-- CO-OP TRANSLATOR LANGUAGES TABLE START -->
[Arabščina](../ar/README.md) | [Bengalščina](../bn/README.md) | [Bolgarščina](../bg/README.md) | [Burmansko (Myanmar)](../my/README.md) | [Kitajščina (poenostavljena)](../zh-CN/README.md) | [Kitajščina (tradicionalna, Hong Kong)](../zh-HK/README.md) | [Kitajščina (tradicionalna, Macau)](../zh-MO/README.md) | [Kitajščina (tradicionalna, Tajvan)](../zh-TW/README.md) | [Hrvaščina](../hr/README.md) | [Češčina](../cs/README.md) | [Danščina](../da/README.md) | [Nizozemščina](../nl/README.md) | [Estonščina](../et/README.md) | [Finščina](../fi/README.md) | [Francoščina](../fr/README.md) | [Nemščina](../de/README.md) | [Grščina](../el/README.md) | [Hebrejščina](../he/README.md) | [Hindujščina](../hi/README.md) | [Madžarščina](../hu/README.md) | [Indonezijščina](../id/README.md) | [Italijanščina](../it/README.md) | [Japonščina](../ja/README.md) | [Kannada](../kn/README.md) | [Khmerščina](../km/README.md) | [Korejščina](../ko/README.md) | [Litvanščina](../lt/README.md) | [Malezijščina](../ms/README.md) | [Malayalam](../ml/README.md) | [Maratščina](../mr/README.md) | [Nepalščina](../ne/README.md) | [Nigerijski pidžin](../pcm/README.md) | [Norveščina](../no/README.md) | [Perzijščina (Farsi)](../fa/README.md) | [Poljščina](../pl/README.md) | [Portugalščina (Brazilija)](../pt-BR/README.md) | [Portugalščina (Portugalska)](../pt-PT/README.md) | [Pandžabščina (Gurmukhi)](../pa/README.md) | [Romunščina](../ro/README.md) | [Ruščina](../ru/README.md) | [Srbščina (cirilica)](../sr/README.md) | [Slovaščina](../sk/README.md) | [Slovenščina](./README.md) | [Španščina](../es/README.md) | [Svahili](../sw/README.md) | [Švedščina](../sv/README.md) | [Tagalog (Filipino)](../tl/README.md) | [Tamilščina](../ta/README.md) | [Telugu](../te/README.md) | [Tajščina](../th/README.md) | [Turščina](../tr/README.md) | [Ukrajinščina](../uk/README.md) | [Urdu](../ur/README.md) | [Vietnamščina](../vi/README.md)

> **Raje klonirate lokalno?**
>
> Ta repozitorij vključuje več kot 50 prevodov jezikov, kar znatno poveča velikost prenosa. Za kloniranje brez prevodov uporabite sparse checkout:
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
> Tako boste dobili vse, kar potrebujete za dokončanje tečaja z bistveno hitrejšim prenosom.
<!-- CO-OP TRANSLATOR LANGUAGES TABLE END -->

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo AI prevajalske storitve [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas prosimo, da upoštevate, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku je treba obravnavati kot avtoritativni vir. Za kritične informacije je priporočljiv strokovni človeški prevod. Ne odgovarjamo za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->