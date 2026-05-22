# नोटबुक्स

हे नोटबुक्स लेख मालिकेसाठी चालवता येणाऱ्या उदाहरणांसह समर्थन करतात.

| नोटबुक | लेख | उद्दिष्ट |
| --- | --- | --- |
| [series-2-open-source-rag.ipynb](./series-2-open-source-rag.ipynb) | [सिरीज 2](../articles/series-2-open-source-rag-end-to-end.md) | FastEmbed, Qdrant लोकल मोड, पुनर्प्राप्ती, पुनर्रँकिंग, ऐच्छिक Ollama निर्मिती, आणि स्रोत संदर्भांसह खुल्या स्रोताचा RAG |

## स्थानिकदृष्ट्या चालवा

आपण चालवू इच्छित असलेल्या नोटबुकसाठी आवश्यकताएं इंस्टॉल करा:

```powershell
python -m venv .venv-series2
.\.venv-series2\Scripts\activate
python -m pip install -r requirements\open-source-rag.txt
```

किंवा सर्व अवलंबने इंस्टॉल करा:

```powershell
python -m pip install -r requirements\all.txt
```

## पडताळणी करा

रेपॉझिटरी मूळगटून:

```powershell
python scripts\verify_notebooks.py
python scripts\verify_notebooks.py --execute
```

सिरीज 2 Ollama कॉन्फिगरेशन रेपॉझिटरी-मुळ `.env` फाईलमधून वाचू शकते. [../.env.example](../../../.env.example) पासून प्रारंभ करा, जे सिरीज नुसार गटबद्ध केलेले आहे.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI भाषांतर सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) चा वापर करून अनुवादित केला आहे. जरी आम्ही अचूकतेसाठी प्रयत्न करतो, तरी कृपया लक्षात घ्या की स्वयंचलित भाषांतरांमध्ये त्रुटी किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या मूळ भाषेत अधिकृत स्रोत मानला पाहिजे. महत्त्वाची माहिती असल्यास, व्यावसायिक मानवी भाषांतराची शिफारस केली जाते. या भाषांतराच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमज किंवा चुकीच्या अर्थलावणीसाठी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->