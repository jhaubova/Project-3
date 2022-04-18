#Projekt_3_Election_Scraper
Tento projekt slouží k vyhodnocení výsledků voleb. 

#Popis
Funkcí programu je zpracovat pomocí scrapování výsledky voleb v roce 2017 v ČR  a to pro vybraný územní celek.
Skript z první stránky získá seznam obcí a informací s nimi spjatými, jako je jejich kód, název a odkaz na další detailnější přehled. Z něj pak získá další údaje potřebné ke splnění zadání (voliči v seznamu, vydané obálky, platné hlasy, kandidující strany). Výsledný seznam obcí pak skript uloží do souboru ve formátu csv.

#Requests
Pro posilani HTTP dotazu bylo nutné přes příkazovou řádku ve vývojovém prostředí nainstalovat modul requests pomocí příkazu 'pip install requests'.
Pro parsování odpovědi z HTTP dotazů bylo nutné nainstalovat přes příkazovou řádku ve vývojovém prostředí modul beatifulsoup4 pomocí příkazu 'pip install beautifulsoup4'.

#Spuštění
Uživatel spustí skript přes 2 argumenty:
1) příkaz 'python3 main.py "URL" (adresa územního celku)
2) "název souboru.csv", do kterého se mají uložit výsledky voleb.
Tedy konkrétně při spuštění příkazu 'python3 main.py "ttps://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107" a "volby_mlada_boleslav.csv"' se uživateli uloží výsledky voleb do souboru 'volby_mlada_boleslav.csv'. 
Při průběhu stahování senejprve stahujidata z vybraného url a ukládají se do souboru csv, následně se ukončuje scraper.

#Příklad_výsledku
code,location,registered,envelopes,ODS....
565750,Bílá Hlína,85,61,61,2,0,0,5,0,4,8,1,3,0,0,0,7,0,0,5,13,0,0,0,0,0,0,0,13,0.
