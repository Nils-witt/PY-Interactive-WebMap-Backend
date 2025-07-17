grundzeichen_types = ("ohne", "taktische-formation", "befehlsstelle", "stelle", "ortsfeste-stelle", "person",
                      "gebaeude", "fahrzeug", "kraftfahrzeug-landgebunden", "kraftfahrzeug-gelaendegaengig",
                      "wechsellader", "abrollbehaelter", "anhaenger", "schienenfahrzeug", "kettenfahrzeug", "fahrrad",
                      "kraftrad", "wasserfahrzeug", "flugzeug", "hubschrauber", "massnahme", "anlass", "gefahr",
                      "gefahr-vermutet", "gefahr-akut",)


def get_grundzeichen_types():
    return {i: i for i in grundzeichen_types}


organisation_types = ("feuerwehr", "thw", "fuehrung", "polizei", "gefahrenabwehr", "hilfsorganisation", "bundeswehr")


def get_organisation_types():
    return {i: i for i in organisation_types}


fachaufgaben_types = ("brandbekaempfung", "hoehenrettung", "wasserversorgung", "technische-hilfeleistung", "heben",
                      "bergung", "raeumen", "entschaerfen", "sprengen", "beleuchtung", "transport", "abc", "messen",
                      "dekontamination", "dekontamination-personen", "dekontamination-geraete",
                      "umweltschaeden-gewaesser", "rettungswesen", "aerztliche-versorgung", "krankenhaus",
                      "einsatzeinheit", "betreuung", "seelsorge", "unterbringung", "logistik", "verpflegung",
                      "verbrauchsgueter", "versorgung-trinkwasser", "versorgung-brauchwasser",
                      "versorgung-elektrizitaet", "instandhaltung", "fuehrung", "iuk", "erkundung", "veterinaerwesen",
                      "schlachten", "wasserrettung", "wasserfahrzeuge", "rettungshunde", "pumpen",
                      "abwehr-wassergefahren", "warnen")


def get_fachaufgaben_types():
    return {i: i for i in fachaufgaben_types}


einheits_types = ("trupp", "staffel", "gruppe", "zug", "zugtrupp", "bereitschaft", "abteilung", "grossverband")


def get_einheits_types():
    return {i: i for i in einheits_types}


verwaltungsstufen_types = ("gemeinde", "kreis", "bezirk", "land", "brd", "eu")


def get_verwaltungsstufen_types():
    return {i: i for i in verwaltungsstufen_types}


funktion_types = ("fuehrungskraft", "sonderfunktion")


def get_funktion_types():
    return {i: i for i in funktion_types}


symbol_types = ("drehleiter", "hebegeraet", "bagger", "raeumgeraet", "bruecke", "sprengmittel", "beleuchtung", "bett",
                "verpflegung", "verbrauchsgueter", "trinkwasser", "brauchwasser", "elektrizitaet", "geraete",
                "sprengung", "bergung", "transport", "fahrzeug", "fahrrad", "kraftrad", "flugzeug", "hubschrauber",
                "entstehungsbrand", "fortentwickelter-brand", "vollbrand", "sirene", "lautsprecher", "warnung", "zelt",
                "sichten", "sammeln", "sammelplatz-betroffene", "veterinaerwesen", "schlachten", "tier-verletzt",
                "tier-tot", "person", "person-verletzt", "person-tot", "person-vermisst", "person-verschuettet",
                "person-gerettet", "person-zu-transportieren", "person-transportiert", "beschaedigt", "teilzerstoert",
                "zerstoert", "teilblockiert", "blockiert", "tendenz-steigend", "tendenz-fallend",
                "tendenz-unveraendert", "ausfall-25", "ausfall-50", "ausfall-75", "ausfall-100", "abc",
                "dekontamination", "dekontamination-personen", "dekontamination-geraete", "wasser", "wasserfahrzeug",
                "pumpe", "bilduebertragung", "bilduebertragung-funk", "datenuebertragung", "datenuebertragung-funk",
                "fax", "fax-funk", "fernsprechen", "fernsprechen-funk", "fernschreiben", "fernschreiben-funk",
                "festbilduebertragung", "festbilduebertragung-funk", "relaisfunkbetrieb", "richtbetrieb", "kabelbau",
                "vermutung", "akut", "technische-hilfeleistung", "seelsorge", "drohne")


def get_symbol_types():
    return {i: i for i in symbol_types}
