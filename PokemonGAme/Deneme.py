import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import csv
player_1_score = 0
player_2_score = 0
total_of_attack = 0
# İstediğiniz Pokemonların listesi
pokemon_list = [
    "Bulbasaur", "Ivysaur", "Venusaur",
    "Charmander", "Charmeleon", "Charizard",
    "Squirtle", "Wartortle", "Blastoise",
    "Caterpie", "Metapod", "Butterfree",
    "Weedle", "Kakuna", "Beedrill",
    "Pidgey", "Pidgeotto", "Pidgeot"
]

# Geçici bir dosya adı
temp_csv_filename = "temp_pokemon.csv"

# Geçici CSV dosyasını oluştur ve başlık satırını yaz
with open(temp_csv_filename, mode="w", newline="") as temp_file:
    writer = csv.writer(temp_file)
    writer.writerow(["Name", "Type 1", "HP", "Attack"])

    # Eski CSV dosyasını aç ve istenilen Pokemonların özelliklerini geçici dosyaya yaz
    with open("pokemon.csv", mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Name"] in pokemon_list:
                writer.writerow([row["Name"], row["Type 1"], row["HP"], row["Attack"]])

# Geçici dosyayı orijinal dosya adıyla değiştirerek üzerine yaz
os.replace(temp_csv_filename, "pokemon.csv")


class Pokemon:
    def __init__(self, name, type1, hp, attack, image_path=None):
        self.name = name
        self.type1 = type1
        self.total_start = hp*5
        self.hp = hp*5
        self.attack = attack
        self.image_path = image_path
        self.image = None

    def __str__(self):
        return f"Name: {self.name}, Type 1: {self.type1},HP: {self.hp}, Attack: {self.attack}"

    def load_image(self):
        if self.image_path and os.path.exists(self.image_path):
            img = Image.open(self.image_path)
            img = img.resize((200, 200), Image.BICUBIC)
            self.image = ImageTk.PhotoImage(img)
        else:
            # Default image if path doesn't exist
            default_image_path = "none.png"
            default_img = Image.open(default_image_path)
            default_img = default_img.resize((200, 200), Image.BICUBIC)
            self.image = ImageTk.PhotoImage(default_img)

def change_pokemons(pokemon_died, pokemon_evolved):
    print(pokemon_died)
    window.geometry("400x400")
    default_image_path = "none.png"
    default_image = Image.open(default_image_path)
    default_image = default_image.resize((200, 200), Image.BICUBIC)
    default_photo = ImageTk.PhotoImage(default_image)

    for widget in window.winfo_children():
        widget.destroy()
    if total_of_attack%2==1:

        # Create a Listbox on the left side of the window
        pokemon_listbox = tk.Listbox(window, width=20, height=18)
        pokemon_listbox.grid(row=1, column=5, padx=20)

        # Create a Frame on the right side of the window for displaying the Pokemon images
        image_frame = tk.Frame(window)
        image_frame.grid(row=1, column=0)

        # Create a Label for displaying the Pokemon images with a default image "none.png"

        pokemon_image_label = tk.Label(image_frame, image=default_photo)
        pokemon_image_label.image = default_photo
        pokemon_image_label.grid(row=0, column=0, pady=10)

        player_1_label = tk.Label(window, text=" Player 2 chooses Pokemon")
        player_1_label.grid(row=0, column=0, pady=10, columnspan=10)

        choose = tk.Button(image_frame, text="Choose!",
                           command=lambda: go_to_war_again(pokemon_died, pokemon_evolved, pokemon_listbox))
        choose.grid(row=1, column=0)
        messagebox.showinfo("Lose!", f"{pokemon_died.name} lost Player 2 chooses a pokemon and Player 1 gets evolved!")

    elif  total_of_attack%2==0:
        # Create a Listbox on the left side of the window
        pokemon_listbox = tk.Listbox(window, width=20, height=18)
        pokemon_listbox.grid(row=1, column=0, padx=20)

        # Create a Frame on the right side of the window for displaying the Pokemon images
        image_frame = tk.Frame(window)
        image_frame.grid(row=1, column=5)

        # Create a Label for displaying the Pokemon images with a default image "none.png"

        pokemon_image_label = tk.Label(image_frame, image=default_photo)
        pokemon_image_label.image = default_photo
        pokemon_image_label.grid(row=0, column=0, pady=10)

        player_1_label = tk.Label(window, text=" Player 1 chooses Pokemon")
        player_1_label.grid(row=0, column=0, pady=10, columnspan=10)

        choose = tk.Button(image_frame, text="Choose!", command= lambda : go_to_war_again(pokemon_died, pokemon_evolved, pokemon_listbox))
        choose.grid(row=1, column=0)
        messagebox.showinfo("Lose!", f"{pokemon_died.name} lost Player 1 chooses a pokemon and Player 2 gets evolved!")

    load_pokemon_data(pokemon_listbox)

    pokemon_listbox.bind("<<ListboxSelect>>", lambda event: pokemon_selected(event, pokemon_listbox, pokemon_image_label))


def create_health_bar(pokemon_defend, pokemon_attack, player__frame):
    global player_1_score
    global player_2_score
    if pokemon_defend.hp <= 0:
        print("change pokemon")
        if total_of_attack % 2 == 0:
            player_2_score += 1
        else:
            player_1_score += 1
        if player_1_score == 3:
            messagebox.showinfo("Win!", "Player 1 Won!")
            window.destroy()
        elif player_2_score == 3:
            messagebox.showinfo("Win!", "Player 2 Won!")
            window.destroy()
        else:
            change_pokemons(pokemon_defend, pokemon_attack)

    else:
        player__canvas = tk.Canvas(player__frame, width=200, height=20, bg='white')
        player__canvas.grid(row=2, column=0)
        # Draw Player 1 health bar
        player__start = pokemon_defend.total_start
        player__current = pokemon_defend.hp
        player__canvas.create_rectangle(0, 0, (player__current/player__start)*200, 20, fill='green')  # Green bar
        player__canvas.create_rectangle(200, 0, 200 - ((1-(player__current / player__start)) * 200), 20,
                                        fill='red')  # Red portion indicating current health
        # Display Player 1 health value
        player_1_health_label = tk.Label(player__frame, text=f"HP: {player__current}/{player__start}")
        player_1_health_label.grid(row=2, column=1)


def attack_information(pokemon_attack, pokemon_defend, damage, player__frame):
    messagebox.showinfo(f"{pokemon_attack.name} Attacks!", f"{pokemon_attack.name} hit {damage} damage!")
    create_health_bar(pokemon_defend, pokemon_attack, player__frame)


def physical_attack_button(pokemon_attack, pokemon_defend, player_defend_frame, phy_button_attack, elmt_button_attack, phy_button_defend, elmt_button_defend):
    global total_of_attack
    total_of_attack += 1
    print(total_of_attack)
    attack_percentage = random.randint(75, 100)
    attack_value = int(pokemon_attack.attack * (attack_percentage / 100))
    pokemon_defend.hp = pokemon_defend.hp-attack_value
    phy_button_attack.config(state=tk.DISABLED)
    elmt_button_attack.config(state=tk.DISABLED)

    phy_button_defend.config(state=tk.NORMAL)
    elmt_button_defend.config(state=tk.NORMAL)
    attack_information(pokemon_attack, pokemon_defend, attack_value, player_defend_frame)


def elemental_attack_button(pokemon_attack, pokemon_defend, player__frame, phy_button_attack, elmt_button_attack, phy_button_defend, elmt_button_defend):
    global total_of_attack
    total_of_attack += 1
    print(total_of_attack)
    attack_percentage = random.randint(50, 100)
    attack_value = int(pokemon_attack.attack * (attack_percentage / 100))
    phy_button_attack.config(state=tk.DISABLED)
    elmt_button_attack.config(state=tk.DISABLED)
    phy_button_defend.config(state=tk.NORMAL)
    elmt_button_defend.config(state=tk.NORMAL)
    list_of_weakness = ["Water Fire", "Fire Grass", "Grass Water", "Bug Normal", "Normal Bug"]
    if f"{pokemon_attack.type1} {pokemon_defend.type1}" in list_of_weakness:
        critical_attack_chance = random.randint(0, 100)
        if critical_attack_chance <= 80:
            damage = attack_value * 2
            pokemon_defend.hp -= damage
            messagebox.showwarning("Critical", "Critical!")
            attack_information(pokemon_attack, pokemon_defend, damage, player__frame)

        else:
            pokemon_defend.hp -= attack_value
            attack_information(pokemon_attack, pokemon_defend, attack_value, player__frame)
    else:
        pokemon_defend.hp -= attack_value
        attack_information(pokemon_attack, pokemon_defend, attack_value, player__frame)




# Create the Tkinter window
window = tk.Tk()
window.title("Pokemon")
window.geometry("400x400")

# Create a Listbox on the left side of the window
pokemon_listbox = tk.Listbox(window, width=20, height=18)
pokemon_listbox.grid(row=1, column=0, padx=20)

# Create a Frame on the right side of the window for displaying the Pokemon images
image_frame = tk.Frame(window)
image_frame.grid(row=1, column=5)

# Create a Label for displaying the Pokemon images with a default image "none.png"
default_image_path = "none.png"
default_image = Image.open(default_image_path)
default_image = default_image.resize((200, 200), Image.BICUBIC)
default_photo = ImageTk.PhotoImage(default_image)

pokemon_image_label = tk.Label(image_frame, image=default_photo)
pokemon_image_label.image = default_photo
pokemon_image_label.grid(row=0, column=0, pady=10)

player_1_label = tk.Label(window, text=" Player 1 chooses Pokemon")
player_1_label.grid(row=0, column=0, pady=10, columnspan=10)



def war_screen(player_1_pokemon, player_2_pokemon):
    for widget in window.winfo_children():
        widget.destroy()



    window.geometry("650x400")
    player_1_frame = tk.Frame(window)
    player_1_frame.grid(row=0, column=0, sticky="w", padx=40, pady=30)
    player_2_frame = tk.Frame(window)
    player_2_frame.grid(row=0, column=1, sticky="e")

    name_1_label = tk.Label(player_1_frame, text="Player1")
    name_1_label.grid(row=0, column=0)
    name_2_label = tk.Label(player_2_frame, text="Player2")
    name_2_label.grid(row=0, column=0)

    score_1_label = tk.Label(player_1_frame, text=f"Score: {player_1_score}")
    score_1_label.grid(row=1, column=0)
    score_2_label = tk.Label(player_2_frame, text=f"Score: {player_2_score}")
    score_2_label.grid(row=1, column=0)

    # Load images for player Pokémons
    player_1_pokemon.load_image()
    player_2_pokemon.load_image()
    # Display Player Pokémons
    player_1_label = tk.Label(player_1_frame, image=player_1_pokemon.image)
    player_1_label.grid(row=3, column=0)
    player_2_label = tk.Label(player_2_frame, image=player_2_pokemon.image)
    player_2_label.grid(row=3, column=0)

    # Create a canvas for Player 1 health bar
    create_health_bar(player_1_pokemon, player_2_pokemon, player_1_frame)
    create_health_bar(player_2_pokemon, player_1_pokemon, player_2_frame)

    # Attack Buttons
    frame_for_player_1_buttons = tk.Frame(player_1_frame)
    frame_for_player_1_buttons.grid(row=4, column=0)

    frame_for_player_2_buttons = tk.Frame(player_2_frame)
    frame_for_player_2_buttons.grid(row=4, column=0)

    player_1_physical_button = tk.Button(frame_for_player_1_buttons, text="Physical", command=lambda: physical_attack_button(player_1_pokemon, player_2_pokemon, player_2_frame, player_1_physical_button, player_1_elemental_button, player_2_physical_button, player_2_elemental_button))
    player_1_physical_button.grid(row=0, column=0)
    player_1_elemental_button = tk.Button(frame_for_player_1_buttons, text="Elemental", command=lambda: elemental_attack_button(player_1_pokemon, player_2_pokemon, player_2_frame, player_1_physical_button, player_1_elemental_button, player_2_physical_button, player_2_elemental_button))
    player_1_elemental_button.grid(row=0, column=1)

    player_2_physical_button = tk.Button(frame_for_player_2_buttons, text="Physical", command=lambda: physical_attack_button(player_2_pokemon, player_1_pokemon, player_1_frame, player_2_physical_button, player_2_elemental_button, player_1_physical_button, player_1_elemental_button))
    player_2_physical_button.grid(row=0, column=0)
    player_2_elemental_button = tk.Button(frame_for_player_2_buttons, text="Elemental", command=lambda: elemental_attack_button(player_2_pokemon, player_1_pokemon, player_1_frame, player_2_physical_button, player_2_elemental_button, player_1_physical_button, player_1_elemental_button))
    player_2_elemental_button.grid(row=0, column=1)

    if total_of_attack%2==0:
        player_2_physical_button.config(state=tk.DISABLED)
        player_2_elemental_button.config(state=tk.DISABLED)
    elif total_of_attack%2==1:
        player_1_physical_button.config(state=tk.DISABLED)
        player_1_elemental_button.config(state=tk.DISABLED)

def go_to_war_again(pokemon_died,pokemon_lived,pokemon_listbox):
    global player_1_score
    global player_2_score
    pokemon_died_name=pokemon_listbox.get(pokemon_listbox.curselection())
    pokemon_died = get_pokemon_details(pokemon_died_name)
    pokemon_died.load_image()
    pokemon_evolved=get_pokemon_details_for_evolved(pokemon_lived.name)
    pokemon_evolved.load_image()
    pokemon_evolved.hp = int(pokemon_evolved.hp*70/100)
    print(pokemon_died.name)
    if total_of_attack%2==0:
        war_screen(pokemon_died, pokemon_evolved)
    else:
        war_screen(pokemon_evolved, pokemon_died)


def choose_button_clicked2(player_1_pokemon):
    selected_pokemon_name = pokemon_listbox.get(pokemon_listbox.curselection())
    player_2_pokemon = get_pokemon_details(selected_pokemon_name)
    player_2_pokemon.load_image()  # Load image for player 2 pokemon
    war_screen(player_1_pokemon, player_2_pokemon)


def choose_button_clicked():
    pokemon_image_label.config(image=default_photo)
    player_1_label.config(text="Player 2 chooses Pokemon")
    pokemon_listbox.grid(row=1, column=5, padx=20)
    image_frame.grid(row=1, column=0)
    pokemon_image_label.grid(row=0, column=0, pady=10)
    choose.grid(row=1, column=0)
    choose.config(text="Choose!", command= lambda: choose_button_clicked2(player_1_pokemon))
    selected_pokemon_name = pokemon_listbox.get(pokemon_listbox.curselection())
    player_1_pokemon = get_pokemon_details(selected_pokemon_name)
    player_1_pokemon.load_image()  # Load image for player 1 pokemon
    pokemon_listbox.selection_clear(0, tk.END)


choose = tk.Button(image_frame, text="Choose!", command=choose_button_clicked)
choose.grid(row=1, column=0)

# Load the Pokemon names from the CSV file into the Listbox
def load_pokemon_data(pokemon_listbox):
    with open('pokemon.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        count = 0
        for row in reader:
            if count % 3 == 0:
                pokemon_listbox.insert(tk.END, row[0])
            count += 1


# Call the function to load Pokemon data
load_pokemon_data(pokemon_listbox)


def pokemon_selected(event,pokemon_listbox,pokemon_image_label):
    selected_pokemon = pokemon_listbox.get(pokemon_listbox.curselection())
    image_path = f"{selected_pokemon}.png"
    if os.path.exists(image_path):
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.BICUBIC)
        pokemon_photo = ImageTk.PhotoImage(image)
        pokemon_image_label.configure(image=pokemon_photo)
        pokemon_image_label.image = pokemon_photo
    else:
        # If the selected pokemon image doesn't exist, show the default image
        pokemon_image_label.configure(image=default_photo)
        pokemon_image_label.image = default_photo


def get_pokemon_details(pokemon_name):
    with open('pokemon.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == pokemon_name:
                return Pokemon(row['Name'], row['Type 1'], int(row['HP']), int(row['Attack']), f"{row['Name']}.png")



def get_pokemon_details_for_evolved(pokemon_name):
    with open('pokemon.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        next_row = False
        for row in reader:
            if next_row:
                # Bir sonraki satırı bulduğumuzda, detayları alıp işleme koyabiliriz
                return Pokemon(row['Name'], row['Type 1'], int(row['HP']), int(row['Attack']), f"{row['Name']}.png")
            if row['Name'] == pokemon_name:
                # İlgili pokemonu bulduğumuzda, bir sonraki satırı almak için next_row değişkenine atayabiliriz
                next_row = True


pokemon_listbox.bind("<<ListboxSelect>>", lambda event: pokemon_selected(event, pokemon_listbox, pokemon_image_label))


# Run the Tkinter application
window.mainloop()
