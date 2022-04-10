import csv
import sys

import bs4
import requests


def get_territories_csv_format(page):
    try:
        # zakladni informace o obcich
        base_infos = []
        for table in page.find("div", id="inner").find_all("table"):
            for tr in table.find_all("tr"):
                code = tr.find("td", class_="cislo")
                name = tr.find("td", class_="overflow_name")
                link = tr.find("td", class_="center")
                if code:
                    base_infos.append(
                        (code.a.text, name.text, "https://volby.cz/pls/ps2017nss/" + link.a['href']))
        # uzemni celky se vsemi udaji
        territories = []
        for base_info in base_infos:
            base_info_url = base_info[2]
            base_info_page = get_page(base_info_url)
            if base_info_page.find("div", class_="in_940"):
                # for publikace_table in publikace_tables:
                territory = []
                territory_links = base_info_page.find(
                    "div", id="publikace").find("table").find_all("td", class_="cislo")
                if territory_links:
                    for territory_link in territory_links:
                        territory1 = get_territory_csv_format(
                            get_page("https://volby.cz/pls/ps2017nss/" + territory_link.a['href']), base_info)
                        if not territory:
                            territory = territory1
                            continue
                        for index in range(len(territory1)):
                            if index > 1:
                                territory[index] = str(int("".join(territory[index].split())) + int(
                                    "".join(territory1[index].split())))
                territories.append(territory)
            else:
                territories.append(get_territory_csv_format(base_info_page, base_info))
        return territories
    except:
        quit("Chyba pri ziskavani vysledku")


def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            quit("Kod z odpovedi stranky neni OK")
        try:
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            return soup
        except:
            quit("Stranka nelze parsovat")
    except:
        quit("Spatna URL")


def get_territory_csv_format(territory_page, base_info):
    table = territory_page.find("table")
    voters = table.find("td", class_="cislo", headers="sa2").text
    envelops = table.find("td", class_="cislo", headers="sa3").text
    valid_votes = table.find("td", class_="cislo", headers="sa6").text
    territory_csv_format = [base_info[0], base_info[1], voters, envelops, valid_votes]
    # pocet platnych hlasu stran
    parties = []
    parties_tables = territory_page.find("div", id="inner").find_all("table")
    for table_index in range(len(parties_tables)):
        parties_table = parties_tables[table_index]
        for party in parties_table.find_all("tr"):
            party_valid_votes = party.find("td", class_="cislo", headers="t" + str(table_index + 1) + "sa2 t" + str(
                table_index + 1) + "sb3")
            if party_valid_votes:
                parties.append(party_valid_votes.text)
    for item in parties:
        territory_csv_format.append(item)
    return territory_csv_format


if __name__ == "__main__":
    try:
        url = str(sys.argv[1])
        name = str(sys.argv[2])
    except:
        quit("Spatne zadane argumenty")
    else:
        if not url:
            quit("Prazdna URL adresa")
        elif not name:
            quit("Prazdny nazev souboru")
        else:
            territories_csv_format = get_territories_csv_format(get_page(url))
            try:
                file = open(name, 'w')
                try:
                    writer = csv.writer(file)
                    writer.writerows(territories_csv_format)
                except:
                    quit("Chyba pri ukladani souboru")
                finally:
                    file.close()
            except:
                quit("Chyba writeru")
