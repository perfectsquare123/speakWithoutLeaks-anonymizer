PSEUDO_DICT = {
    "PERSON": ["Aaron", "Bernice", "Cihui", "Daniel", "Eunice", "Horstann", "Ivan", "Racheal"],
    "GPE": ["Paris", "Berlin", "Tokyo", "Kuala Lumpur", "Beijing", "Seoul", "Bangkok", "Rome"],
    "ORG": ["Apple", "Google", "Huawei", "MIT", "NTU", "SAP", "Tsinghua"],
    "DATE": ["February 2,1965", "April 9,2001", "July 15,2003", "October 11,2004", "October 24,2023", "November 3,2018", "November 5,2019", "December 31,2002"]
}

GENERALIZE_DICT = {
    "PERSON": "given_name",
    "GPE": "country_name",
    "LOC": "location_name",
    "DATE": "01-01-2000",
    "TIME": "00:10:24",
    "EMAIL": "email@gmail.com",
    "CREDIT_CARD": "1234567890123456",
    "PHONE": "+1-234-567-8901",
    "MONEY": "1000 dollar"
}