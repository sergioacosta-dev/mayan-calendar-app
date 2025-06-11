#THE LIVING SPIRAL APP 4/27/25
#pylint:disable=E0606
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import os
import math
import time
from calendar_logic import get_today_moon_data, get_kin_for_date
from iching_logic import (
    get_seed_from_question,
    generate_hexagram_lines,
    get_binary_from_lines,
    find_hexagram,
    load_iching_data
)
from tarot_logic import draw_card, draw_three_cards
from journal_logic import save_journal_entry, load_journal_entry, list_journal_dates, delete_journal_entry

########################################
########################################
# ——— Build UI ———
app = tk.Tk()
app.title("Living Spiral")
app.geometry("400x600")
app.configure(bg="black")

# ——— Load curriculum JSON ———
def load_json(fn):
    path = os.path.join("data", fn)
    with open(path, "r") as f:
        return json.load(f)
curriculum = load_json("living_spiral_curriculum.json")
moon_data = get_today_moon_data()

# ——— Popup helper ———
def show_popup(title, text):
    for window in app.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()
    popup = tk.Toplevel(app)
    popup.title(title)
    popup.configure(bg="black")
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    popup.geometry(f"{screen_width - 50}x{screen_height - 60}+10+0")
    wrapper = tk.Frame(popup, bg="black", padx=10, pady=10)
    wrapper.pack(expand=True, fill="both")
    scrollbar = tk.Scrollbar(wrapper)
    scrollbar.pack(side="right", fill="y")
    text_widget = tk.Text(wrapper, wrap="word", bg="black", fg="white", yscrollcommand=scrollbar.set)
    text_widget.insert("1.0", text)
    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both", padx=(0, 10), pady=(0, 5))
    scrollbar.config(command=text_widget.yview)
    popup.bind("<Escape>", lambda e: popup.destroy())

# ——— If DOT, automatic popup ———
if moon_data.get("is_day_out_of_time"):
    def show_dot_info():
        show_popup("Day Out of Time", moon_data.get("message", "Sacred pause."))
else:
    m_num = moon_data["moon_number"]
    global_day = (m_num - 1) * 28 + moon_data["moon_day"]
    entry = curriculum.get(str(global_day), {})

# ——— Get DOT text———
DAY_OUT_OF_TIME_TEXT = (
    "Day Out of Time — July 25\n\n"
    "This is a sacred pause between cycles.\n"
    "Use it for creativity, release, and renewal.\n\n"
    "Suggestions:\n"
    "- Create something from spirit (art, music, dance)\n"
    "- Reflect on the cycle just completed\n"
    "- Let go of old patterns\n"
    "- Celebrate being a living spiral\n\n"
    "Affirmation:\n"
    "\"I exist beyond time. I am a living spiral.\""
)

# ——— Daily summary frame ———
sf = tk.Frame(app, bg="black")
sf.pack(pady=10)
for line in (
	"The Living Spiral\n",
    f"{moon_data['moon']}",
    f"Moon Day: {moon_data['moon_day']}",
    f"Day of Week: {moon_data['moon_day_of_week']} ({moon_data.get('moon_day_name','')})",
    f"Seal: {moon_data['seal']}",
    f"Tone: {moon_data['tone']}",
    f"Guide: {moon_data['guide']}"
):
    tk.Label(sf, text=line, fg="white", bg="black", font=("Helvetica",12)).pack(anchor="n")

# ——— Multi-Ring Clock ———
def show_clock():
    popup = tk.Toplevel(app)
    popup.title("Multi-Ring Clock")
    popup.configure(bg="black")
    sw, sh = app.winfo_screenwidth(), app.winfo_screenheight()
    popup.geometry(f"{sw-50}x{sh-60}+10+0")

    canvas = tk.Canvas(popup, width=800, height=800, bg="black")
    canvas.pack(fill="both", expand=True)

    CENTER_X, CENTER_Y = 515, 1000
    CLOCK_RADIUS = 100

    RINGS = [
        ("Seconds",   60,   CLOCK_RADIUS+5,   5,  "red"),
        ("Minutes",   60,   CLOCK_RADIUS+25, 10, "orange"),
        ("Hours",     24,   CLOCK_RADIUS+60, 15, "yellow"),
        ("Weekdays",   7,   CLOCK_RADIUS+100,20, "green"),
        ("MonthDays", 28,   CLOCK_RADIUS+150,21, "blue"),
        ("Months",    13,   CLOCK_RADIUS+200,22, "indigo"),
        ("Years",  25920,   CLOCK_RADIUS+250,23, "purple"),
    ]

    def draw_dot(angle, r, color, size, tag=""):
        a = math.radians(angle)
        x = CENTER_X + math.sin(a) * r
        y = CENTER_Y - math.cos(a) * r
        canvas.create_oval(x-size, y-size, x+size, y+size,
                           fill=color, outline="", tags=tag)

    def draw_clock_face():
        canvas.delete("face")
        for _, count, r, _, _ in RINGS:
            for i in range(count):
                draw_dot(i * (360/count), r, "grey30", 3, tag="face")
            draw_dot(0, r, "white", 6, tag="face")

    def draw_legend():
        LEGEND = [
            ("Seconds","red"),("Minutes","orange"),
            ("Hours","yellow"),("Weekdays","green"),
            ("MonthDays","blue"),("Months","indigo"),
            ("Years","purple")
        ]
        items_per_row = 1
        spacing_x   = 150
        spacing_y   = 50
        start_x     = 25
        base_y      = CENTER_Y + CLOCK_RADIUS + 700

        for idx, (label, color) in enumerate(LEGEND):
            row = idx // items_per_row
            col = idx % items_per_row
            x = start_x + col * spacing_x
            y = base_y  + row * spacing_y

            dot_size = 6
            canvas.create_oval(
                x - dot_size, y - dot_size,
                x + dot_size, y + dot_size,
                fill=color, outline="", tags="face"
            )
            canvas.create_text(
                x + dot_size + 4, y,
                text=label,
                fill="white",
                font=("Helvetica", 10),
                anchor="w",
                tags="face"
            )
        
    def update_clock():
        canvas.delete("hands")
        now  = time.localtime()
        moon = get_today_moon_data()

        # convert to int for lunar calendar values
        weekday_raw = str(moon.get("moon_day_of_week", "0"))
        weekday_idx = int(''.join(filter(str.isdigit, weekday_raw))) - 1
        monthday_raw = str(moon.get("moon_day", "1"))
        monthday_idx = int(''.join(filter(str.isdigit, monthday_raw))) - 1
        month_raw = str(moon.get("moon_number", "1"))
        month_idx = int(''.join(filter(str.isdigit, month_raw))) - 1
        yearday_idx = month_idx * 28 + monthday_idx
        
        vals = {
            "Seconds":   now.tm_sec,
            "Minutes":   now.tm_min + now.tm_sec/60,
            "Hours":     (now.tm_hour % 24) + now.tm_min/60,
            "Weekdays":  weekday_idx,
            "MonthDays": monthday_idx,
            "Months":    month_idx,
            # match ring name
            "Years":     yearday_idx
        }

        for name, count, r, size, color in RINGS:
            frac = vals[name] / count
            angle = frac * 360
            draw_dot(angle, r, color, size, tag="hands")

        popup.after(1000, update_clock)

    draw_clock_face()
    draw_legend()
    update_clock()

#——— Find Kin ———
def find_my_kin():
    d = simpledialog.askstring("Birth Date", "Enter your birth date (YYYY-MM-DD):", parent=app)
    if not d:
        return
    try:
        y, m, day = map(int, d.strip().split("-"))
        from calendar_logic import get_signature_by_birthdate
        kin = get_signature_by_birthdate(y, m, day)
        text = f"Kin # {kin['kin_number']}\nTone: {kin['tone']}\nSeal: {kin['seal']}\nGuide: {kin['guide']}"
        show_popup("Your Galactic Signature", text)
    except Exception as e:
        show_popup("Error", f"Could not interpret date.\n{e}")
        
# ——— Button callbacks ———
def show_daily_reading():
    txt = moon_data.get("daily_affirmation", "No affirmation available.")
    show_popup("Daily Reading", txt)
def show_weekly_practice():
    txt = entry.get("weekly_practice", "No practice found.")
    show_popup("Weekly Practice", txt)
def show_monthly_focus():
    txt = (
        f"Theme: {entry.get('theme','')}\n\n"
        f"Affirmation: {entry.get('affirmation','')}\n\n"
        f"Quote: {entry.get('quote','')}"
    )
    show_popup("Monthly Focus", txt)

# Galactic Prayer Text
GALACTIC_PRAYER = (
    "From the East, House of Light\n"
    "May wisdom dawn in us\n"
    "So we may see all things in clarity.\n\n"
    "From the North, House of Night\n"
    "May wisdom ripen in us\n"
    "So we may know all from within.\n\n"
    "From the West, House of Transformation\n"
    "May wisdom be transformed into right action\n"
    "So we may do what must be done.\n\n"
    "From the South, House of the Eternal Sun\n"
    "May right action reap the harvest\n"
    "So we may enjoy the fruits of planetary being.\n\n"
    "From Above, House of Heaven\n"
    "Where star people and ancestors gather\n"
    "May their blessings come to us now.\n\n"
    "From Below, House of Earth\n"
    "May the heartbeat of her crystal core\n"
    "Bless us with harmonies to end all war.\n\n"
    "From the Center, Galactic Source\n"
    "Which is everywhere at once\n"
    "May everything be known\n"
    "As the light of mutual love."
)
def show_galactic_prayer():
        show_popup("Prayer of the 7 Galactic Directions", GALACTIC_PRAYER)

# Rainbow Bridge Text
RAINBOW_BRIDGE_MEDITATION = (
    "RAINBOW BRIDGE MEDITATION\n"
    "Globally synchronized every Silio day.\n\n"
    "1. Visualize yourself inside the Earth's octahedron crystal core.\n"
    "2. Feel your heart at the center of this crystal core generating an intensely blazing point of white light.\n"
    "3. Feel this blazing stream of light transform into multicolored plasma\n"
    "   emanating from your heart core and extending out into the North and South poles.\n"
    "4. Feel the two streams of rainbow light rushing through your spinal column,\n"
    "   shooting out from above your head and beneath your feet to create a rainbow bridge around your body.\n"
    "5. Hold this brilliant pulsing vision for as long as possible; now YOU ARE the Rainbow Bridge!\n"
    "6. The rainbow bridge is the realization of planetary peace.\n"
    "   As Earth revolves on its axis, this rainbow bridge remains steady and constant, unmoving.\n"
    "7. Visualized by enough people in a telepathic wave of love,\n"
    "   we will vibrate into the already existing reality of the Rainbow Bridge."
)
def show_rainbow_bridge():
    show_popup("Rainbow Bridge Meditation", RAINBOW_BRIDGE_MEDITATION)

# Natural Mind Meditaion Text
NATURAL_MIND_MEDITATION = (
    "NATURAL MIND MEDITATION\n"
    "1. Sit still, with spine erect, seated on a chair with feet firmly on the floor or on a cushion or pillow on the floor.\n"
    "2. Keep your eyes slightly opened looking toward the floor.\n"
    "3. Place your hands comfortably on your knees, palms down, or place your right hand on your left hand, palms up, held at the level of your navel.\n"
    "4. Feel your intrinsic dignity in this posture.\n"
    "5. Watch your breath. Breathe normally.\n"
    "6. Practice allowing mind to relax into its natural state.\n"
    "7. As you become aware of your thoughts just label them “thinking” and as you exhale, dissolve the thoughts.\n"
    "8. Note the GAP between the thoughts. It is this GAP that you want to become familiar with and cultivate. It is the seed of natural mind and the key to your true, authentic self."
)
def show_natural_mind():
    show_popup("Natural Mind Meditation", NATURAL_MIND_MEDITATION)

# Sychronic Keys Text
def show_synchronic_keys():
    text = (
        "5 KEYS TO THE SYNCHRONIC ORDER\n\n"
        "1. NATURAL MIND MEDITATION\n"
        "Set aside time each day to practice relaxing the mind into its natural state.\n"
        "Allow your thoughts to dissolve with your out-breath. Not only does this make us feel more calm and centered,\n"
        "it also creates a peaceful anchor to offset the fast-paced world.\n\n"
        "2. WORK EACH DAY TO TURN “NEGATIVES” INTO POSITIVES\n"
        "Our challenge at this time is to remain focused on the world we wish to create.\n"
        "Everything serves to further. Our vibrations affect the whole.\n\n"
        "3. 13 MOON CALENDAR\n"
        "Contemplate the energy of the daily galactic signature.\n"
        "This equips you with a cosmic lens to view daily life events.\n\n"
        "4. KEEP A SYNCHRONICITY JOURNAL\n"
        "The more you focus on synchronicities, the more they increase.\n\n"
        "5. FORM A SYNCHRONIC STUDY GROUP\n"
        "Share synchronicities. Activate new cosmic dialogue and share your highest dreams.\n"
        "Anchor a new consciousness on Earth."
    )
    show_popup("5 Keys to the Synchronic Order", text)
    
# ——— I ching ———
def show_iching():
    question = simpledialog.askstring("I Ching Reading", "What is your question?")
    if not question:
        return
    seed = get_seed_from_question(question)
    lines = generate_hexagram_lines(seed)
    binary = get_binary_from_lines(lines)
    hexagram = find_hexagram(binary, load_iching_data())
    if not hexagram:
        show_popup("Error", "No hexagram found.")
        return
    line_text = "\n".join(
        f"Line {6 - i}: {hexagram['changing_lines'].get(f'line_{6 - i}', '')}"
        for i in range(6)
    )
    text = (
        f"Hexagram {hexagram['number']}: {hexagram['name']}\n"
        f"Binary Code: {binary}\n\n"
        f"Judgment:\n{hexagram['judgment']}\n\n"
        f"Image:\n{hexagram['image']}\n\n"
        f"Changing Lines:\n{line_text}"
    )
    show_popup("I Ching Reading", text)
    
# ——— Tarot ———
def show_tarot_menu():
    popup = tk.Toplevel(app)
    popup.title("Tarot Reading")
    popup.configure(bg="black")
    popup.geometry(f"{app.winfo_screenwidth()-50}x{app.winfo_screenheight()-60}+10+0")
    wrapper = tk.Frame(popup, bg="black", padx=10, pady=10)
    wrapper.pack(expand=True, fill="both")
    ttk.Button(wrapper, text="Single Card Reading", command=show_single_tarot).pack(pady=10, fill="x")
    ttk.Button(wrapper, text="Three Card Spread", command=show_three_tarot).pack(pady=10, fill="x")
    popup.bind("<Escape>", lambda e: popup.destroy())
def show_single_tarot():
    card = draw_card()
    text = (
        f"Card: {card['name']} ({card['orientation'].capitalize()})\n"
        f"Suit: {card['suit']}\n\n"
        f"Meaning:\n{card['meaning']}"
    )
    show_popup("Single Tarot Card Reading", text)
def show_three_tarot():
    cards = draw_three_cards()
    text = ""
    for card in cards:
        text += (
            f"{card['position']}:\n"
            f"{card['name']} ({card['orientation'].capitalize()})\n"
            f"Suit: {card['suit']}\n"
            f"Meaning: {card['meaning']}\n\n"
        )
    show_popup("Three Card Tarot Spread", text)
    
# ——— Journal popup———
def show_journal_popup():
    popup = tk.Toplevel(app)
    popup.title("Daily Journal")
    popup.geometry(f"{app.winfo_screenwidth()-50}x{app.winfo_screenheight()-60}+10+0")
    popup.configure(bg="black")
    wrapper = tk.Frame(popup, bg="black", padx=10, pady=10)
    wrapper.pack(expand=True, fill="both")
    tk.Label(wrapper, text="Today's Journal", fg="white", bg="black", font=("Helvetica", 14)).pack()
    text_box = tk.Text(wrapper, wrap="word", height=25, bg="white", fg="black")
    text_box.pack(expand=True, fill="both")
    text_box.insert("1.0", load_journal_entry())
    def save_entry():
        content = text_box.get("1.0", "end-1c")
        save_journal_entry(content)
        popup.destroy()
    ttk.Button(wrapper, text="Save Entry", command=save_entry).pack(pady=10)
    ttk.Button(wrapper, text="View Past Entries", command=show_journal_archive).pack(pady=5)
    
def custom_confirm_delete(date_str, on_confirm):
    confirm_popup = tk.Toplevel(app)
    confirm_popup.title("Confirm Delete")
    confirm_popup.configure(bg="black")
    confirm_popup.geometry(f"{app.winfo_screenwidth()-50}x{app.winfo_screenheight()-60}+10+0")
    wrapper = tk.Frame(confirm_popup, bg="black", padx=10, pady=10)
    wrapper.pack(expand=True, fill="both")
    tk.Label(wrapper, text=f"Delete entry for {date_str}?", fg="white", bg="black", font=("Helvetica", 12)).pack(pady=10)

    def confirm():
        on_confirm()
        confirm_popup.destroy()

    def cancel():
        confirm_popup.destroy()

    btn_frame = tk.Frame(wrapper, bg="black")
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Yes", command=confirm).pack(side="left", padx=10)
    ttk.Button(btn_frame, text="No", command=cancel).pack(side="left", padx=10)

def show_journal_archive():
    popup = tk.Toplevel(app)
    popup.title("Journal Archive")
    popup.geometry(f"{app.winfo_screenwidth()-50}x{app.winfo_screenheight()-60}+10+0")
    popup.configure(bg="black")
    wrapper = tk.Frame(popup, bg="black", padx=10, pady=10)
    wrapper.pack(expand=True, fill="both")
    dates = list_journal_dates()
    listbox = tk.Listbox(wrapper, height=20, bg="white", fg="black")
    listbox.pack(fill="both", expand=True)
    for date in dates:
        listbox.insert("end", date)
    def show_selected_entry():
        selected = listbox.curselection()
        if selected:
            date_str = listbox.get(selected[0])
            entry = load_journal_entry(date_str)
            show_popup(f"Journal for {date_str}", entry)

    def edit_selected_entry():
        selected = listbox.curselection()
        if selected:
            date_str = listbox.get(selected[0])
            entry = load_journal_entry(date_str)

            def save_edit():
                new_content = edit_box.get("1.0", "end-1c")
                save_journal_entry(new_content)
                popup.destroy()

            popup = tk.Toplevel(app)
            popup.title(f"Edit Journal: {date_str}")
            popup.geometry(f"{app.winfo_screenwidth()-50}x{app.winfo_screenheight()-60}+10+0")
            popup.configure(bg="black")
            wrapper = tk.Frame(popup, bg="black", padx=10, pady=10)
            wrapper.pack(expand=True, fill="both")
            edit_box = tk.Text(wrapper, wrap="word", bg="white", fg="black")
            edit_box.insert("1.0", entry)
            edit_box.pack(expand=True, fill="both")
            ttk.Button(wrapper, text="Save Changes", command=save_edit).pack(pady=10)

    def delete_selected_entry():
    	selected = listbox.curselection()
    	if selected:
        	date_str = listbox.get(selected[0])
        	def on_confirm():
        	   	delete_journal_entry(date_str)
        	   	listbox.delete(selected[0])
        	custom_confirm_delete(date_str, on_confirm)
    ttk.Button(wrapper, text="View Entry", command=show_selected_entry).pack(pady=10)
    ttk.Button(wrapper, text="Edit Entry", command=edit_selected_entry).pack(pady=5)
    ttk.Button(wrapper, text="Delete Entry", command=delete_selected_entry).pack(pady=5)

# ——— Buttons frame ———
btnf = tk.Frame(app, bg="gray15")
btnf.pack(pady=20, fill="x", padx=20)
ttk.Button(btnf, text="Clock", command=show_clock).pack(fill="x", pady=5)
ttk.Button(btnf, text="Find Your Kin", command=find_my_kin).pack(fill="x", pady=5)
ttk.Button(btnf, text="Daily Reading", command=show_daily_reading).pack(fill="x", pady=5)
ttk.Button(btnf, text="Weekly Practice", command=show_weekly_practice).pack(fill="x", pady=5)
ttk.Button(btnf, text="Monthly Focus", command=show_monthly_focus).pack(fill="x", pady=5)
ttk.Button(btnf, text="Galactic Prayer", command=show_galactic_prayer).pack(fill="x", pady=5)
ttk.Button(btnf, text="Rainbow Bridge Meditation", command=show_rainbow_bridge).pack(fill="x", pady=5)
ttk.Button(btnf, text="Natural Mind Meditation", command=show_natural_mind).pack(fill="x", pady=5)
ttk.Button(btnf, text="5 Keys to the Synchronic Order", command=show_synchronic_keys).pack(fill="x", pady=5)
ttk.Button(btnf, text="I Ching Reading", command=show_iching).pack(fill="x", pady=5)
ttk.Button(btnf, text="Tarot Reading", command=show_tarot_menu).pack(fill="x", pady=5)
ttk.Button(btnf, text="Journal", command=show_journal_popup).pack(fill="x", pady=5)

app.mainloop()