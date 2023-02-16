# This program is a shoe inventory management system that allows the user to view, add, and modify the inventory of a shoe store. 
# The program uses the tabulate library to display the inventory data in a tabular format, and stores the inventory data in 
# a text file for persistence. The user can view all the shoes in the inventory, add new shoes, re-stock existing shoes, 
# search for a shoe, calculate the value of each item, and see which product has the highest quantity available. 
# The program utilizes object-oriented programming principles to represent each shoe as a Shoe object.

from tabulate import tabulate

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
       
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity
      
    def __str__(self):
        # Returns a string representation of the Shoe class
        return f"{self.product} ({self.code}): {self.quantity} units available at ${self.cost} each from {self.country}."
        
#=============Shoe list===========
shoes = []

#==========Functions outside the class==============
def read_shoes_data():
    # This function opens the file inventory.txt and reads the data from this file, then creates a shoes object with this data
    # and appends this object into the shoes list. 
    try:
        with open("inventory.txt", "r") as f:
            next(f)  # Skip the first line
            for line in f:
                data = line.strip().split(",")
                country = data[0].strip()
                code = data[1].strip()
                product = data[2].strip()
                cost = float(data[3].strip())
                quantity = int(data[4].strip())
                shoe = Shoe(country, code, product, cost, quantity)
                shoes.append(shoe)
    except FileNotFoundError:
        print("The inventory file was not found.")
    except:
        print("An error occurred while reading the inventory file.")

def capture_shoes():
    # This function allows a user to capture data about a shoe and use this data to create a shoe object and append this object inside the shoe list.
    country = input("Enter country of origin: ")
    code = input("Enter code of the shoe: ")
    product = input("Enter name of the shoe: ")
    cost = float(input("Enter cost of the shoe: "))
    quantity = int(input("Enter quantity of the shoe: "))
    shoe = Shoe(country, code, product, cost, quantity)
    shoes.append(shoe)
    print("Shoe added successfully!")
    with open("inventory.txt", "a") as f:
        f.write(f"{country}, {code}, {product}, {cost}, {quantity}\n")

def view_all():
    # This function iterates over the shoes list and print the details of the shoes returned from the __str__ function
    headers = ["Code", "Product", "Country", "Cost", "Quantity"]
    rows = [[shoe.code, shoe.product, shoe.country, shoe.cost, shoe.quantity] for shoe in shoes]
    print(tabulate(rows, headers=headers))

def restock():
    # This function will find the shoe object with the lowest quantity, which is the shoes that need to be re-stocked. Ask the user if they want to add this quantity of shoes and then update it.

    # Find the shoe object with the lowest quantity using lambda
    min_quantity_shoe = min(shoes, key=lambda shoe: shoe.get_quantity())
    # Ask the user if they want to add this quantity of shoes
    print(f"The shoe with the lowest quantity is {min_quantity_shoe}.\n")
    user_input = input("Do you want to add this quantity of shoes? (y/n): ")

    # Update the quantity of the shoe object
    if user_input.lower() == "y":
        new_quantity = int(input(f"How many {min_quantity_shoe.product}s do you want to add?: "))
        min_quantity_shoe.quantity += new_quantity
        print(f"{new_quantity} {min_quantity_shoe.product}s added to the inventory.")
        
        # Update the inventory.txt file
        with open("inventory.txt", "r+") as f:
            data = f.readlines()
            f.seek(0)
            for line in data:
                if line.split(",")[1] == min_quantity_shoe.code:
                    line_data = line.split(",")
                    line_data[4] = str(int(line_data[4]) + new_quantity)
                    line = ",".join(line_data)
                f.write(line)
            f.truncate()
    else:
        print("No changes have been made to the inventory.")

def search_shoe():
    # This function searches for a shoe from the list using the shoe code and returns this object so that it will be printed.
    code = input("Enter the code of the shoe to search for: ")
    for shoe in shoes:
        if shoe.code == code:
            return shoe
    print("The shoe with the specified code was not found.")
    return None

def value_per_item():
    # This function calculates the total value for each item and prints this information on the console for all the shoes.
    # Print a header for the shoe value table
    print("Shoe value per item:")
    print("---------------------")
    for shoe in shoes:
        # Calculate the total value of the shoe (cost * quantity)
        value = shoe.get_cost() * shoe.get_quantity()
        # Print the shoe's product name, code, and calculated value
        print(f"{shoe.product} ({shoe.code}): ${value:.2f}")

def highest_qty():
    # This code finds the product with the highest quantity and prints this shoe as being for sale.
    highest_qty_shoe = max(shoes, key=lambda shoe: shoe.get_quantity())
    print(f"{highest_qty_shoe.product} ({highest_qty_shoe.code}) is for sale with the highest quantity of {highest_qty_shoe.get_quantity()} pieces")
 
read_shoes_data()   

#==========Main Menu=============
while True:
    print("===== Shoe Inventory Management =====")
    print("1. View all shoes")
    print("2. Add new shoe")
    print("3. Re-stock shoes")
    print("4. Search for a shoe")
    print("5. Show value per item")
    print("6. Show product with the highest quantity")
    print("7. Exit")

    choice = input("Enter your choice: ")
    
    if choice == "1":
        view_all()
    elif choice == "2":
        capture_shoes()
    elif choice == "3":
        restock()
    elif choice == "4":
        shoe = search_shoe()
        if shoe is not None:
            print(shoe)
    elif choice == "5":
        value_per_item()
    elif choice == "6":
        highest_qty()
    elif choice == "7":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
