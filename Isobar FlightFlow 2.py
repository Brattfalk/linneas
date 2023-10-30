from Artefacts import *
from Prompts_and_Prints import Prompts

boat_type_library_instance = BoatTypeLibrary()
boat_type_library_instance.load_boat_types()

def main():
    print("Välkommen till Sprintsegling Organiserare!")

    answer = input("\nVill du organisera en regatta? Svara [Ja]/[Nej]: ")

    if answer.lower() == "ja":
        choice, boat_type, num_boats = Prompts.main_menu()
        if choice == "1":
            expected_sailors(boat_type, num_boats)
        elif choice == "2":
            get_names(boat_type, num_boats)
        elif choice == "3":
            num_teams(boat_type, num_boats)
        else:
            print("Ogiltigt val, vänligen försök igen.")

    else:
        print("Programmet avslutas, välkommen tillbaka till Isobar FlightFlow!")
        exit()

    while True:
        choice, boat_type, num_boats = Prompts.main_menu()
        boat_type = lookup_boat_type(boat_type)

        if boat_type is None:
            print(f"Fel: Båttyp '{boat_type}' hittades inte i databasen.")
            retry = input("Vill du försöka igen? (ja/nej): ").strip().lower()
            if retry == 'nej':
                return
        else:
            break

    Prompts.display_plan(num_teams)

def lookup_boat_type(boat_type):
    return boat_type_library_instance.find_boat_type(boat_type)


def expected_sailors(boat_type, num_boats):  # För choise == 1
    num_sailors = int(input("Ange förväntat antal deltagare: "))
    return boat_type, num_boats, num_sailors


def get_names(boat_type, num_boats):  # För choise == 2
    if sailors.json.import_file("deltagare2.txt"):
        num_sailors = range(sailors.json.names)
        print(f"{num_sailors} deltagare importerade framgångsrikt!")
        return boat_type, num_boats, num_sailors
    else:
        print("Det gick inte att läsa in filen.")
        pass


def num_teams(boat_type, num_boats):  # För choise == 3
    num_teams = int(input("Ange totalt antal lag: "))
    return boat_type, num_boats, num_teams


if __name__ == "__main__":
    main()
