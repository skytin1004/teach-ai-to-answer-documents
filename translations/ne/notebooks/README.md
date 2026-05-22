# नोटबुकहरू

यी नोटबुकहरूले लेख श्रृंखला सँग चलाउन मिल्ने उदाहरणहरू समर्थन गर्छन्।

| नोटबुक | लेख | उद्देश्य |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [श्रृंखला २](../articles/series-2-open-source-rag-end-to-end.md) | FastEmbed, Qdrant स्थानीय मोड, पुनः प्राप्ति, पुनः श्रेणीकरण, वैकल्पिक Ollama उत्पादन, र स्रोत सन्दर्भहरूसँग खुला स्रोत RAG |

## स्थानीय रूपमा चलाउनुहोस्

तपाईंले चलाउन चाहनुभएको नोटबुकको लागि आवश्यकताहरू स्थापना गर्नुहोस्:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

वा सबै निर्भरताहरू स्थापना गर्नुहोस्:

```powershell
python -m pip install -r requirements\all.txt
```

## प्रमाणीकरण गर्नुहोस्

रिपोजिटोरी मुख्य फोल्डरबाट:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

श्रृंखला २ ले रिपोजिटोरी-मूल `.env` फाइलबाट Ollama कन्फिगरेसन पढ्न सक्छ। [../.env.example](../../../.env.example) बाट सुरु गर्नुहोस्, जुन श्रृंखलाहरू द्वारा समूहबद्ध गरिएको छ।

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
यो दस्तावेज़ AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरेर अनुवाद गरिएको हो। हामी सही हुन प्रयास गर्छौं, तर कृपया जानकार हुनुस् कि स्वचालित अनुवादमा त्रुटिहरू वा अशुद्धताहरू हुन सक्छन्। मूल दस्तावेज़ यसको मूल भाषामा आधिकारिक स्रोत मानिनुपर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलत बुझाइ वा त्रुटिको लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->