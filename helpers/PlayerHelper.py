from discord.ui import View, Button
import discord
class PlayerHelper:
    def __init__(self, player_id, player_stats):
        self.stats = player_stats
        self.player_id = str(player_id)
        self.name = self.stats["player_name"]


    def adjust_materials(self, adjustment):
        before = self.stats["materials"]
        self.stats["materials"] += adjustment
        return(f"\n> Adjusted materials from {before} to {before+adjustment}")


    def adjust_science(self, adjustment):
        before = self.stats["science"]
        self.stats["science"] += adjustment
        return (f"\n> Adjusted science from {before} to {before + adjustment}")
    def adjust_resource(self, resource, adjustment):
        if(resource == "science"):
            return self.adjust_science(adjustment)
        elif resource == "materials":
            return self.adjust_materials(adjustment)
        elif resource == "money":
            return self.adjust_money(adjustment)

    def adjust_money(self, adjustment):
        before = self.stats["money"]
        self.stats["money"] += adjustment
        return(f"\n> Adjusted money from {before} to {before+adjustment}")

    def adjust_material_cube(self, adjustment):
        before = self.stats["material_pop_cubes"]
        amount = min(self.stats["material_pop_cubes"] + adjustment, 11)
        self.stats["material_pop_cubes"] = amount
        return (f"\n> Adjusted material cubes from {before} to {amount}")

    def adjust_science_cube(self, adjustment):
        before = self.stats["science_pop_cubes"]
        amount = min(self.stats["science_pop_cubes"] + adjustment, 11)
        self.stats["science_pop_cubes"] = amount
        return (f"\n> Adjusted science cubes from {before} to {amount}")

    def adjust_money_cube(self, adjustment):
        before = self.stats["money_pop_cubes"]
        amount = min(self.stats["money_pop_cubes"] + adjustment, 11)
        self.stats["money_pop_cubes"] = amount
        return (f"\n> Adjusted money cubes from {before} to {amount}")
    def adjust_influence(self, adjustment):
        before = self.stats["influence_discs"]
        amount = max(0, self.stats["influence_discs"]+adjustment)
        amount = min(15, amount)
        self.stats["influence_discs"] = amount
        return (f"\n> Adjusted influence discs from {before} to {amount}")
    def spend_influence_on_action(self, action:str):
        self.adjust_influence(-1)
        if action+"_action_counters" not in self.stats:
            self.stats[action+"_action_counters"] = 0
        self.stats[action+"_action_counters"] = self.stats[action+"_action_counters"]+1

    def adjust_influence_on_action(self, action:str, amount:int):
        self.adjust_influence(-amount)
        if action+"_action_counters" not in self.stats:
            self.stats[action+"_action_counters"] = 0
        if self.stats[action+"_action_counters"]+amount > -1:
            self.stats[action+"_action_counters"] = self.stats[action+"_action_counters"]+amount
        else:
            self.stats[action+"_action_counters"] = 0
    
    def acquire_disc_tile_for_points(self):
        if "disc_tiles_for_points" not in self.stats:
            self.stats["disc_tiles_for_points"] = 0
        self.stats["disc_tiles_for_points"] = self.stats["disc_tiles_for_points"]+1
    def setOldShipParts(self, ship):
        if f"old_{ship}_parts" not in self.stats:
            self.stats[f"old_{ship}_parts"] = self.stats[f"{ship}_parts"]
        
    def passTurn(self, passed:bool):
        self.stats["passed"] = passed
    def permanentlyPassTurn(self, passed:bool):
        self.stats["perma_passed"] = passed
    
    def setFirstPlayer(self, firstPlayerBool : bool):
        self.stats["firstPlayer"] = firstPlayerBool

    def adjust_colony_ships(self, adjustement):
        if self.stats["colony_ships"] <= 0:
            return False
        elif (self.stats["colony_ships"] - adjustement) < 0:
            return False
        else:
            self.stats["colony_ships"] = self.stats["colony_ships"] - adjustement
            return(self.stats["colony_ships"])
    
    def materials_income(self):
        track = self.stats["population_track"]
        cubes = self.stats["material_pop_cubes"]
        return(track[cubes-1])

    def science_income(self):
        track = self.stats["population_track"]
        cubes = self.stats["science_pop_cubes"]
        return(track[cubes-1])

    def money_income(self):
        track = self.stats["population_track"]
        cubes = self.stats["money_pop_cubes"]
        return(track[cubes-1])

    def upkeep(self):
        track = self.stats["influence_track"]
        discs = self.stats["influence_discs"]
        if discs >= 13:
            return(0)
        else:
            return(track[discs])
    
    def cleanUp(self):
        self.adjust_money(self.money_income()-self.upkeep())
        self.adjust_materials(self.materials_income())
        self.adjust_science(self.science_income())
        self.stats["colony_ships"] = self.stats["base_colony_ships"]
        self.stats["passed"] = False
        self.stats["perma_passed"] = False
        actions = ["influence","build","move","upgrade","explore","research"]
        for action in actions:
            if action+"_action_counters" not in self.stats:
                self.stats[action+"_action_counters"] = 0
            else:
                count = self.stats[action+"_action_counters"]
                self.stats[action+"_action_counters"] = 0
                self.adjust_influence(count)