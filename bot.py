import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from datetime import datetime, date

TOKEN = "8811357585:AAG2OtX6w5hIwXMTfPYF6WsoW237_DEXpfk"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

sessions = {}

def gs(cid):
    cid = str(cid)
    if cid not in sessions:
        sessions[cid] = {"step": "idle", "d": {}}
    return sessions[cid]

# ── Aerport ma'lumotlari ──────────────────────────────────────────────────────
AP = {
    "toshkent":"TAS","tashkent":"TAS","tas":"TAS",
    "samarqand":"SKD","samarkand":"SKD","skd":"SKD",
    "namangan":"NMA","nma":"NMA",
    "fergana":"FEG","farghona":"FEG","feg":"FEG",
    "urganch":"UGC","urgench":"UGC","ugc":"UGC",
    "nukus":"NCU","ncu":"NCU",
    "moskva":"SVO","moscow":"SVO","svo":"SVO",
    "domodedovo":"DME","dme":"DME",
    "peterburg":"LED","petersburg":"LED","led":"LED",
    "kazan":"KZN","kzn":"KZN",
    "novosibirsk":"OVB","ovb":"OVB",
    "dubai":"DXB","dubay":"DXB","dxb":"DXB",
    "abudhabi":"AUH","auh":"AUH",
    "doha":"DOH","doh":"DOH",
    "riyadh":"RUH","riad":"RUH","ruh":"RUH",
    "istanbul":"IST","ist":"IST",
    "antalya":"AYT","ayt":"AYT",
    "ankara":"ESB","esb":"ESB",
    "london":"LHR","lhr":"LHR",
    "paris":"CDG","cdg":"CDG",
    "berlin":"BER","ber":"BER",
    "amsterdam":"AMS","ams":"AMS",
    "frankfurt":"FRA","fra":"FRA",
    "rome":"FCO","rim":"FCO","fco":"FCO",
    "barcelona":"BCN","bcn":"BCN",
    "madrid":"MAD","mad":"MAD",
    "milan":"MXP","mxp":"MXP",
    "newyork":"JFK","jfk":"JFK","nyc":"JFK",
    "losangeles":"LAX","lax":"LAX",
    "miami":"MIA","mia":"MIA",
    "chicago":"ORD","ord":"ORD",
    "toronto":"YYZ","yyz":"YYZ",
    "beijing":"PEK","pekin":"PEK","pek":"PEK",
    "shanghai":"PVG","pvg":"PVG",
    "seoul":"ICN","seul":"ICN","icn":"ICN",
    "tokyo":"NRT","tokio":"NRT","nrt":"NRT",
    "singapore":"SIN","singapur":"SIN","sin":"SIN",
    "bangkok":"BKK","bkk":"BKK",
    "delhi":"DEL","del":"DEL",
    "mumbai":"BOM","bom":"BOM",
    "almaty":"ALA","olmaota":"ALA","ala":"ALA",
    "astana":"NQZ","nursultan":"NQZ","nqz":"NQZ",
    "bishkek":"FRU","fru":"FRU",
    "baku":"GYD","gyd":"GYD",
    "tbilisi":"TBS","tbs":"TBS",
    "yerevan":"EVN","evn":"EVN",
    "minsk":"MSQ","msq":"MSQ",
    "kyiv":"KBP","kiev":"KBP","kiyev":"KBP","kbp":"KBP",
    "cairo":"CAI","qohira":"CAI","cai":"CAI",
    "sydney":"SYD","syd":"SYD",
    "nairobi":"NBO","nbo":"NBO",
    "johannesburg":"JNB","jnb":"JNB",
}

AN = {
    "TAS":"Toshkent","SKD":"Samarqand","NMA":"Namangan",
    "FEG":"Fargona","UGC":"Urganch","NCU":"Nukus",
    "SVO":"Moskva (SVO)","DME":"Moskva (DME)",
    "LED":"Sankt-Peterburg","KZN":"Qozon","OVB":"Novosibirsk",
    "DXB":"Dubai","AUH":"Abu-Dabi","DOH":"Doha","RUH":"Ar-Riyod",
    "IST":"Istanbul","AYT":"Antalya","ESB":"Ankara",
    "LHR":"London","CDG":"Parij","BER":"Berlin","AMS":"Amsterdam",
    "FRA":"Frankfurt","FCO":"Rim","BCN":"Barselona",
    "MAD":"Madrid","MXP":"Milan",
    "JFK":"Nyu-York","LAX":"Los-Anjeles","MIA":"Miami",
    "ORD":"Chikago","YYZ":"Toronto",
    "PEK":"Pekin","PVG":"Shanxay","ICN":"Seul",
    "NRT":"Tokio","SIN":"Singapur","BKK":"Bangkok",
    "DEL":"Dehli","BOM":"Mumbai",
    "ALA":"Olmaota","NQZ":"Astana","FRU":"Bishkek",
    "GYD":"Boku","TBS":"Tbilisi","EVN":"Yerevan",
    "MSQ":"Minsk","KBP":"Kiyev",
    "CAI":"Qohira","SYD":"Sidney","NBO":"Nayrobi","JNB":"Yoxannesburg",
}

STREETS = {
    "TAS":["Amir Temur kochasi","Mustaqillik maydoni","Yunusobod","Chilonzor"],
    "SKD":["Registon kochasi","Siob bozori","Afrosiyob"],
    "DXB":["Sheikh Zayed Road","Downtown Dubai","Palm Jumeirah","Dubai Marina"],
    "IST":["Istiklal Caddesi","Taksim","Sultanahmet","Besiktas"],
    "LHR":["Oxford Street","Piccadilly","Mayfair","Knightsbridge"],
    "CDG":["Champs-Elysees","Opera","Marais","Montmartre"],
    "BER":["Kurfurstendamm","Mitte","Unter den Linden"],
    "AMS":["Dam Square","Jordaan","Canal Ring","Museum Quarter"],
    "SVO":["Tverskaya","Arbat","Kutuzovsky","Novy Arbat"],
    "JFK":["5th Avenue","Times Square","Broadway","Midtown"],
    "NRT":["Shinjuku","Shibuya","Ginza","Akihabara"],
    "BKK":["Sukhumvit Rd","Silom","Siam","Khao San Rd"],
    "SIN":["Marina Bay","Orchard Road","Clarke Quay","Sentosa"],
    "ALA":["Al-Farabi kochasi","Furmanov kochasi","Dostyk kochasi"],
    "ICN":["Myeongdong","Gangnam","Hongdae","Insadong"],
}

HOTEL_BRANDS = {
    5:["Grand Hyatt","Four Seasons","Ritz-Carlton","Marriott","InterContinental"],
    4:["Hilton","Radisson Blu","Sheraton","DoubleTree","Crowne Plaza"],
    3:["Novotel","Mercure","Holiday Inn","Best Western","ibis Styles"],
    2:["ibis","Travelodge","Premier Inn","Motel One","EasyHotel"],
}
HOTEL_TYPES = ["Hotel","Resort","Suites","Palace","Inn","Grand"]
HOTEL_IMGS = {
    5:["https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80",
       "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=600&q=80",
       "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=600&q=80"],
    4:["https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600&q=80",
       "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80",
       "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=600&q=80"],
    3:["https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=600&q=80",
       "https://images.unsplash.com/photo-1496417263034-38ec4f0b665a?w=600&q=80"],
    2:["https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600&q=80",
       "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&q=80"],
}
AMENITIES = {
    5:["Bepul Wi-Fi","Basseyn","Spa","Restoran","Bar","Trenajyor zal","24/7 Resepshn"],
    4:["Bepul Wi-Fi","Basseyn","Fitnes-zal","Restoran","Bar","Biznes markaz"],
    3:["Wi-Fi","Restoran","Breakfast","Parking","24h Resepshn"],
    2:["Wi-Fi","Nonushta","Resepshn"],
}

CAR_MODELS = {
    "Economy":["Toyota Yaris","Hyundai i20","Kia Picanto","VW Polo","Ford Fiesta"],
    "Standard":["Toyota Camry","Hyundai Elantra","VW Passat","Nissan Altima","Ford Focus"],
    "SUV":["Toyota RAV4","Hyundai Tucson","BMW X5","Ford Explorer","Kia Sportage"],
    "Luxury":["BMW 7 Series","Mercedes E-Class","Audi A8","Lexus ES350","Cadillac CT5"],
    "Minivan":["Toyota Sienna","Honda Odyssey","Kia Carnival","Chrysler Pacifica"],
}
CAR_IMGS = {
    "Economy":"https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=600&q=80",
    "Standard":"https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600&q=80",
    "SUV":"https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=600&q=80",
    "Luxury":"https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&q=80",
    "Minivan":"https://images.unsplash.com/photo-1553440569-bcc63803a83d?w=600&q=80",
}
CAR_FEATS = {
    "Economy":"Konditsioner | Mexanik | 5 orin",
    "Standard":"Konditsioner | Avtomat | 5 orin | Bluetooth",
    "SUV":"Konditsioner | Avtomat | 7 orin | 4x4 | GPS",
    "Luxury":"Full-optsia | Avtomat | 5 orin | GPS | Krujniy kamera",
    "Minivan":"Konditsioner | Avtomat | 7-8 orin | Keng salon",
}

# ── Yordamchi funksiyalar ─────────────────────────────────────────────────────
def get_iata(text):
    low = text.lower().strip().replace(" ", "")
    if low in AP: return AP[low]
    low2 = text.lower().strip()
    if low2 in AP: return AP[low2]
    for k in AP:
        if low2 in k or k in low2: return AP[k]
    return None

def get_name(iata):
    return f"{AN[iata]} ({iata})" if iata in AN else iata

def parse_date(raw):
    norm = raw.replace(".", "-").replace("/", "-")
    try:
        d = datetime.strptime(norm, "%Y-%m-%d").date()
        return norm, d
    except:
        return None, None

def city_tier(iata):
    long = ["LHR","CDG","FRA","AMS","BER","FCO","BCN","MAD","MXP","JFK","LAX","MIA","ORD","YYZ","ICN","NRT","PEK","PVG","SIN","BKK","DEL","BOM","SYD","CAI","NBO","JNB"]
    med  = ["DXB","AUH","DOH","RUH","IST","AYT","ESB","GYD","TBS","EVN","KBP","MSQ"]
    near = ["ALA","NQZ","FRU","SVO","DME","LED","KZN","OVB"]
    if iata in long: return "long"
    if iata in med:  return "med"
    if iata in near: return "near"
    return "near"

def get_flights(frm, to, dt, adults, ret_date=None):
    tier = city_tier(to) if city_tier(to) != "near" else city_tier(frm)
    bases = {"long":(500,1200),"med":(200,500),"near":(80,320)}
    base = random.randint(*bases.get(tier,(180,600)))

    airlines = [("HY","Uzbekistan Airways"),("TK","Turkish Airlines"),("EK","Emirates"),
                ("FZ","flydubai"),("KC","Air Astana"),("SU","Aeroflot"),
                ("QR","Qatar Airways"),("PC","Pegasus"),("S7","S7 Airlines"),("LH","Lufthansa")]
    dep_times = [6,8,10,12,14,16,18,21]
    dur_ranges = {"long":(8,18),"med":(4,8),"near":(1,5)}
    results = []
    used = []
    for i in range(6):
        al = random.choice([a for a in airlines if a[0] not in used] or airlines)
        used.append(al[0])
        dh = dep_times[i % len(dep_times)]
        dm = random.choice([0,5,10,15,20,25,30,35,40,45,50,55])
        durH = random.randint(*dur_ranges.get(tier,(3,9)))
        durM = random.choice([0,15,30,45])
        ah = (dh + durH + (dm + durM) // 60) % 24
        am = (dm + durM) % 60
        stops = 1 if (durH >= 9 or i in [2,4]) else 0
        price = int(base * (1 + i*0.07) * adults)
        if stops: price = int(price * 0.83)
        results.append({
            "price":price,"airline":al[1],"fnum":f"{al[0]}{random.randint(100,999)}",
            "dep":f"{dh:02d}:{dm:02d}","arr":f"{ah:02d}:{am:02d}",
            "dur":f"{durH}h {durM:02d}m","stops":stops,"seats":random.randint(2,18)
        })
    return sorted(results, key=lambda x: x["price"])

def get_hotels(iata, nights, guests):
    city = AN.get(iata, iata)
    tier = city_tier(iata)
    p = {"long":{5:280,4:150,3:80,2:40},"med":{5:200,4:100,3:55,2:30},
         "near":{5:120,4:60,3:35,2:18}}.get(tier,{5:180,4:90,3:50,2:28})
    streets = STREETS.get(iata, ["City Center","Main Street"])
    results = []
    for stars in [5,5,4,4,3,2][:5]:
        brand = random.choice(HOTEL_BRANDS[stars])
        htype = random.choice(HOTEL_TYPES)
        name = f"{brand} {city} {htype}"
        addr = f"{random.choice(streets)} {random.randint(1,200)}, {city}"
        price = int(p[stars] * (1 + random.randint(-15,25)/100) * guests)
        total = price * nights
        rating = round(random.randint(70,99)/10.0, 1)
        img = random.choice(HOTEL_IMGS[stars])
        amen_pool = AMENITIES[stars]
        amen = " | ".join(random.sample(amen_pool, min(4, len(amen_pool))))
        stars_emoji = "⭐" * stars
        results.append({"name":name,"stars":stars,"emoji":stars_emoji,
                        "addr":addr,"price":price,"total":total,
                        "rating":rating,"img":img,"amen":amen})
    return sorted(results, key=lambda x: -x["stars"])

def get_cars(iata, days):
    tier = city_tier(iata)
    p = {"long":{5:35,4:60,3:90,2:150,1:75},"med":{5:25,4:45,3:70,2:120,1:55},
         "near":{5:15,4:25,3:40,2:70,1:35}}.get(tier,{5:22,4:40,3:65,2:110,1:50})
    prices = {"Economy":p[5],"Standard":p[4],"SUV":p[3],"Luxury":p[2],"Minivan":p[1]}
    results = []
    for cat in ["Economy","Standard","SUV","Luxury","Minivan"]:
        model = random.choice(CAR_MODELS[cat])
        price = int(prices[cat] * (1 + random.randint(-10,20)/100))
        results.append({"cat":cat,"model":model,"price":price,
                        "total":price*days,"img":CAR_IMGS[cat],"feats":CAR_FEATS[cat]})
    return results

# ── Inline klaviatura ─────────────────────────────────────────────────────────
def kb_roundtrip():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("Bir tomonga",callback_data="rt:no"),
           InlineKeyboardButton("Borib-qaytish",callback_data="rt:yes"))
    return kb

def kb_hotel(city):
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton(f"Ha, {city} da mehmonhona",callback_data="hotel:yes"),
           InlineKeyboardButton("Yoq, rahmat",callback_data="hotel:no"))
    return kb

def kb_nights():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("1 kecha",callback_data="nights:1"),
           InlineKeyboardButton("3 kecha",callback_data="nights:3"),
           InlineKeyboardButton("5 kecha",callback_data="nights:5"),
           InlineKeyboardButton("7 kecha",callback_data="nights:7"))
    kb.row(InlineKeyboardButton("10 kecha",callback_data="nights:10"),
           InlineKeyboardButton("14 kecha",callback_data="nights:14"))
    return kb

def kb_car(city):
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton(f"Ha, {city} da mashina",callback_data="car:yes"),
           InlineKeyboardButton("Yoq, rahmat",callback_data="car:no"))
    return kb

def kb_cardays():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("1 kun",callback_data="cardays:1"),
           InlineKeyboardButton("3 kun",callback_data="cardays:3"),
           InlineKeyboardButton("5 kun",callback_data="cardays:5"),
           InlineKeyboardButton("7 kun",callback_data="cardays:7"))
    kb.row(InlineKeyboardButton("10 kun",callback_data="cardays:10"),
           InlineKeyboardButton("14 kun",callback_data="cardays:14"))
    return kb

# ── Natija ko'rsatish ─────────────────────────────────────────────────────────
def show_flights(cid, sess):
    d = sess["d"]
    flights = get_flights(d["origin"],d["destination"],d["date"],d["adults"],d.get("retDate"))
    tur = "Borib-qaytish" if d.get("retDate") else "Bir tomon"
    ret = f" / {d['retDate']}" if d.get("retDate") else ""
    out = f"*{d['originName']} -- {d['destinationName']}*\n"
    out += f"Sana: {d['date']}{ret} | {tur} | {d['adults']} yolovchi\n"
    out += "=" * 32 + "\n"
    for i,f in enumerate(flights,1):
        stxt = "Togri parvoz" if f["stops"]==0 else "1 toxtash"
        jtxt = f"Qoldi: {f['seats']}" if f["seats"]<=5 else f"Joy: {f['seats']}"
        out += f"\n[{i}] *{f['airline']}*  {f['fnum']}\n"
        out += f"Uchish: {f['dep']}  Qonish: {f['arr']}  ({f['dur']})\n"
        out += f"{stxt}  |  {jtxt}\n"
        out += f"Narx: *${f['price']} USD*\n"
        out += "-" * 32
    out += "\n\nYangi parvoz: /search"
    bot.send_message(cid, out)
    city = AN.get(d["destination"], d["destination"])
    bot.send_message(cid, f"{city} da mehmonhona qidirmoqchimisiz?", reply_markup=kb_hotel(city))
    sess["step"] = "hotel_q"

def show_hotels(cid, sess):
    d = sess["d"]
    dest = d["destination"]
    nights = d["hotelNights"]
    city = AN.get(dest, dest)
    bot.send_message(cid, "Mehmonhonalar qidirilmoqda...")
    hotels = get_hotels(dest, nights, d["adults"])
    bot.send_message(cid, f"*{city} mehmonhonalari*\nKirish: {d['date']} | {nights} kecha | {d['adults']} mehmon\n" + "="*32)
    for h in hotels:
        cap = f"{h['emoji']} *{h['name']}*\n"
        cap += f"Joylashuv: {h['addr']}\n"
        cap += f"Narx: *${h['price']}/kecha*  x{nights} = ${h['total']}\n"
        cap += f"Baho: {h['rating']}/10\n{h['amen']}"
        try:
            bot.send_photo(cid, h["img"], caption=cap)
        except:
            bot.send_message(cid, cap)
    city = AN.get(dest, dest)
    bot.send_message(cid, f"{city} da mashina ijaralamoqchimisiz?", reply_markup=kb_car(city))
    sess["step"] = "car_q"

def show_cars(cid, sess):
    d = sess["d"]
    dest = d["destination"]
    days = d["carDays"]
    city = AN.get(dest, dest)
    bot.send_message(cid, "Mashinalar qidirilmoqda...")
    cars = get_cars(dest, days)
    bot.send_message(cid, f"*{city} - Mashina ijarasi*\nMuddat: {days} kun\n" + "="*32)
    for c in cars:
        cap = f"*{c['cat']}: {c['model']}*\n"
        cap += f"Narx: *${c['price']}/kun*  x{days} kun = ${c['total']}\n"
        cap += c["feats"]
        try:
            bot.send_photo(cid, c["img"], caption=cap)
        except:
            bot.send_message(cid, cap)
    bot.send_message(cid, "Yangi qidiruv: /search")
    sess["step"] = "idle"
    sess["d"] = {}

# ── Xabar handlerlari ─────────────────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    sess = gs(msg.chat.id)
    sess["step"] = "idle"; sess["d"] = {}
    t = "sarvaravia\_bot \- Aviaparvoz \+ Mehmonhona \+ Mashina ijarasi\n\n"
    t += "/search \- Qidirishni boshlash\n"
    t += "/help \- Yordam\n\n"
    t += "Format: *Shahar1 Shahar2 Sana*\n"
    t += "Misol: Toshkent Dubai 2026\.10\.06"
    bot.send_message(msg.chat.id, t, parse_mode="MarkdownV2")

@bot.message_handler(commands=["help"])
def cmd_help(msg):
    t = "*Qidiruv formati:*\n\n"
    t += "Shahar1 Shahar2 Sana \[Yolovchi\]\n\n"
    t += "Misol:\n"
    t += "  Toshkent Dubai 2026\.10\.06\n"
    t += "  TAS DXB 2026\-10\-06 2\n\n"
    t += "Qidiruv natijasida mehmonhona va mashina ham taklif etiladi\."
    bot.send_message(msg.chat.id, t, parse_mode="MarkdownV2")

@bot.message_handler(commands=["search"])
def cmd_search(msg):
    sess = gs(msg.chat.id)
    sess["step"] = "query"; sess["d"] = {}
    t = "Marshrut va sanani kiriting:\n\n"
    t += "*Shahar1 Shahar2 Sana*\n\n"
    t += "Misol:\n"
    t += "  Toshkent Dubai 2026.10.06\n"
    t += "  TAS DXB 2026-10-06 2"
    bot.send_message(msg.chat.id, t)

@bot.message_handler(commands=["cancel"])
def cmd_cancel(msg):
    sess = gs(msg.chat.id)
    sess["step"] = "idle"; sess["d"] = {}
    bot.send_message(msg.chat.id, "Bekor qilindi. /search \- yangi qidiruv.")

@bot.message_handler(func=lambda m: True)
def handle_text(msg):
    cid = msg.chat.id
    txt = msg.text.strip() if msg.text else ""
    sess = gs(cid)
    step = sess["step"]

    if step == "query":
        parts = txt.split()
        if len(parts) < 3:
            bot.send_message(cid, "Kamida 3 qism: Shahar1 Shahar2 Sana\nMisol: Toshkent Dubai 2026.10.06")
            return
        date_idx = -1
        import re
        for i, p in enumerate(parts):
            if re.match(r'^\d{4}[.\-/]\d{2}[.\-/]\d{2}$', p):
                date_idx = i; break
        if date_idx < 2:
            bot.send_message(cid, "Sana topilmadi. Format: YYYY.MM.DD\nMisol: Toshkent Dubai 2026.10.06")
            return
        origin_txt = parts[0]
        dest_txt   = parts[date_idx - 1]
        pax = 1
        if len(parts) > date_idx + 1:
            pv = parts[date_idx + 1]
            if pv.isdigit() and 1 <= int(pv) <= 9: pax = int(pv)
        date_str, date_obj = parse_date(parts[date_idx])
        if not date_str:
            bot.send_message(cid, "Notogri sana. Format: YYYY.MM.DD"); return
        if date_obj < date.today():
            bot.send_message(cid, "Utgan sana. Kelajakdagi sanani kiriting."); return
        from_iata = get_iata(origin_txt)
        to_iata   = get_iata(dest_txt)
        if not from_iata:
            bot.send_message(cid, f"Birinchi shahar topilmadi: {origin_txt}"); return
        if not to_iata:
            bot.send_message(cid, f"Ikkinchi shahar topilmadi: {dest_txt}"); return
        if from_iata == to_iata:
            bot.send_message(cid, "Ketish va kelish shahri bir xil bolmasin."); return
        sess["d"] = {
            "origin":from_iata,"originName":get_name(from_iata),
            "destination":to_iata,"destinationName":get_name(to_iata),
            "date":date_str,"adults":pax,"retDate":None,
        }
        sess["step"] = "roundtrip"
        c  = f"{sess['d']['originName']} -> {sess['d']['destinationName']}\n"
        c += f"Sana: {date_str} | {pax} yolovchi\n\nQaysi tur?"
        bot.send_message(cid, c, reply_markup=kb_roundtrip())

    elif step == "retdate":
        date_str, date_obj = parse_date(txt)
        if not date_str:
            bot.send_message(cid, "Notogri sana. Format: YYYY.MM.DD"); return
        d0_str, d0_obj = parse_date(sess["d"]["date"])
        if date_obj <= d0_obj:
            bot.send_message(cid, "Qaytish sanasi ketish sanasidan keyin bolishi kerak."); return
        sess["d"]["retDate"] = date_str
        bot.send_message(cid, "Qidirilmoqda...")
        show_flights(cid, sess)

    elif step == "hotel_nights":
        if txt.isdigit() and 1 <= int(txt) <= 30:
            sess["d"]["hotelNights"] = int(txt)
            bot.send_message(cid, "Mehmonhonalar qidirilmoqda...")
            show_hotels(cid, sess)
        else:
            bot.send_message(cid, "1 dan 30 gacha son kiriting (masalan: 5)")

    elif step == "car_days":
        if txt.isdigit() and 1 <= int(txt) <= 30:
            sess["d"]["carDays"] = int(txt)
            bot.send_message(cid, "Mashinalar qidirilmoqda...")
            show_cars(cid, sess)
        else:
            bot.send_message(cid, "1 dan 30 gacha son kiriting (masalan: 3)")

    else:
        bot.send_message(cid, "Parvoz qidirish uchun /search yozing.")

# ── Callback handlerlari ──────────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call):
    cid  = call.message.chat.id
    mid  = call.message.message_id
    data = call.data
    sess = gs(cid)
    bot.answer_callback_query(call.id)

    if data.startswith("rt:"):
        choice = data[3:]
        if choice == "yes":
            sess["step"] = "retdate"
            bot.edit_message_text("Qaytish sanasini kiriting:\nFormat: YYYY.MM.DD\nMisol: 2026.11.06", cid, mid)
        else:
            sess["d"]["retDate"] = None
            bot.edit_message_text("Qidirilmoqda...", cid, mid)
            show_flights(cid, sess)

    elif data.startswith("hotel:"):
        choice = data[6:]
        if choice == "no":
            city = AN.get(sess["d"].get("destination",""), "")
            bot.edit_message_text("Xop!", cid, mid)
            bot.send_message(cid, f"{city} da mashina ijaralamoqchimisiz?", reply_markup=kb_car(city))
            sess["step"] = "car_q"
        else:
            sess["step"] = "hotel_nights"
            city = AN.get(sess["d"].get("destination",""), "")
            bot.edit_message_text(f"{city} da necha kecha? Tugma bosing yoki raqam yozing (1-30):", cid, mid)
            bot.send_message(cid, "Kechalar sonini tanlang:", reply_markup=kb_nights())

    elif data.startswith("nights:"):
        nights = int(data[7:])
        sess["d"]["hotelNights"] = nights
        bot.edit_message_text("Mehmonhonalar qidirilmoqda...", cid, mid)
        show_hotels(cid, sess)

    elif data.startswith("car:"):
        choice = data[4:]
        if choice == "no":
            sess["step"] = "idle"; sess["d"] = {}
            bot.edit_message_text("Xop! Yangi qidiruv: /search", cid, mid)
        else:
            sess["step"] = "car_days"
            city = AN.get(sess["d"].get("destination",""), "")
            bot.edit_message_text(f"{city} da necha kun mashina kerak? Tugma bosing yoki raqam yozing (1-30):", cid, mid)
            bot.send_message(cid, "Ijara muddatini tanlang:", reply_markup=kb_cardays())

    elif data.startswith("cardays:"):
        days = int(data[8:])
        sess["d"]["carDays"] = days
        bot.edit_message_text("Mashinalar qidirilmoqda...", cid, mid)
        show_cars(cid, sess)

# ── Ishga tushirish ───────────────────────────────────────────────────────────
from flask import Flask, request as freq
import os

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    import json
    update = telebot.types.Update.de_json(freq.get_data().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def health():
    return 'sarvaravia_bot ishlayapti!', 200

if __name__ == "__main__":
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')
    if WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f'{WEBHOOK_URL}/{TOKEN}')
        print(f"Webhook: {WEBHOOK_URL}/{TOKEN}")
        port = int(os.environ.get('PORT', 10000))
        app.run(host='0.0.0.0', port=port)
    else:
        print("sarvaravia_bot ishga tushdi (polling)...")
        bot.infinity_polling()
