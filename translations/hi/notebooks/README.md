# नोटबुक

ये नोटबुक रन करने योग्य उदाहरणों के साथ लेख श्रृंखला का समर्थन करती हैं।

| नोटबुक | लेख | उद्देश्य |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [शृंखला 2](../articles/series-2-open-source-rag-end-to-end.md) | FastEmbed, Qdrant स्थानीय मोड, पुनःप्राप्ति, पुनःरैंकिंग, वैकल्पिक Ollama जेनेरेशन, और स्रोत संदर्भों के साथ ओपन-सोर्स RAG |

## स्थानीय रूप से चलाएं

उस नोटबुक के लिए आवश्यकताओं को स्थापित करें जिसे आप चलाना चाहते हैं:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

या सभी निर्भरताओं को स्थापित करें:

```powershell
python -m pip install -r requirements\all.txt
```

## सत्यापित करें

रिपोजिटरी रूट से:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

शृंखला 2 रिपोजिटरी-रूट `.env` फ़ाइल से Ollama कॉन्फ़िगरेशन पढ़ सकती है। [../.env.example](../../../.env.example) से शुरुआत करें, जो श्रृंखलाओं के अनुसार समूहित है।

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
इस दस्तावेज़ का अनुवाद AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके किया गया है। जबकि हम सटीकता के लिए प्रयास करते हैं, कृपया ध्यान दें कि स्वचालित अनुवादों में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सिफारिश की जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम उत्तरदायी नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->