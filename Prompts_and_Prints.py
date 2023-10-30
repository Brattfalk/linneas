from Artefacts import *

class Prompts:
#Main menu: list users options and get answer as input. Return the answer and use it somehow.
    num_teams = None
    boat_type = None
    num_boats = None
    num_sailors = None
    @classmethod
    def main_menu(cls):
        while True:
            print("Välj ett alternativ:")
            print("1. Ange ett fixt antal deltagare.")
            print("2. Hämta deltagarlista.")
            print("3. Ange ett fixt antal lag.")

            choice = input("Ange ditt val (1, 2 eller 3): ")

            boat_type = input("Ange båttyp: ")
            num_boats = int(input("Ange antal båtar: "))

            return choice, boat_type, num_boats

    @classmethod
    def display_plan(cls, num_teams):
        sailing_org_instance = SailingOrganisation(cls.boat_type, cls.num_boats)
        if num_teams is None:
            cls.num_teams = sailing_org_instance.calc_num_team()
        lower_bound, upper_bound = sailing_org_instance.calc_team_size()

        if cls.num_teams <= cls.num_boats:
            num_on_water = cls.num_teams
            num_on_land = 0
        else:
            num_on_water = cls.num_boats
            num_on_land = cls.num_teams - num_on_water

        print(f"Vald båttyp: {cls.boat_type}")
        print(f"Antal båtar: {cls.num_boats}")
        if cls.num_sailors:
            print(f"Förväntade deltagare: {cls.num_sailors}")
        print(f"Totalt antal lag: {cls.num_teams}")
        print(f"Antal lag på vattnet: {num_on_water}")
        print(f"Antal lag på land: {num_on_land}")
        if lower_bound != upper_bound:
            print(f"Lagstorlek: {lower_bound}-{upper_bound} deltagare per lag")
        else:
            print(f"Lagstorlek: {lower_bound} deltagare per lag")

    @classmethod
    def show_results(cls):
        sorted_results = sorted(cls.results_data.items(), key=lambda x: x[1], reverse=True)
        for team, points in sorted_results:
            print(f"{team}: {points} poäng")

            """
            Presenterar resultattavlan.
            """
            # Sortera resultaten och visa dem, till exempel i fallande ordning.


