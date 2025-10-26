import argparse
import sys

def generuj_strukture(trojki):
    print("\n[INFO] Generuję strukturę katalogów...")
    for m, d, p in trojki:
        print(f"  -> {m}/{d}/{p}")
        # TODO os 2
    print("[OK] Struktura wygenerowana (symulacja).")


# Te 4 funkcje (mozna 2 jak nie robimy jsonow) TODO os 3

def zapisz_csv():
    print("[INFO] Tworzę pliki CSV... (symulacja)")

def odczytaj_csv():
    print("[INFO] Odczytuję pliki CSV... (symulacja)")

def zapisz_json():
    print("[INFO] Tworzę pliki JSON... (symulacja)")

def odczytaj_json():
    print("[INFO] Odczytuję pliki JSON... (symulacja)")

DNI = ["pn", "wt", "sr", "czw", "pt", "sb", "nd"]

def rozszerz_kod(kod):
    """
    Rozszerza kod dnia:
      - "pn" -> ["pn"]
      - "pn-wt" -> ["pn", "wt"]
      - "pn-pt" -> ["pn","wt","sr","czw","pt"]
    Rzuca ValueError jeśli kod jest niepoprawny.
    """
    kod = kod.strip().lower()
    if "-" in kod:
        krance = kod.split("-")
        if len(krance) != 2:
            raise ValueError(f"Nieprawidłowy zakres dni: '{kod}'")
        pocz, kon = krance[0], krance[1]
        if pocz not in DNI or kon not in DNI:
            raise ValueError(f"Nieznany dzień w zakresie: '{kod}'. Dozwolone: {DNI}")
        ind_pocz, ind_kon = DNI.index(pocz), DNI.index(kon)
        if ind_pocz <= ind_kon:
            return DNI[ind_pocz:ind_kon+1]
        else:
            # jeśli ktoś poda np. "wt-pn" uznajemy, że cyklicznie przechodzimy przez koniec tygodnia
            return DNI[ind_pocz:] + DNI[:ind_kon+1]
    else:
        if kod not in DNI:
            raise ValueError(f"Nieznany dzień: '{kod}'. Dozwolone: {DNI}")
        return [kod]

def rozszerz_liste_kodow(lista_kodow):
    wynik = []
    for kod in lista_kodow:
        wynik.append(rozszerz_kod(kod))
    return wynik

def uprosc_strukture(miesiace, dni, pory):
    """
    Przyjmujemy:
      - miesiace: lista nazw miesiecy (len M)
      - dni: lista kodow dni (len M)
      - pory_tokens: lista pór, które ma być przypisane do wszystkich rozwiniętych dni
    Zwraca listę tuple (miesiac, dzien, pora)
    """
    if len(miesiace) != len(dni):
        raise ValueError("Liczba elementów w --miesiace musi być równa liczbie elementów w --dni.")

    dni_na_miesiac = rozszerz_liste_kodow(dni)
    ile_dni = sum(len(lst) for lst in dni_na_miesiac)

    # Wydluzam pory
    if not pory:
        pory = ["r"] * ile_dni
    else:
        for i in range(len(pory)):
            pory[i] = pory[i].strip().lower()
            if (pory[i] not in ["w", "r"]):
                raise ValueError(f"Niepoprawna pora dnia ({pory[i]}). Dozwolone: {["r", "w"]}")
        if len(pory) > ile_dni:
            raise ValueError(f"Podano więcej pór ({len(pory)}) niż dni ({ile_dni}).")
        pory += ["r"] * (ile_dni - len(pory))
        
    # Dopasowywuje dni do miesiecy
    wynik = []
    ind_p = 0
    for i in range(len(miesiace)):
        for j in dni_na_miesiac[i]:
            wynik.append((miesiace[i], j, pory[ind_p]))
            ind_p += 1

    return wynik

def main():
    parser = argparse.ArgumentParser(
        description="Skrypt do tworzenia lub odczytywania plików danych (csv/json) "
                    "w strukturze katalogów miesiąc/dzień/pora."
    )

    # a) wybór miesięcy
    parser.add_argument(
        "-m", "--miesiace",
        nargs="+",
        required=True,
        help="Lista miesięcy, np. -m styczeń luty"
    )

    # b) wybór dni tygodnia
    parser.add_argument(
        "-d", "--dni",
        nargs="+",
        required=True,
        help="Zakresy dni tygodnia, np. -d pn-wt pt"
    )

    # c) wybór pory dnia (rano/wieczór)
    parser.add_argument(
        "-p", "--pory",
        nargs="*",
        default=None,
        help="Pory dnia (r - rano, w - wieczór). Domyślnie wszystkie = rano."
    )

    # d) tryb tworzenia / odczytu
    parser.add_argument(
        "-t", "--tworzenie",
        action="store_true",
        help="Tryb tworzenia plików (domyślnie odczyt)."
    )

    # e) wybór formatu pliku
    parser.add_argument(
        "-f", "--format",
        choices=["csv", "json"],
        default="csv",
        help="Format pliku: csv lub json (domyślnie csv)."
    )

    args = parser.parse_args()

    # === Informacje diagnostyczne ===
    print("\n===== Parametry uruchomienia =====")
    print(f"Miesiące: {args.miesiace}")
    print(f"Dni:      {args.dni}")
    print(f"Pory:     {args.pory}")
    print(f"Tryb:     {'tworzenie' if args.tworzenie else 'odczyt'}")
    print(f"Format:   {args.format}")
    print("==================================\n")

    try:
        trojki = uprosc_strukture(args.miesiace, args.dni, args.pory)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(2)

    print(trojki)

    # === Wywołanie odpowiednich funkcji ===
    generuj_strukture(trojki)

    if args.tworzenie:
        if args.format == "csv":
            zapisz_csv()
        else:
            zapisz_json()
    else:
        if args.format == "csv":
            odczytaj_csv()
        else:
            odczytaj_json()


if __name__ == "__main__":
    main()