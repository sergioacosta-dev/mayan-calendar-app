from datetime import datetime

# Constants
MOONS = [
    "Magnetic", "Lunar", "Electric", "Self-Existing", "Overtone", "Rhythmic",  
    "Resonant", "Solar", "Planetary", "Spectral", "Crystal", "Cosmic"  
]
DAYS = [
    "Dali", "Seli", "Gamma", "Kali", "Alpha", "Limi", "Silio"  
]
SEALS = [
    "Red Dragon", "White Wind", "Blue Night", "Yellow Seed", "Red Serpent", "White Worldbridger",  
    "Blue Hand", "Yellow Star", "Red Moon", "White Dog", "Blue Monkey", "Yellow Human",   
    "Red Skywalker", "White Wizard", "Blue Eagle", "Yellow Warrior", "Red Earth", "White Mirror",   
    "Blue Storm", "Yellow Sun"  
]
TONES = [
    "Magnetic", "Lunar", "Electric", "Self-Existing", "Overtone", "Rhythmic", "Resonant",  
    "Galactic", "Solar", "Planetary", "Spectral", "Crystal", "Cosmic"  
]
A = [
    "Unify", "Polarize", "Activate", "Define", "Empower", "Organize",  
    "Channel", "Harmonize", "Pulse", "Perfect", "Dissolve", "Dedicate", "Endure"  
]
B = [
    "Nurture", "Communicate", "Dream", "Target",
     "Survive", "Equalize", "Know", "Beautify", "Purify", 
    "Love", "Play", "Influence", "Explore", "Enchant", "Create", "Question",  
    "Evolve", "Reflect", "Catalyze", "Enlighten"  
]
C = [
    "Attracting", "Stabilizing", "Bonding", "Measuring", "Commanding", "Balancing",  
    "Inspiring", "Modeling", "Realizing", "Producing", "Releasing", "Universalizing", "Transcending"  
]
D = [
    "Being", "Breath", "Intuition", "Awareness", "Instinct", "Opportunity", "Healing", "Art",  
    "Flow", "Loyalty", "Illusion", "Wisdom", "Wakefulness", "Receptivity", "Mind",  
    "Fearlessness", "Synchronicity", "Order", "Energy", "Life"  
]
E = [
    "Input", "Store", "Process", "Output", "Matrix"  
]
F = [
    "Birth", "Spirit", "Abundance", "Flowering",
     "Life Force", "Death", "Accomplishment", "Elegance",
    "Universal Water", "Heart", "Magic", "Free Will", "Space", "Timelessness", "Vision",  
    "Intelligence", "Navigation", "Endlessness", "Self-Generation", "Universal Fire"  
]
G = [
    "Magnetic", "Lunar", "Electric", "Self-Existing",
     "Overtone", "Rhythmic", "Resonant", "Galactic",
    "Solar", "Planetary", "Spectral", "Crystal", "Cosmic"  
]
H = [
    "Purpose", "Challenge", "Service", "Form", "Radiance", "Equality", "Attunement",  
    "Integrity", "Intention", "Manifestation", "Liberation", "Cooperation", "Presence"  
]
FACE = [
    "Empty", "Half-Empty", "Full", "Half-Full"  
]

def get_today_moon_data():
    today = datetime.now()
    is_day_out_of_time = (today.month == 7 and today.day == 25)
    if is_day_out_of_time:
    	return {
            "is_day_out_of_time": True,
            "message": "Day Out of Time — A sacred pause. Use it for creativity, rest, and reflection."
        }
    # determine start of current 13‑moon year
    if today.month < 7 or (today.month == 7 and today.day < 26):
        start_year = today.year - 1
    else:
        start_year = today.year
    START_DATE = datetime(start_year, 7, 26)
      
    days_since_start = (today - START_DATE).days  
    if days_since_start < 0:
        return {"error": "Date is before start of 13 Moon calendar"}
    
    # Moon & day
    moon_index = (days_since_start // 28) % 13
    moon_name = MOONS[moon_index]
    moon_number = moon_index + 1
    moon_day = (days_since_start % 28) + 1
    moon_dow = ((moon_day - 1) % 7) + 1
    moon_day_name = DAYS[moon_dow - 1]
  
    # Seal, tone, and guide
    if today.month <= 7 and today.day <= 25:
        tone_offset = (today.year - 2020) % 13
    else:
        tone_offset = ((today.year - 2020) + 1) % 13
    if today.month <= 7 and today.day <= 25:
        seal_offset = (today.year - 2007) % 20
    else:
        seal_offset = ((today.year - 2007) + 5) % 20
          
    tone_num = (days_since_start + tone_offset) % 13
    tone = TONES[tone_num]
    seal_num = (days_since_start + seal_offset) % 20
    seal = SEALS[seal_num]
      
    # Guide logic, cleaned up
    case = (tone_num % 5) + 1
    if case == 1:
        guide_num = seal_num
    elif case == 2:
        guide_num = (seal_num + 12) % 20
    elif case == 3:
        guide_num = (seal_num + 4) % 20
    elif case == 4:
        guide_num = (seal_num + 16) % 20
    else:  # case == 5
        guide_num = (seal_num + 8) % 20
    guide = SEALS[guide_num]
          
    creative_power = A[(days_since_start + tone_offset) % 13]
    b = B[(days_since_start + seal_offset) % 20]
    action = C[((days_since_start + tone_offset) - 1) % 13]
    d = D[(days_since_start - seal_offset) % 20]
    if ((days_since_start - seal_offset) % 20) <= 5:
        e = E[0]
    elif ((days_since_start - seal_offset) % 20) > 5 and ((days_since_start - seal_offset) % 20) <= 10:
        e = E[1]
    elif ((days_since_start - seal_offset) % 20) > 10 and ((days_since_start - seal_offset) % 20) <= 15:
        e = E[2]
    elif ((days_since_start - seal_offset) % 20) > 15 and ((days_since_start - seal_offset) % 20) <= 20:
        e = E[3]
    f = F[(days_since_start - seal_offset) % 20]
    tone_name = G[((days_since_start + tone_offset) - 1) % 13]
    function = H[((days_since_start + tone_offset) - 1) % 13]
      
    # Daily affirmation
    if (((days_since_start + tone_offset) ) % 13) % 5 == 0:
        daily_affirmation = f"I {creative_power} in order to {b}\n{action} {d}\nI seal the {e} of {f}\nWith the {tone_name} tone of {function}\nI am guided by my own power doubled"  
    else:
        daily_affirmation = f"I {creative_power} in order to {b}\n{action} {d}\nI seal the {e} of {f}\nWith the {tone_name} tone of {function}\nI am guided by the power of {f}"
  
    return {
        "moon_number": moon_number,  
        "moon_name":   moon_name,  
        "moon":        f"Moon {moon_number}: {moon_name}",  
        "moon_day":    moon_day,  
        "moon_day_of_week": f"Day {moon_dow}",  
        "moon_day_name" : moon_day_name,  
        "seal":        seal,  
        "tone":        tone,  
        "guide":       guide,  
        "daily_affirmation": daily_affirmation,
        "is_day_out_of_time": False
    }
  
def get_kin_for_date(year: int, month: int, day: int) -> dict:
    date = datetime(year, month, day)
    if date.month < 7 or (date.month == 7 and date.day < 26):
        start_year = date.year - 1
    else:
        start_year = date.year
    start = datetime(start_year, 7, 26)
  
    days = (date - start).days
    if days < 0:
        # Shift to previous cycle
        start = datetime(start_year - 1, 7, 26)
        days = (date - start).days
  
    kin = (days % 260) + 1
    tone_idx = (kin - 1) % 13
    seal_idx = (kin - 1) % 20
    tone = TONES[tone_idx]
    seal = SEALS[seal_idx]
    
    # Guide calculation
    case = (tone_idx % 5) + 1
    if case == 1:
        guide_idx = seal_idx
    elif case == 2:
        guide_idx = (seal_idx + 16) % 20
    elif case == 3:
        guide_idx = (seal_idx + 8) % 20
    elif case == 4:
        guide_idx = (seal_idx + 20) % 20
    else:
        guide_idx = (seal_idx + 13) % 20
    guide = SEALS[guide_idx]
  
    return {
        "kin_number": kin,  
        "tone": tone,  
        "seal": seal,  
        "guide": guide  
    }
  
# Debugging output
if __name__ == "__main__":
    data = get_today_moon_data()
    for key, value in data.items():
        print(f"{key}: {value}")
        

# Galactic Signature Finder Based on Year + Month + Day Method

year_table = {1939: 247, 1940: 92, 1941: 197, 1942: 42, 1943: 147, 1944: 252, 1945: 97, 1946: 202, 1947: 47, 1948: 152, 1949: 257, 1950: 102, 1951: 207, 1952: 52, 1953: 157, 1954: 2, 1955: 107, 1956: 212, 1957: 57, 1958: 162, 1959: 7, 1960: 112, 1961: 217, 1962: 62, 1963: 167, 1964: 12, 1965: 117, 1966: 222, 1967: 67, 1968: 172, 1969: 17, 1970: 122, 1971: 227, 1972: 72, 1973: 177, 1974: 22, 1975: 127, 1976: 232, 1977: 77, 1978: 182, 1979: 27, 1980: 132, 1981: 237, 1982: 82, 1983: 187, 1984: 32, 1985: 137, 1986: 242, 1987: 87, 1988: 192, 1989: 37, 1990: 142, 1991: 247, 1992: 92, 1993: 197, 1994: 42, 1995: 147, 1996: 252, 1997: 97, 1998: 202, 1999: 47, 2000: 152, 2001: 257, 2002: 102, 2003: 207, 2004: 52, 2005: 157, 2006: 2, 2007: 107, 2008: 212, 2009: 57, 2010: 162, 2011: 7, 2012: 112, 2013: 217, 2014: 62, 2015: 167, 2016: 12, 2017: 117, 2018: 222, 2019: 67, 2020: 172, 2021: 17, 2022: 122, 2023: 227, 2024: 72}

month_table = {1: 0, 2: 31, 3: 59, 4: 90, 5: 120, 6: 151, 7: 181, 8: 212, 9: 243, 10: 13, 11: 44, 12: 74}

def get_signature_by_birthdate(year: int, month: int, day: int) -> dict:
    year_value = year_table.get(year)
    if year_value is None:
        raise ValueError(f"Year {year} is not supported.")

    month_value = month_table.get(month)
    if month_value is None:
        raise ValueError(f"Invalid month: {month}")

    kin = year_value + month_value
    while kin > 260:
        kin -= 260

    tone_idx = (kin - 1) % 13
    seal_idx = (kin - 1) % 20
    tone = TONES[tone_idx]
    seal = SEALS[seal_idx]

    return {
        "kin_number": kin,
        "tone": tone,
        "seal": seal,
        "guide": SEALS[(seal_idx + 13) % 20]
    }
