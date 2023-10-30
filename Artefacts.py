from typing import Dict, Any
import json
import math


class Sailor:
    def __init__(self):  # Initierar en lista av seglare.
        self.sailors = []

    def save_to_json(self):  # Sparar listan av seglare till en JSON-fil.
        with open("sailors.json", "w") as f:
            json.dump(self.sailors, f)

    def load_sailors(self):  # Laddar en lista av seglare från en JSON-fil. Om filen inte finns, initieras en tom lista.
        try:
            with open("sailors.json", "r") as f:
                self.sailors = json.load(f)
        except FileNotFoundError:
            self.sailors = []

    def import_file(self, filename):  # Importerar namn av seglare från en fil till listan av seglare. Sparas till JSON.
        try:
            with open(filename, 'r') as f:
                names = f.read().splitlines()
            for name in names:
                sailor_id = len(self.sailors) + 1
                self.sailors.append({"sailor_id": sailor_id, "name": name})
            self.save_to_json()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    # Begära namn från användaren, lägger till ett spec. antal seglare manuellt. Listan sparas till en JSON-fil.
    def add_sailors_manually(self, num_sailors):
        for i in range(num_sailors):
            name = input(f"Ange namn för deltagare {i + 1}: ")
            sailor_id = len(self.sailors) + 1
            self.sailors.append({"sailor_id": sailor_id, "name": name})
        self.save_to_json()

    # Lägger till ett spec. antal anonyma seglare till listan. Sparas som "Sailor 1", "Sailor 2", osv till en JSON-fil.
    def create_anonymous(self, num_sailors):
        for i in range(num_sailors):
            sailor_id = len(self.sailors) + 1
            self.sailors.append({"sailor_id": sailor_id, "name": f"Sailor {sailor_id}"})
        self.save_to_json()

# Example usage:
# sailor_obj = Sailor()
# sailor_obj.load_sailors()  # Load existing sailors from JSON
# sailor_obj.create_anonymous(5)  # Create 5 anonymous sailors
# print(sailor_obj.sailors)  # Print all sailors

class Team:
    def __init__(self, name):
        self.name = name
        self.sailors = []
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    @staticmethod
    def create_teams_from_sailors(sailor_obj, num_teams, filename="teams.json"):
        sailors = sailor_obj.sailors
        teams = []
        i = 0

        for _ in range(num_teams):
            team = Team(f"Team {_ + 1}")
            while i < len(sailors):
                team.sailors.append(sailors[i])
                i += 1
                if i % num_teams == 0:
                    break
            teams.append(team.__dict__)

        with open(filename, 'w') as f:
            json.dump(teams, f)

        return teams


class Boat:
    def __init__(self, name, boat_type):
        self.boat_type = boat_type
        self.name = name


class BoatType:
    def __init__(self, name, min_crew, max_crew, opti_crew):
        self.name = name
        self.min_crew = min_crew
        self.max_crew = max_crew
        self.opti_crew = opti_crew


class Schedule:
    def __init__(self, races):
        self.races = races


class RaceResult:
    def __init__(self, race, place):
        self.race = race
        self.place = place

class Results:
    def __init__(self):
        self.results_data = {}

    def update_results(self, team, points):
        """
        Uppdaterar resultattavlan med ett lags prestation.
        """
        self.results_data[team.name] = points

    def get_results(self, team):
        """
        Returnerar resultatet för ett specifikt lag.
        """
        return self.results_data.get(team.name, None)

    def show_results(self):
        """
        Presenterar resultattavlan.
        """
        # Sortera resultaten och visa dem, till exempel i fallande ordning.
        sorted_results = sorted(self.results_data.items(), key=lambda x: x[1], reverse=True)
        for team, points in sorted_results:
            print(f"{team}: {points} poäng")


class Race:
    def __init__(self, name):
        self.name = name
        self.result = None


class BoatTypeLibrary:
    def __init__(self, filename="boat_types.json"):
        self.filename = filename
        self.load_boat_types()
        self.boats = {}

    def find_boat_type(self, name):
        return self.boats.get(name, None)

    def load_boat_types(self):
        try:
            with open(self.filename, 'r') as f:
                self.boats = json.load(f)
        except FileNotFoundError:
            self.boats = {}

    def add_boat_types(self, boat_type, opti_crew):
        try:
            if not boat_type:
                boat_type = input("Ange båttyp: ")
            if not opti_crew:
                opti_crew = int(input(f"Ange optimal besättningsstorlek för {boat_type}: "))
            self.save_boat_data(boat_type, opti_crew)
        except KeyError:
            print(f"Fel: Kunde inte lägga till eller uppdatera data för båttyp {boat_type}.")

    def get_boat_data(self, boat_type):
        boat_data = self.boats.get(boat_type)
        if boat_data:
            return boat_type, boat_data.get("opti_crew")
        return None, None

    def calc_crew(self, opti_crew):
        min_crew = opti_crew - 1 if opti_crew > 1 else 1
        max_crew = opti_crew + 1
        return min_crew, max_crew

    def save_boat_data(self, boat_type: object, opti_crew: float) -> None:
        min_crew, max_crew = self.calc_crew(opti_crew)
        self.boats[boat_type] = {
            "opti_crew": opti_crew,
            "min_crew": min_crew,
            "max_crew": max_crew
        }
        self.save_boat_type()

    def save_boat_type(self):
        with open(self.filename, 'w') as f:
            json.dump(self.boats, f)


class SailingOrganisation:
    def __init__(self, boat_type: str, num_boats: int, num_sailors: int = None, num_teams: int = None):
        self.boat_type = boat_type
        self.num_boats = num_boats
        self.num_sailors = num_sailors
        self.num_teams = num_teams
        self.min_crew = None
        self.max_crew = None

        boat_lib = BoatTypeLibrary()
        boat_type_from_lib, opti_crew = boat_lib.get_boat_data(boat_type)

        if boat_type_from_lib and opti_crew is not None:
            self.min_crew, self.max_crew = boat_lib.calc_crew(opti_crew)
        else:
            print(f"Båttyp {boat_type} finns inte i databasen.")
            boat_lib.add_boat_types(boat_type, opti_crew)
            boat_type_from_lib, opti_crew = boat_lib.get_boat_data(boat_type)
            # Hämta data igen efter att båten lagts till
            self.min_crew, self.max_crew = boat_lib.calc_crew(opti_crew)
        if num_teams is not None:
            self.num_sailors = self.num_teams * opti_crew

    def calc_num_team(self):
        upper_bound = self.max_crew
        if self.max_crew is None:
            return 0
        total_on_water = self.num_boats * upper_bound
        remaining_sailors = self.num_sailors - total_on_water

        if remaining_sailors <= 0:
            return self.num_boats

        extra_teams_needed = int(math.ceil(remaining_sailors / float(upper_bound)))
        return self.num_boats + extra_teams_needed

    def calc_team_size(self):
        total_teams = self.calc_num_team()
        lower_bound = self.num_sailors // total_teams
        upper_bound = math.ceil(self.num_sailors / float(total_teams))

        return lower_bound, upper_bound


class SailingSchedule:
    def __init__(self, num_boats, num_teams, event_type):
        self.num_boats = num_boats
        self.num_teams = num_teams
        self.event_type = event_type
        self.schedule = []
        self.team_count = [0] * num_teams

    def calc_max_race(self):
        if self.event_type == "kort":
            max_time = 2.5 * 60
        else:
            max_time = 3.5 * 60
        return max_time // 20  # Med antagandet att varje race tar max 20 minuter

    def divide_into_groups(self):
        # Om antalet lag överskrider 2x antalet båtar, dela upp dem i grupper
        if self.num_teams > 2 * self.num_boats:
            group_size = 2 * self.num_boats
            return [range(i, i + group_size) for i in range(0, self.num_teams, group_size)]
        else:
            return [range(self.num_teams)]

    def sailing_schedule(self):
        max_race = self.calc_max_race()
        race_count = 0
        groups = self.divide_into_groups()

        for group in groups:
            for i in group:
                for j in group:
                    if j > i and race_count < max_race:
                        self.schedule.append((i, j))
                        self.team_count[i] += 1
                        self.team_count[j] += 1
                        race_count += 1
                    if race_count >= max_race:
                        return
        # Här skapas grundomgången.
        for i in range(self.num_teams):
            for j in range(i + 1, self.num_teams):
                if race_count < max_race:
                    self.schedule.append((i, j))
                    race_count += 1
                else:
                    return

    def extra_round(self):
        max_race = self.calc_max_race()
        race_count = len(self.schedule)

        # Här fyller vi upp schemat med ytterligare race.
        for i in range(self.num_teams):
            for j in range(i + 1, self.num_teams):
                if (i, j) not in self.schedule and race_count < max_race:
                    self.schedule.append((i, j))
                    race_count += 1
                if race_count >= max_race:
                    return

    def generate_schedule(self):
        self.sailing_schedule()
        if len(self.schedule) < self.calc_max_race():
            self.extra_round()

    def display_schedule(self):
        print(f"Totalt {len(self.schedule)} race kommer att seglas.")
        for race_num, lagen in enumerate(self.schedule, 1):
            print(f"Race {race_num}:", end=" ")
            for lag in lagen:
                print(f"Lag {lag + 1}", end=" vs ")
            print(f"i Båt {race_num % self.num_boats + 1}")

    def identify_finalists(self, results_object):
        """
        Identifierar vilka lag som går till final baserat på resultat.
        """
        # logik för att identifiera de bästa lagen baserat på deras resultat ska implementeras.
        # Resultatobjektet kan användas för att få information om lagen.
        pass


class Results:
    def __init__(self):
        self.results_data = {}

    def update_results(self, team, points):
        """
        Uppdaterar resultattavlan med ett lags prestation.
        """
        self.results_data[team.name] = points

    def get_results(self, team):
        """
        Returnerar resultatet för ett specifikt lag.
        """
        return self.results_data.get(team.name, None)
