#Project_3_Election_Sraper

#Imports
import csv
import sys

import bs4
import requests

#Get_territories
def get_territories_csv_format(page):
    try:
        #Basic_info
        base_infos = []
        table = page.find("div", id="inner").find("table")
        headers_appended = False
        code_header = table.find("th", class_="fixed45", id="t1sb1").text.title()
        name_header = table.find("th", class_="fixed150", id="t1sb2").text.title()
        for table in page.find("div", id="inner").find_all("table"):
            for tr in table.find_all("tr"):
                code = tr.find("td", class_="cislo")
                name = tr.find("td", class_="overflow_name")
                link = tr.find("td", class_="center")
                if code:
                    base_infos.append(
                        (code.a.text, name.text, "https://volby.cz/pls/ps2017nss/" + link.a['href']))
        #Get_municipalities
        territories = []
        for base_info in base_infos:
            base_info_url = base_info[2]
            base_info_page = get_page(base_info_url)
            if base_info_page.find("div", class_="in_940"):
                #For_publication_tables
                territory = []
                territory_links = base_info_page.find(
                    "div", id="publikace").find("table").find_all("td", class_="cislo")
                if territory_links:
                    for territory_link in territory_links:
                        territory_page = get_page("https://volby.cz/pls/ps2017nss/" + territory_link.a['href'])
                        if not headers_appended:
                            territories.append(get_headers_csv_format(code_header, name_header, territory_page))
                            headers_appended = True
                        territory1 = get_territory_csv_format(territory_page, base_info)
                        if not territory:
                            territory = territory1
                            continue
                        for index in range(len(territory1)):
                            if index > 1:
                                territory[index] = str(int("".join(territory[index].split())) + int(
                                    "".join(territory1[index].split())))
                territories.append(territory)
            else:
                if not headers_appended:
                    territories.append(get_headers_csv_format(code_header, name_header, base_info_page))
                    headers_appended = True
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

#Territories_basic_info
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

#Headers
def get_headers_csv_format(code_header, name_header, territory_page):
    table = territory_page.find("table")
    voters_header_br_tag = table.find("th", id="sa2").find("br")
    envelops_header_br_tag = table.find("th", id="sa3").find("br")
    valid_votes_header_br_tag = table.find("th", id="sa6").find("br")
    voters_header = voters_header_br_tag.previous_sibling + " " + voters_header_br_tag.next_sibling
    envelops_header = envelops_header_br_tag.previous_sibling + " " + envelops_header_br_tag.next_sibling
    valid_votes_header = valid_votes_header_br_tag.previous_sibling + " " + valid_votes_header_br_tag.next_sibling
    headers = [code_header, name_header, voters_header, envelops_header, valid_votes_header]
    party_name_headers = []
    parties_tables = territory_page.find("div", id="inner").find_all("table")
    for table_index in range(len(parties_tables)):
        parties_table = parties_tables[table_index]
        for party in parties_table.find_all("tr"):
            party_name_header = party.find("td", class_="overflow_name",
                                           headers="t" + str(table_index + 1) + "sa1 t" + str(table_index + 1) + "sb2")
            if party_name_header:
                party_name_headers.append(party_name_header.text)
    for item in party_name_headers:
        headers.append(item)
    return headers


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
