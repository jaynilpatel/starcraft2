import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, \
GATEWAY, STALKER, CYBERNETICSCORE
import random

class OurCustomBot(sc2.BotAI):
    async def on_step(self, iteration):
        #do whatever we want
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.expand()
        await self.build_assimilator()
        await self.build_offensive_force_buildings()
        await self.build_offensive_force()
        await self.attack()
        

    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near= nexuses.first)

    async def expand(self):
        if self.units(NEXUS).amount < 2 and self.can_afford(NEXUS):
            await self.expand_now()

    async def build_assimilator(self):
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(15, nexus)
            for vaspene in vaspenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(ASSIMILATOR, vaspene))

    async def build_offensive_force_buildings(self):
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random
            if self.units(GATEWAY).ready.exists:
                if not self.units(CYBERNETICSCORE):
                    if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                        await self.build( CYBERNETICSCORE, near=pylon)
            else:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)

    async def build_offensive_force(self):
        for gw in self.units(GATEWAY).ready.noqueue:
            if self.can_afford(STALKER) and self.supply_left > 0:
                await self.do(gw.train(STALKER))

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units) # choose random enemy-units once we reach the enemy_start_location 
        elif len(self.known_enemy_structures) > 0:       #choose random enemy-structures once we reach the enemy_start_location
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]  #if no activity is currently performed then go to enemy_start_location
    ''' 
        To attack an enemy, there are 2 ways:
        1) We build our army (>15 units) and find the enemy start(base) location using find_traget() and attack.
        2) If enemy attacks us, and if we have >3 STALKERS, then attack that enemy
    '''
    async def attack(self):
        if self.units(STALKER).amount > 15:
            for s in self.units(STALKER).idle: # for all the idle stalker
                await self.do(s.attack(self.find_target(self.state))) #attack the based on the return value of find_target. ie enemy-location, enemy-structures, enemy-units
               
        elif self.units(STALKER).amount > 3:
            if len(self.known_enemy_units) > 0:
                for s in self.units(STALKER).idle:
                    await self.do(s.attack(random.choice(self.known_enemy_units))) # randomly choose the enemy-unit and then attack


run_game(maps.get("AbyssalReefLE"),[
    Bot( Race.Protoss, OurCustomBot()),
    Computer( Race.Terran, Difficulty.Easy)
], realtime=False)
