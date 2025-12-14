import mesa
import random
import matplotlib.pyplot as plt
import pandas as pd

# --- 1. Agenten ---

class PassengerAgent(mesa.Agent):
    def __init__(self, unique_id, model, transport_type_preference):
        super().__init__(model)
        self.unique_id = unique_id
        self.transport_type = transport_type_preference 
        self.waiting_time = 0
        self.satisfaction = 100
        self.arrived = False
        self.has_switched = False # Neu: Merker, ob gewechselt wurde

    def step(self):
        if not self.arrived:
            self.waiting_time += 1
            
            # Zufriedenheit sinkt
            decay = 0.5 if self.transport_type == "Tram" else 0.8
            self.satisfaction -= decay
            if self.satisfaction < 0: self.satisfaction = 0

            # --- HIER IST DIE SWITCHING LOGIC (R1 Loop) ---
            # Wenn Agent auf Bus wartet UND länger als 30 Ticks wartet:
            if self.transport_type == "Bus" and self.waiting_time > 30:
                self.switch_to_tram()

    def switch_to_tram(self):
        """Der Passagier gibt auf und wechselt zum Tram."""
        self.transport_type = "Tram"
        self.has_switched = True
        self.satisfaction -= 10 # Wechseln ist stressig (Zufriedenheit sinkt einmalig)
        
        # WICHTIG: Agent muss physisch auf die Tram-Spur (y=1) umziehen
        x, y = self.pos
        if y == 0: # Wenn er noch auf der Busspur ist
            self.model.grid.move_agent(self, (x, 1))

class VehicleAgent(mesa.Agent):
    def __init__(self, unique_id, model, v_type):
        super().__init__(model)
        self.unique_id = unique_id
        self.v_type = v_type 
        self.speed = 1

    def step(self):
        x, y = self.pos
        
        # Baustelle bremst nur Busse
        if self.v_type == "Bus" and self.model.construction_active:
            if 10 <= x <= 20:
                if random.random() < 0.7: return # Stau

        # Bewegung
        new_x = (x + 1) % self.model.grid.width 
        self.model.grid.move_agent(self, (new_x, y))
        
        # Passagiere einsammeln
        cell_mates = self.model.grid.get_cell_list_contents([(new_x, y)])
        for mate in cell_mates:
            if isinstance(mate, PassengerAgent) and not mate.arrived:
                # Jetzt nimmt das Tram auch die "Wechsler" mit, 
                # da diese ihren transport_type auf "Tram" geändert haben.
                if mate.transport_type == self.v_type:
                    mate.arrived = True 

# --- 2. Modell ---

class CityTransportModel(mesa.Model):
    def __init__(self, num_passengers, construction_active=True):
        super().__init__()
        self.construction_active = construction_active
        self.grid = mesa.space.MultiGrid(50, 2, torus=True)
        
        # Datensammler erweitert um "Total_Switchers"
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Avg_Satisfaction": compute_avg_satisfaction,
                "Bus_Wait": lambda m: count_waiting(m, "Bus"),
                "Tram_Wait": lambda m: count_waiting(m, "Tram"),
                "Total_Switchers": count_switchers # Neue Metrik
            }
        )

        # Fahrzeuge
        bus = VehicleAgent(0, self, "Bus")
        self.grid.place_agent(bus, (0, 0))
        tram = VehicleAgent(1, self, "Tram")
        self.grid.place_agent(tram, (0, 1))

        # Passagiere
        for i in range(num_passengers):
            # Starten wir mit mehr Busfahrern, um den Effekt zu sehen
            p_type = "Bus" if random.random() < 0.8 else "Tram"
            a = PassengerAgent(i + 100, self, p_type)
            x = random.randrange(self.grid.width)
            y = 0 if p_type == "Bus" else 1
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")

# --- Hilfsfunktionen ---

def compute_avg_satisfaction(model):
    passengers = [a for a in model.agents if isinstance(a, PassengerAgent)]
    if not passengers: return 0
    return sum([a.satisfaction for a in passengers]) / len(passengers)

def count_waiting(model, v_type):
    return sum([1 for a in model.agents 
                if isinstance(a, PassengerAgent) 
                and a.transport_type == v_type 
                and not a.arrived])

def count_switchers(model):
    """Zählt, wie viele Leute bisher umgestiegen sind."""
    return sum([1 for a in model.agents 
                if isinstance(a, PassengerAgent) and a.has_switched])

# --- 3. Ausführung ---

if __name__ == "__main__":
    model = CityTransportModel(num_passengers=150, construction_active=True)

    for i in range(150): 
        model.step()

    results = model.datacollector.get_model_vars_dataframe()

    # Plotten mit Subplots für bessere Übersicht
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

    # Plot 1: Zufriedenheit & Wechsler
    ax1.plot(results["Avg_Satisfaction"], label="Zufriedenheit", color="green")
    ax1.set_ylabel("Zufriedenheit (0-100)")
    ax1.legend(loc="upper left")
    
    # Zweite Y-Achse für die Anzahl der Wechsler
    ax1b = ax1.twinx()
    ax1b.plot(results["Total_Switchers"], label="Anzahl Umsteiger (Switchers)", color="red", linestyle="--")
    ax1b.set_ylabel("Anzahl Personen")
    ax1b.legend(loc="upper right")
    ax1.set_title("Effekt der Baustelle: Passagiere wechseln zur Tram")

    # Plot 2: Warteschlangen
    ax2.plot(results["Bus_Wait"], label="Wartende Bus", color="blue")
    ax2.plot(results["Tram_Wait"], label="Wartende Tram", color="orange")
    ax2.set_ylabel("Anzahl Wartende")
    ax2.set_xlabel("Zeit (Ticks)")
    ax2.legend()
    ax2.set_title("Verlagerung der Warteschlangen")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()