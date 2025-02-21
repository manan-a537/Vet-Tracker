import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import webbrowser

class PaymentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Payment Gateway")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        # Configure style
        self.style = ttk.Style(self.root)
        self.style.theme_use("arc")
        self.style.configure("Accent.TButton", 
                           font=("Helvetica", 12, "bold"), 
                           background="#4CAF50", 
                           foreground="white")
        self.style.map("Accent.TButton", 
                      background=[("active", "#45a049")])
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.create_header()
        self.create_payment_details()
        self.create_payment_methods()
        
    def create_header(self):
        # Header Frame
        header_frame = ttk.Frame(self.main_frame, padding="10")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Title
        ttk.Label(
            header_frame, 
            text="Payment Gateway", 
            font=("Helvetica", 24, "bold"), 
            foreground="#4CAF50"
        ).grid(row=0, column=0, sticky=tk.W)
        
    def create_payment_details(self):
        # Payment Details Frame
        details_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Payment Details", 
            padding="15"
        )
        details_frame.grid(
            row=1, 
            column=0, 
            columnspan=2, 
            sticky=(tk.W, tk.E), 
            padx=10, 
            pady=10
        )
        
        # Amount
        ttk.Label(
            details_frame, 
            text="Booking Amount:", 
            font=("Helvetica", 14)
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(
            details_frame, 
            text="₹ 399/-", 
            font=("Helvetica", 14, "bold"), 
            foreground="#4CAF50"
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Service details
        ttk.Label(
            details_frame, 
            text="Service:", 
            font=("Helvetica", 14)
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(
            details_frame, 
            text="Veterinary Appointment Booking", 
            font=("Helvetica", 14)
        ).grid(row=1, column=1, sticky=tk.W, pady=5)
        
    def create_payment_methods(self):
        # Payment Methods Frame
        methods_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Select Payment Method", 
            padding="15"
        )
        methods_frame.grid(
            row=2, 
            column=0, 
            columnspan=2, 
            sticky=(tk.W, tk.E), 
            padx=10, 
            pady=10
        )
        
        # UPI Payment
        upi_frame = ttk.Frame(methods_frame, padding="10")
        upi_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(
            upi_frame, 
            text="UPI Payment", 
            font=("Helvetica", 12, "bold")
        ).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(
            upi_frame, 
            text="Pay with UPI", 
            style="Accent.TButton",
            command=self.pay_with_upi
        ).grid(row=1, column=0, pady=10)
        
        # Card Payment
        card_frame = ttk.Frame(methods_frame, padding="10")
        card_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(
            card_frame, 
            text="Card Payment", 
            font=("Helvetica", 12, "bold")
        ).grid(row=0, column=0, sticky=tk.W)
        
        # Card Number
        ttk.Label(
            card_frame, 
            text="Card Number:"
        ).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.card_number = ttk.Entry(card_frame, width=30)
        self.card_number.grid(row=1, column=1, padx=5)
        
        # Expiry
        ttk.Label(
            card_frame, 
            text="Expiry (MM/YY):"
        ).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.expiry = ttk.Entry(card_frame, width=10)
        self.expiry.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # CVV
        ttk.Label(
            card_frame, 
            text="CVV:"
        ).grid(row=3, column=0, sticky=tk.W, pady=2)
        self.cvv = ttk.Entry(card_frame, width=5, show="*")
        self.cvv.grid(row=3, column=1, sticky=tk.W, padx=5)
        
        ttk.Button(
            card_frame, 
            text="Pay with Card", 
            style="Accent.TButton",
            command=self.pay_with_card
        ).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Net Banking
        net_banking_frame = ttk.Frame(methods_frame, padding="10")
        net_banking_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(
            net_banking_frame, 
            text="Net Banking", 
            font=("Helvetica", 12, "bold")
        ).grid(row=0, column=0, sticky=tk.W)
        
        banks = ["Select Bank", "SBI", "HDFC", "ICICI", "Axis", "Other"]
        self.selected_bank = tk.StringVar()
        bank_dropdown = ttk.Combobox(
            net_banking_frame, 
            textvariable=self.selected_bank, 
            values=banks, 
            state="readonly",
            width=30
        )
        bank_dropdown.current(0)
        bank_dropdown.grid(row=1, column=0, pady=5)
        
        ttk.Button(
            net_banking_frame, 
            text="Pay with Net Banking", 
            style="Accent.TButton",
            command=self.pay_with_netbanking
        ).grid(row=2, column=0, pady=10)

    def pay_with_upi(self):
        messagebox.showinfo(
            "UPI Payment", 
            "Redirecting to UPI payment gateway...\nAmount: ₹399/-"
        )
        # Here you would integrate with actual UPI payment gateway

    def pay_with_card(self):
        if not self.card_number.get() or not self.expiry.get() or not self.cvv.get():
            messagebox.showerror("Error", "Please fill all card details")
            return
        
        messagebox.showinfo(
            "Card Payment", 
            "Processing card payment...\nAmount: ₹399/-"
        )
        # Here you would integrate with actual card payment gateway

    def pay_with_netbanking(self):
        if self.selected_bank.get() == "Select Bank":
            messagebox.showerror("Error", "Please select a bank")
            return
        
        messagebox.showinfo(
            "Net Banking", 
            f"Redirecting to {self.selected_bank.get()} payment gateway...\nAmount: ₹399/-"
        )
        # Here you would integrate with actual net banking gateway

def main():
    root = ThemedTk(theme="arc")
    app = PaymentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
