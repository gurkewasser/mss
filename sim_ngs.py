import mesa
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- 1. Agenten ---

class PassengerAgent(mesa.Agent):
    def __init__(self, unique_id, model, transport_type_preference):
        super().__init__(model)
        self.unique_id = unique_id
        self.transport_type = transport_type_preference 
        self.waiting_time = 0
        self.satisfaction = 100
        self.arrived = False
        self.has_switched = False 

    def step(self):
        if not self.arrived:
            self.waiting_time += 1
            
            # Dimension: SOZIAL (Zufriedenheit sinkt)
            decay = 0.5 if self.transport_type == "Tram" else 0.8
            self.satisfaction -= decay
            if self.satisfaction < 0: self.satisfaction = 0

            # --- Verhalten 2. Ordnung: Mode-Switching ---
            # Wenn Agent auf Bus wartet UND länger als 30 Ticks wartet:
            if self.transport_type == "Bus" and self.waiting_time > 30:
                self.switch_to_tram()

    def switch_to_tram(self):
        """Der Passagier gibt auf und wechselt zum Tram."""
        self.transport_type = "Tram"
        self.has_switched = True
        self.satisfaction -= 10 # Wechselstress
        
        # Agent muss physisch auf die Tram-Spur (y=1) umziehen
        x, y = self.pos
        if y == 0: 
            self.model.grid.move_agent(self, (x, 1))

class VehicleAgent(mesa.Agent):
    def __init__(self, unique_id, model, v_type):
        super().__init__(model)
        self.unique_id = unique_id
        self.v_type = v_type 
        self.emissions = 0 # Dimension: ÖKOLOGISCH

    def step(self):
        x, y = self.pos
        moved = True
        
        # Baustelle bremst nur Busse
        if self.v_type == "Bus" and self.model.construction_active:
            if 10 <= x <= 20:
                if random.random() < 0.7: 
                    moved = False # Bus steht im Stau
                    # CO2: Stop & Go ist sehr ineffizient
                    self.emissions += 8
        
        # Bewegung
        if moved:
            new_x = (x + 1) % self.model.grid.width 
            self.model.grid.move_agent(self, (new_x, y))
            
            # CO2 Berechnung für Fahren
            if self.v_type == "Bus":
                self.emissions += 5  # Dieselbus Normalfahrt
            elif self.v_type == "Tram":
                self.emissions += 2  # Tram (Strom) - weniger als Bus, aber vorhanden

        # Passagiere einsammeln
        if moved:
            cell_mates = self.model.grid.get_cell_list_contents([(new_x, y)])
            for mate in cell_mates:
                if isinstance(mate, PassengerAgent) and not mate.arrived:
                    if mate.transport_type == self.v_type:
                        mate.arrived = True 

# --- 2. Modell mit IMBMS Logik ---

class CityTransportModel(mesa.Model):
    def __init__(self, num_passengers, scenario="baseline"):
        super().__init__()
        self.scenario = scenario # "baseline" oder "imbms"
        self.construction_active = True
        self.grid = mesa.space.MultiGrid(50, 2, torus=True)
        self.tram_deployed = False # Merker, ob System schon eingegriffen hat
        
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Avg_Satisfaction": compute_avg_satisfaction,
                "Total_Switchers": count_switchers,
                # Summe aller Emissionen aller Fahrzeuge
                "Total_CO2": lambda m: sum([a.emissions for a in m.agents if isinstance(a, VehicleAgent)])
            }
        )

        # Agenten ID Counter
        self.current_id = 0

        # 1. Fahrzeuge erstellen
        bus = VehicleAgent(self.next_id(), self, "Bus")
        self.grid.place_agent(bus, (0, 0))

        tram = VehicleAgent(self.next_id(), self, "Tram")
        self.grid.place_agent(tram, (0, 1))

        # 2. Passagiere erstellen
        for i in range(num_passengers):
            p_type = "Bus" if random.random() < 0.7 else "Tram"
            a = PassengerAgent(self.next_id(), self, p_type)
            x = random.randrange(self.grid.width)
            y = 0 if p_type == "Bus" else 1
            self.grid.place_agent(a, (x, y))

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")
        
        # --- DAS INTELLIGENTE SYSTEM (IMBMS) ---
        if self.scenario == "imbms" and not self.tram_deployed:
            # Datenerfassung (Digital Twin)
            current_sat = compute_avg_satisfaction(self)
            
            # Entscheidungsschwelle: Wenn Zufriedenheit unter 80 fällt
            if current_sat < 80:
                self.deploy_extra_tram()

    def deploy_extra_tram(self):
        """Das System reagiert auf die Störung mit Taktverdichtung."""
        print(f"ALARM [Zeit {self.steps}]: Zufriedenheit kritisch! IMBMS sendet Verstärker-Tram.")
        # Neues Tram an den Start setzen
        new_tram = VehicleAgent(self.next_id(), self, "Tram")
        self.grid.place_agent(new_tram, (0, 1)) # Startet bei x=0 auf Tramspur
        self.tram_deployed = True

# --- Hilfsfunktionen ---

def compute_avg_satisfaction(model):
    passengers = [a for a in model.agents if isinstance(a, PassengerAgent)]
    if not passengers: return 0
    return sum([a.satisfaction for a in passengers]) / len(passengers)

def count_switchers(model):
    return sum([1 for a in model.agents if isinstance(a, PassengerAgent) and a.has_switched])

# --- 3. Ausführung & Vergleich ---

if __name__ == "__main__":
    steps = 150
    n_passengers = 200
    
    print("--- Simulation 1: Status Quo (Kein System) ---")
    model_base = CityTransportModel(n_passengers, scenario="baseline")
    for i in range(steps): model_base.step()
    res_base = model_base.datacollector.get_model_vars_dataframe()

    print("\n--- Simulation 2: IMBMS (Datengetriebene Lösung) ---")
    model_imbms = CityTransportModel(n_passengers, scenario="imbms")
    for i in range(steps): model_imbms.step()
    res_imbms = model_imbms.datacollector.get_model_vars_dataframe()

    # --- PLOTTING FÜR DEN LEISTUNGSNACHWEIS (NGS) ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # 1. Soziale Dimension: Zufriedenheit
    ax1.plot(res_base["Avg_Satisfaction"], label="Status Quo (Passiv)", color="red", linestyle="--")
    ax1.plot(res_imbms["Avg_Satisfaction"], label="IMBMS (Aktiv)", color="green", linewidth=2)
    ax1.axhline(y=80, color='gray', linestyle=':', label="Interventions-Schwelle")
    ax1.set_title("Soziale Dimension: Stabilisierung der Zufriedenheit")
    ax1.set_ylabel("Score (0-100)")
    ax1.legend()
    ax1.grid(True)

    # 2. Ökologische Dimension: CO2
    ax2.plot(res_base["Total_CO2"], label="Status Quo CO2", color="grey", linestyle="--")
    ax2.plot(res_imbms["Total_CO2"], label="IMBMS CO2 (Investition)", color="green")
    ax2.set_title("Ökologische Dimension: CO2-Trade-off (Energieeinsatz für Resilienz)")
    ax2.set_ylabel("Emissionseinheiten")
    ax2.legend()
    ax2.grid(True)

    # 3. Verhalten: Umsteiger
    ax3.plot(res_base["Total_Switchers"], label="Umsteiger (Status Quo)", color="red", linestyle="--")
    ax3.plot(res_imbms["Total_Switchers"], label="Umsteiger (IMBMS)", color="green")
    ax3.set_title("2. Ordnung Effekt: Systemlast durch Umsteiger")
    ax3.set_xlabel("Zeit (Ticks)")
    ax3.set_ylabel("Anzahl Personen")
    ax3.legend()
    ax3.grid(True)

    plt.tight_layout()
    plt.show()