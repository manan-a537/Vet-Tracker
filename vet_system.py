from dataclasses import dataclass
from typing import List
import math
import pandas as pd
import geocoder
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ttkthemes import ThemedTk
from PIL import Image, ImageTk 

@dataclass
class Location:
    latitude: float
    longitude: float

    def distance_to(self, other: 'Location') -> float:
        R = 6371
        lat1, lon1 = math.radians(float(self.latitude)), math.radians(float(self.longitude))
        lat2, lon2 = math.radians(float(other.latitude)), math.radians(float(other.longitude))
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

@dataclass
class Pet:
    name: str
    species: str
    age: float
    weight: float
    symptoms: List[str]
    medical_history: List[str]
    location: Location

@dataclass
class VetDoctor:
    name: str
    specializations: List[str]
    experience_years: int
    rating: float
    location: Location
    contact: str

class VetMatchingSystem:
    def __init__(self):
        self.doctors = [] 
        self.load_doctors_from_excel()
        
    def load_doctors_from_excel(self):
        try:
            df = pd.read_excel('vets_database.xlsx')
            print(f"Found {len(df)} doctors in database")
            for _, row in df.iterrows():
                try:
                    specializations = [s.strip() for s in row['Specializations'].split(',')]
                    doctor = VetDoctor(
                        name=row['Name'],
                        specializations=specializations,
                        experience_years=int(row['Experience_Years']),
                        rating=float(row['Rating']),
                        location=Location(float(row['Latitude']), float(row['Longitude'])),
                        contact=str(row['Contact'])
                    )
                    self.add_doctor(doctor)
                    print(f"Loaded doctor: {doctor.name}, Specializations: {doctor.specializations}")
                except Exception as e:
                    print(f"Error loading doctor from row {row}: {e}")
        except Exception as e:
            print(f"Error loading doctors: {e}")
            messagebox.showerror("Database Error", f"Could not load doctors database: {e}")
            
    def add_doctor(self, doctor: VetDoctor):
        self.doctors.append(doctor)
        
    def find_best_doctor(self, pet: Pet, max_distance: float) -> List[VetDoctor]:
        specialists = []
        non_specialists = []
        print(f"\nSearching for doctors for {pet.species}")
        print(f"Total doctors in system: {len(self.doctors)}")
        
        for doctor in self.doctors:
            distance = pet.location.distance_to(doctor.location)
            print(f"Checking {doctor.name} - Distance: {distance}km, Specializations: {doctor.specializations}")
            if distance <= max_distance:
               
                rating_score = doctor.rating
                experience_score = min(5, doctor.experience_years * 0.2)
                distance_penalty = -0.1 * distance
                score = rating_score + experience_score + distance_penalty
                
               
                if pet.species.lower().strip() in [s.lower().strip() for s in doctor.specializations]:
                    specialists.append((doctor, score))
                    print(f"Specialist found: {doctor.name} with score {score}")
                else:
                    non_specialists.append((doctor, score))
                    print(f"Non-specialist found: {doctor.name} with score {score}")
        
     
        sorted_specialists = sorted(specialists, key=lambda x: x[1], reverse=True)
        sorted_non_specialists = sorted(non_specialists, key=lambda x: x[1], reverse=True)
        
      
        return [doctor for doctor, _ in sorted_specialists + sorted_non_specialists]

class VetSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Veterinary Doctor Matching System")
        self.root.geometry("1000x800")
        
        # Create main scrollable canvas
        self.main_canvas = tk.Canvas(self.root, bg="#E3F2FD", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=980)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure mouse wheel scrolling
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Rest of your initialization code, but use scrollable_frame instead of root
        self.main_frame = ttk.Frame(self.scrollable_frame, padding="20")
        self.main_frame.pack(fill="both", expand=True)
        
        # Rest of the initialization
        self.system = VetMatchingSystem()
        self.create_header()
        self.create_pet_info_section()
        self.create_medical_section()
        self.create_search_section()
        self.create_results_section()

    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, padding="10")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        try:
            image = Image.open("pet_icon.png") 
            image = image.resize((50, 50), Image.ANTIALIAS)
            self.pet_icon = ImageTk.PhotoImage(image)
            ttk.Label(header_frame, image=self.pet_icon).grid(row=0, column=0, padx=10)
        except Exception as e:
            print(f"Error loading image: {e}")
        
        
        ttk.Label(header_frame, text="Veterinary Doctor Matching System", font=("Helvetica", 20, "bold"), foreground="#4CAF50").grid(row=0, column=1, sticky=tk.W)

    def create_pet_info_section(self):
        pet_frame = ttk.LabelFrame(self.main_frame, text="Pet Information", padding="15")
        pet_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        ttk.Label(pet_frame, text="Pet Name:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pet_name = ttk.Entry(pet_frame, width=30, font=("Helvetica", 12))
        self.pet_name.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(pet_frame, text="Species:", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.species = ttk.Entry(pet_frame, width=30, font=("Helvetica", 12))
        self.species.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(pet_frame, text="Age (years):", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.age = ttk.Entry(pet_frame, width=30, font=("Helvetica", 12))
        self.age.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(pet_frame, text="Weight (kg):", font=("Helvetica", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.weight = ttk.Entry(pet_frame, width=30, font=("Helvetica", 12))
        self.weight.grid(row=3, column=1, padx=10, pady=5)

    def create_medical_section(self):
        medical_frame = ttk.LabelFrame(self.main_frame, text="Medical Information", padding="15")
        medical_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        # Symptoms Label
        ttk.Label(medical_frame, text="Symptoms:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Symptoms Frame
        symptoms_frame = ttk.Frame(medical_frame)
        symptoms_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Available symptoms
        self.symptoms_vars = {}
        symptoms_list = [
            "Bloody Vomit",
            "Excessive Hairloss",
            "Extreme Smell",
            "Not Eating Food",
            "Fever"
        ]
        
        # Create checkboxes for symptoms
        for i, symptom in enumerate(symptoms_list):
            var = tk.BooleanVar()
            self.symptoms_vars[symptom] = var
            ttk.Checkbutton(
                symptoms_frame,
                text=symptom,
                variable=var,
                style="Symptom.TCheckbutton"
            ).grid(row=i//2, column=i%2, sticky=tk.W, padx=5, pady=2)
        
        # Other symptoms
        ttk.Label(
            symptoms_frame,
            text="Other Symptoms:",
            font=("Helvetica", 11)
        ).grid(row=3, column=0, sticky=tk.W, pady=(10,2))
        
        self.other_symptoms = scrolledtext.ScrolledText(
            symptoms_frame,
            height=2,
            width=40,
            font=("Helvetica", 11)
        )
        self.other_symptoms.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Medical History
        ttk.Label(
            medical_frame,
            text="Medical History:",
            font=("Helvetica", 12)
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.medical_history = scrolledtext.ScrolledText(
            medical_frame,
            height=4,
            width=50,
            font=("Helvetica", 12)
        )
        self.medical_history.grid(row=1, column=1, padx=10, pady=5)

    def create_search_section(self):
        search_frame = ttk.LabelFrame(
            self.main_frame,
            text="Search Settings",
            padding="15",
            style="Card.TLabelframe"
        )
        search_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
            padx=10,
            pady=10
        )
        
        # Distance input with better styling
        ttk.Label(
            search_frame,
            text="Max Distance (km):",
            font=("Helvetica", 12)
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.max_distance = ttk.Entry(
            search_frame,
            width=30,
            font=("Helvetica", 12)
        )
        self.max_distance.grid(row=0, column=1, padx=10, pady=5)
        self.max_distance.insert(0, "10")
        
        # Enhanced Find Doctors button with shadow effect
        button_frame = ttk.Frame(search_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=15)
        
        self.search_button = tk.Button(
            button_frame,
            text="🔍 Find Doctors",
            command=self.find_doctors,
            font=("Helvetica", 14, "bold"),
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            cursor="hand2",
            relief="raised",
            padx=30,
            pady=10,
            bd=0
        )
        self.search_button.pack(pady=5)

    def create_results_section(self):
        results_frame = ttk.LabelFrame(
            self.main_frame,
            text="Results",
            padding="15",
            style="Card.TLabelframe"
        )
        results_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            padx=10,
            pady=10
        )
        
        # Results area with better styling
        self.results_area = tk.Text(
            results_frame,
            height=15,
            width=80,
            font=("Helvetica", 12),
            bg="#FFFFFF",
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=10
        )
        self.results_area.grid(row=0, column=0, padx=10, pady=10)
        
        # Styled scrollbar
        scrollbar = ttk.Scrollbar(
            results_frame,
            orient="vertical",
            command=self.results_area.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.results_area.configure(yscrollcommand=scrollbar.set)
        
        # Configure clickable text styling
        self.results_area.tag_configure(
            "clickable",
            foreground="#2196F3",
            underline=1,
            font=("Helvetica", 12, "bold")
        )
        self.results_area.tag_bind("clickable", "<Button-1>", self.open_payment_page)
        self.results_area.tag_bind("clickable", "<Enter>", lambda e: self.results_area.configure(cursor="hand2"))
        self.results_area.tag_bind("clickable", "<Leave>", lambda e: self.results_area.configure(cursor=""))

    def open_payment_page(self, event=None):
        payment_window = tk.Toplevel(self.root)
        from payment import PaymentGUI
        PaymentGUI(payment_window)

    def get_current_location(self):
        try:
            g = geocoder.ip('me')
            if g.ok:
                return Location(g.lat, g.lng)
            else:
                raise Exception("Could not detect location")
        except Exception as e:
            messagebox.showerror("Location Error", 
                               "Could not detect location automatically. Using default location.")
            return Location(28.2487, -77.0635)  

    def find_doctors(self):
        try:
            # Get selected symptoms
            selected_symptoms = [
                symptom for symptom, var in self.symptoms_vars.items()
                if var.get()
            ]
            
            # Add other symptoms if any
            other = self.other_symptoms.get("1.0", tk.END).strip()
            if other:
                selected_symptoms.extend(other.split('\n'))
            
            pet = Pet(
                name=self.pet_name.get(),
                species=self.species.get(),
                age=float(self.age.get()),
                weight=float(self.weight.get()),
                symptoms=selected_symptoms,
                medical_history=self.medical_history.get("1.0", tk.END).strip().split('\n'),
                location=self.get_current_location()
            )
            
            max_distance = float(self.max_distance.get())
            
            best_doctors = self.system.find_best_doctor(pet, max_distance)
            
            self.results_area.delete("1.0", tk.END)
            if not best_doctors:
                self.results_area.insert(tk.END, f"No doctors found within {max_distance} km matching your criteria.")
            else:
                for doctor in best_doctors:
                    distance = pet.location.distance_to(doctor.location)
                    
                    self.results_area.insert(tk.END, "\nDoctor: ")
                    self.results_area.insert(tk.END, doctor.name, "clickable")
                    
                    result_text = (
                        f"\nSpecializations: {', '.join(doctor.specializations)}\n"
                        f"Experience: {doctor.experience_years} years\n"
                        f"Rating: {doctor.rating}\n"
                        f"Distance: {distance:.2f} km\n"
                        f"Contact: {doctor.contact}\n"
                        f"{'='*40}\n"
                    )
                    self.results_area.insert(tk.END, result_text)
                    
        except ValueError as e:
            messagebox.showerror("Input Error", "Please check your input values. Age and weight must be numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = ThemedTk(theme="arc") 
    app = VetSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()