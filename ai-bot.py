import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, \
GATEWAY, STALKER, CYBERNETICSCORE, \
STARGATE, VOIDRAY   
'''
NEXUS is required to build PROBES (ie WORKERS, collects the minerals).

PYLON is required to increase supplies and gives an area (PSIONIC MATRIX) to make offensive buildings such as GATEWAYS, 
CYBERNETICS CORE, STARGATE etc.

ASSIMILATOR is built on VASPENE GEYSERS to collect VASPENE GAS.

The GATEWAY is a unit production structure for the PROTOSS, responsible for warping in ground units. 

The CYBERNETICS CORE unlocks new units and the Shield Battery building, and enables research of several upgrades.
Possessing a CYBERNECTICS CORE unlocks the construction of Sentries, STALKER and Adepts at the GATEWAY. Requires 
a Gateway before it can be warped in. 

STALKER are ground unit force.

The STARGATE is a unit producing structure for the PROTOSS, responsible for producing most of the PROTOSS air units.
It requires a CYBERNETICS CORE before it can be warped in. The STARGATE produces the Phoenix, Oracle and the VOIDRAY.

VOIDRAY are air unit force.


'''

import random

class OurCustomBot(sc2.BotAI):

    def __init__(self):
        self.ITERATIONS_PER_MINUTE = 165
        self.MAX_WORKERS = 60

    async def on_step(self, iteration):
        #do whatever we want
        self.iteration = iteration
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.expand()
        await self.build_assimilator()
        await self.build_offensive_force_buildings()
        await self.build_offensive_force()
        await self.attack()
        

    async def build_workers(self):
        if (len(self.units(NEXUS)) * 16) > len(self.units(PROBE)):
            if len(self.units(PROBE)) < self.MAX_WORKERS:
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
        #print(self.iteration / self.ITERATIONS_PER_MINUTE)
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random

            if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon)

            elif len(self.units(GATEWAY)) < ((self.iteration / self.ITERATIONS_PER_MINUTE)/2):
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)

            if self.units(CYBERNETICSCORE).ready.exists:
                if len(self.units(STARGATE)) < ((self.iteration / self.ITERATIONS_PER_MINUTE)/2):
                    if self.can_afford(STARGATE) and not self.already_pending(STARGATE):
                        await self.build(STARGATE, near=pylon)


    async def build_offensive_force(self):
        for gw in self.units(GATEWAY).ready.noqueue:
            if not self.units(STALKER).amount > self.units(VOIDRAY).amount:

                if self.can_afford(STALKER) and self.supply_left > 0:
                    await self.do(gw.train(STALKER))

        for sg in self.units(STARGATE).ready.noqueue:
            if self.can_afford(VOIDRAY) and self.supply_left > 0:
                await self.do(sg.train(VOIDRAY))

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units) # choose random enemy-units once we reach the enemy_start_location 
        elif len(self.known_enemy_structures) > 0:       #choose random enemy-structures once we reach the enemy_start_location
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]  #if no activity is currently performed then go to enemy_start_location
    ''' 
        To attack an enemy, there are 2 ways:
        1) We build our army and find the enemy start(base) location using find_traget() and attack.
        2) If enemy attacks us, then we have to attack that enemy
    '''
    async def attack(self):
        # {UNIT: [n to fight, n to defend]}
        aggressive_units = {STALKER: [15, 5],
                            VOIDRAY: [8, 3]}

        for UNIT in aggressive_units:
            if self.units(UNIT).amount > aggressive_units[UNIT][0] and self.units(UNIT).amount > aggressive_units[UNIT][1]:
                for s in self.units(UNIT).idle:
                    await self.do(s.attack(self.find_target(self.state)))

            elif self.units(UNIT).amount > aggressive_units[UNIT][1]:
                if len(self.known_enemy_units) > 0:
                    for s in self.units(UNIT).idle:
                        await self.do(s.attack(random.choice(self.known_enemy_units)))

run_game(maps.get("AbyssalReefLE"),[
    Bot( Race.Protoss, OurCustomBot()),
    Computer( Race.Terran, Difficulty.Hard)
], realtime=False)
