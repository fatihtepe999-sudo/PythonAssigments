import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox


class AnnouncementScraper:
    def __init__(self):
        self.base_url = "https://www.medipol.edu.tr/en/announcements"


    # This function takes title, date and link for announcement
    def get_announcements(self, page):
        url = f"{self.base_url}?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed to retrieve page {url}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        announcement_divs = soup.find_all('div', class_='col-md-4 col-sm-6 list-card')

        announcements = []
        for div in announcement_divs:
            link = div.find('a')['href']
            title_element = div.find('h2')
            title = title_element.text.strip() if title_element else "Title not found"
            date_element = div.find('span', class_='date')
            date = date_element.text.strip() if date_element else "Date not found"
            announcements.append({'title': title, 'date': date, 'link': link})

        print(f"{len(announcements)} announcements scraped from {url}")
        return announcements

    # This function takes content in announcements
    def get_announcement_content(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to retrieve content"

        soup = BeautifulSoup(response.content, 'html.parser')
        content_divs = soup.find_all('div', class_='paragraph')
        content = '\n\n'.join([content_div.text.strip() for content_div in content_divs]) if content_divs else "Content not found"
        return content


class AnnouncementGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Medipol University Announcement")
        self.master.geometry("1200x600")  # Set window size

        # Frame for the headers
        self.header_frame = tk.Frame(master)
        self.header_frame.grid(row=0, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="w")

        # Announcements label
        self.announcement_label = tk.Label(self.header_frame, text="Announcements", font=("Arial", 14))
        self.announcement_label.grid(row=0, column=0, padx=130, pady=(10, 0), sticky="w")

        # Content of Announcement label
        self.content_label = tk.Label(self.header_frame, text="Content of Announcement", font=("Arial", 14))
        self.content_label.grid(row=0, column=1, padx=100, pady=(10, 0), sticky="w")

        # Date label
        self.date_var = tk.StringVar()
        self.date_label = tk.Label(self.header_frame, textvariable=self.date_var, font=("Arial", 12))
        self.date_label.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="e")

        # Listbox for announcements
        self.announcement_listbox = tk.Listbox(master, width=80, height=30)
        self.announcement_listbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nwse")

        # Text widget for announcement details
        self.details_text = tk.Text(master, height=20, width=80)
        self.details_text.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nwse")
        self.details_text.config(state="normal", selectbackground="blue", selectforeground="white")

        self.announcements = []
        self.current_announcement = None
        self.selected_index = None  
        self.scraper = AnnouncementScraper()

        self.scrape_announcements()  # Automatically scrape announcements on startup

    def scrape_announcements(self):
        self.announcement_listbox.delete(0, tk.END)
        self.announcements = []
        total_announcements = 0
        for page in range(6):
            announcements = self.scraper.get_announcements(page)
            total_announcements += len(announcements)
            self.announcements.extend(announcements)

        self.populate_listbox()


    #  Fill the listbox
    def populate_listbox(self):
        for index, announcement in enumerate(self.announcements):
            self.announcement_listbox.insert(tk.END, announcement['title'])
        self.announcement_listbox.bind('<<ListboxSelect>>', self.show_announcement_details)
        if self.announcements:
            self.announcement_listbox.selection_set(0)
            self.show_announcement_details(None)

    def show_announcement_details(self, event):
        selection = self.announcement_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_index = index  # Save chosen one
            self.current_announcement = self.announcements[index]
            self.highlight_selected_item(index)
            self.display_announcement_details()

    def highlight_selected_item(self, index):
        self.announcement_listbox.itemconfig(index, {'bg': 'light blue'})  # change color for chosen ones

    # This function display announcement details
    def display_announcement_details(self):
        self.details_text.delete(1.0, tk.END)
        content = self.scraper.get_announcement_content(self.current_announcement['link'])
        self.date_var.set(self.current_announcement['date'])
        self.details_text.insert(tk.END, f"{content}\n\nURL: {self.current_announcement['link']}\n")
        # Add title of announcment to GUI title
        self.master.title(f"Medipol University Announcement - {self.current_announcement['title']}")


root = tk.Tk()
app = AnnouncementGUI(root)
root.mainloop()
