# Lista kontrolna publikacji

Użyj tej listy kontrolnej przed zatwierdzeniem lub wypchnięciem publicznych aktualizacji.

## Bezpieczeństwo

- Potwierdź, że w plikach Markdown, notatnikach, przykładowych danych lub skryptach nie zapisano kluczy API, tokenów, haseł ani prywatnych punktów końcowych.
- Przechowuj poświadczenia w zmiennych środowiskowych lub zarządzanej tożsamości, nie w plikach zatwierdzonych.
- Nie zatwierdzaj plików `.env` ani wyników wykonania notatników.
- Plik `.env.example` powinien zawierać tylko symbole zastępcze.

## Weryfikacja

Uruchom skrypt weryfikacji repozytorium:

```powershell
python scripts\verify_notebooks.py
```

Przeprowadź pełne lokalne i bezpieczne wykonanie notatnika przed opublikowaniem zmian implementacyjnych:

```powershell
python scripts\verify_notebooks.py --execute
```

Oczekiwane kontrole:

- lokalne linki w Markdown przechodzą poprawnie
- walidacja JSON notatników przechodzi pomyślnie
- notatniki nie zawierają zapisanych wyników ani liczników wykonania
- skanowanie pod kątem wzorców wysokiego ryzyka tajnych danych przechodzi pomyślnie
- publiczne notatniki wykonują się lokalnie
- materiały w `drafts/` są celowo pomijane

## Recenzja

- Potwierdź, że linki w artykułach README wskazują na zamierzone pliki.
- Potwierdź, że każdy artykuł zawiera nawigację po repozytorium i powiązane linki do notatników.
- Potwierdź, że szkice nie są linkowane z publicznych indeksów, chyba że są gotowe do publikacji.
- Potwierdź, że szablony zgłoszeń i pull requestów na GitHub nadal odpowiadają przepływowi pracy repozytorium.
- Potwierdź, że wyniki weryfikacji w artykule odpowiadają najnowszemu wynikowi notatnika.
- Potwierdź, że workflow GitHub Actions powinien zostać uruchomiony po wypchnięciu.
- Potwierdź, że `CHANGELOG.md` odzwierciedla publikowaną aktualizację.
- Potwierdź, że `CONTRIBUTING.md` nadal odpowiada przepływowi pracy repozytorium.

## Git

- Sprawdź wynik `git status --short --branch`.
- Sprawdź wynik `git diff --stat`.
- Zatwierdzaj i wypychaj zmiany tylko, gdy jesteś wyraźnie gotowy.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Choć dążymy do dokładności, prosimy pamiętać, że automatyczne tłumaczenia mogą zawierać błędy lub niedokładności. Oryginalny dokument w jego języku źródłowym należy uznawać za autorytatywne źródło. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z użycia tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->