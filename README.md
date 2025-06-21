# Projekt: Zarządzanie firmą kurierską

**Autorzy**: Kajetan Gołucki, Maksym Kushta   

**Grupa**: 2ID12A 

**Prowadzący**: dr inż. Dariusz Michalski  

**Data oddania**: 22-06-2025  

## Cel projektu

Celem projektu jest stworzenie prostego systemu do zarządzania paczkami, kierowcami i trasami w firmie kurierskiej, z zastosowaniem elementów programowania obiektowego, funkcyjnego i obsługi plików.

## Funkcjonalności

- Dodawanie paczek i kierowców
- Tworzenie tras dostaw
- Zapis danych do pliku JSON i TXT
- Analiza czasu trasy (map/lambda)
- Statystyki paczek (set, dict, tuple)
- Edycja i wyszukiwanie danych
- Obsługa błędów i walidacja danych
- Testy i asercje

## Struktura projektu
projekt_kurier :
- main.py # Główna logika, menu
- models.py # Klasy: Package, Driver, Route
- utils.py # Funkcje pomocnicze: load/save
- data.json # Dane paczek i kierowców
- README.md # Opis projektu
- trasa_R001.json # Przykładowy plik trasy
