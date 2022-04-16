#Projekt
Elections scrapper. Tento projekt slouží k vyhodnocení výsledků voleb v roce 2017 v ČR. 

##Popis
Funkcí programu je zpracovat pomocí scrapování výsledky voleb pro vybraný územní celek.
Skript z první stránky získá seznam obcí a informací s nimi spjatými, jako je jejich kód, název a odkaz na další detailnější přehled. Z něj pak získá další údaje potřebné ke splnění zadání (voliči v seznamu, vydané obálky, platné hlasy, kandidující strany). Výsledný seznam obcí pak skript uloží do souboru ve formátu csv.

#Requests
Pro posilani HTTP dotazu bylo nutné přes příkazovou řádku ve vývojovém prostředí nainstalovat modul requests pomocí příkazu 'pip install requests'.
Aby bylo možné parsovat odpovědi z HTTP dotazů, bylo potřeba nainstalovat přes příkazovou řádku ve vývojovém prostředí modul beatifulsoup4 pomocí příkazu 'pip install beautifulsoup4'.

#Spuštění skriptu "Výsledky hlasování pro okres Mladá Boleslav"
Uživatel spustí skript přes 2 argumenty, 1) příkaz 'python3 main.py "URL" a 2) "název souboru.csv"', kde 'URL' je adresa územního celku a 'název souboru.csv' je název CSV souboru, do kterého se mají uložit výsledky voleb.
Tedy konkrétně při spuštění příkazu 'python3 main.py "https://volby.cz/pls/ps2017nss/ps31?xjazyk=CZ&xkraj=2&xnumnuts=2107" a "volby_mlada_boleslav.csv"' se uživateli uloží výsledky voleb do souboru 'volby_mlada_boleslav.csv'. 
Při průběhu stahování senejprve stahujidata z vybraného url a ukládají se do souboru csv, následně se ukončuje scraper.

#Příklad výsledku
code,location,registered,envelopes,ODS
35443,Bělá pod Bezdězem,3805,2219,2204
