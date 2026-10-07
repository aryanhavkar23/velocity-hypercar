"""Idempotent seed data. Run manually with `python -m app.db.seed`."""
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db.database import Base, SessionLocal, engine
from app.models import (
    AeroPackage, Caliper, Car, Configuration, Engine, InteriorColor, InteriorMaterial,
    Paint, PerformancePackage, SeatType, Wheel,
)

CARS = [
    dict(
        name="GLC 300e",
        slug="glc-300e",
        base_price=8_700_000,
        horsepower=313,
        top_speed=218,
        acceleration=6.7,
        handling=70,
        braking=75,
        image_url="/assets/glc-300e.png",
        description="Luxury plug-in hybrid SUV pairing a 2.0L turbo combustion engine with electric drive for refined everyday efficiency and effortless agility.",
    ),
    dict(
        name="Porsche 911 GT3 RS",
        slug="porsche-911-gt3-rs",
        base_price=35_000_000,
        horsepower=525,
        top_speed=296,
        acceleration=3.2,
        handling=98,
        braking=97,
        image_url="/assets/porsche-911-gt3-rs.png",
        description="Uncompromising track-bred sports car with naturally aspirated flat-six power, central radiator concept, and extreme active aerodynamics.",
    ),
    dict(
        name="Lamborghini Huracán Tecnica",
        slug="lamborghini-huracan-tecnica",
        base_price=40_400_000,
        horsepower=640,
        top_speed=325,
        acceleration=3.2,
        handling=94,
        braking=95,
        image_url="/assets/lamborghini-huracan-tecnica.png",
        description="Rear-wheel drive masterpiece featuring a high-revving 5.2L naturally aspirated V10, rear-wheel steering, and track-tuned LDVI predictive dynamics.",
    ),
    dict(
        name="EQS 580",
        slug="eqs-580",
        base_price=16_200_000,
        horsepower=523,
        top_speed=210,
        acceleration=4.3,
        handling=76,
        braking=80,
        image_url="/assets/eqs-580.png",
        description="All-electric luxury flagship sedan with dual permanently synchronous electric motors, intelligent all-wheel drive, and whisper-quiet serenity.",
    ),
    dict(
        name="Ferrari 296 GTB",
        slug="ferrari-296-gtb",
        base_price=54_000_000,
        horsepower=830,
        top_speed=330,
        acceleration=2.9,
        handling=96,
        braking=96,
        image_url="/assets/ferrari-296-gtb.png",
        description="Definitive mid-rear hybrid berlinetta combining a 120-degree twin-turbo V6 with plug-in electric motor for breathtaking responsiveness.",
    ),
    dict(
        name="Mazda 3",
        slug="mazda-3",
        base_price=2_800_000,
        horsepower=186,
        top_speed=216,
        acceleration=7.9,
        handling=74,
        braking=72,
        image_url="/assets/mazda-3.png",
        description="Elegantly sculpted premium compact vehicle emphasizing Jinba Ittai harmony, intuitive G-Vectoring chassis dynamics, and human-centric craftsmanship.",
    ),
]

PAINTS = [
    dict(name="Obsidian Black", hex_code="#080808", price_modifier=0, category="solid"),
    dict(name="Pearl White", hex_code="#F5F5F0", price_modifier=150_000, category="pearl"),
    dict(name="Racing Red", hex_code="#C8102E", price_modifier=200_000, category="metallic"),
    dict(name="Electric Blue", hex_code="#0A5CFF", price_modifier=250_000, category="metallic"),
    dict(name="Neon Green", hex_code="#39FF14", price_modifier=300_000, category="special"),
]

WHEELS = [
    dict(name="Aero", description="Closed-face aero wheels for reduced drag.", price_modifier=100_000),
    dict(name="Carbon", description="Lightweight full carbon-fibre wheels.", price_modifier=450_000),
    dict(name="Forged", description="Forged alloy wheels with a classic multi-spoke design.", price_modifier=300_000),
    dict(name="Performance", description="Track-focused wheels with a wide contact patch.", price_modifier=200_000),
]

CALIPERS = [
    dict(name="Red", hex_code="#D00000", price_modifier=25_000),
    dict(name="Yellow", hex_code="#FFD60A", price_modifier=25_000),
    dict(name="Blue", hex_code="#1E6FFF", price_modifier=25_000),
    dict(name="Black", hex_code="#111111", price_modifier=0),
]

MATERIALS = [
    dict(name="Leather", description="Hand-stitched premium leather.", price_modifier=200_000),
    dict(name="Alcantara", description="Grippy suede-like microfibre.", price_modifier=350_000),
    dict(name="Carbon", description="Exposed carbon-fibre with minimal trim.", price_modifier=600_000),
]

INTERIOR_COLORS = [
    dict(name="Black", hex_code="#101010", price_modifier=0),
    dict(name="White", hex_code="#F2F2F2", price_modifier=0),
    dict(name="Red", hex_code="#B3122B", price_modifier=50_000),
    dict(name="Tan", hex_code="#B08968", price_modifier=50_000),
]

SEATS = [
    dict(name="Sport", description="Supportive everyday sport seats.", price_modifier=0),
    dict(name="Racing", description="Fixed-back carbon racing shells with harness points.", price_modifier=250_000),
    dict(name="Luxury", description="Heated, ventilated, massaging comfort seats.", price_modifier=400_000),
]

ENGINES = [
    # GLC 300e
    dict(car_slug="glc-300e", name="2.0L Turbo Plug-in Hybrid",
         description="Standard 313 hp PHEV powertrain pairing 2.0L inline-4 turbo with permanent electric motor.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="glc-300e", name="2.0L Turbo PHEV Performance Tune",
         description="Optimized hybrid torque map and boost calibration delivering 338 hp.",
         price_modifier=350_000, horsepower_modifier=25, top_speed_modifier=5,
         acceleration_modifier=-0.2, handling_modifier=0, braking_modifier=0),

    # Porsche 911 GT3 RS
    dict(car_slug="porsche-911-gt3-rs", name="4.0L Naturally Aspirated Flat-Six",
         description="High-revving atmospheric 4.0L six-cylinder boxer producing 525 hp at 9,000 RPM.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="porsche-911-gt3-rs", name="4.0L Flat-Six Weissach Power Spec",
         description="Lightweight titanium valvetrain and sport exhaust delivering 545 hp.",
         price_modifier=1_800_000, horsepower_modifier=20, top_speed_modifier=4,
         acceleration_modifier=-0.1, handling_modifier=1, braking_modifier=0),

    # Lamborghini Huracán Tecnica
    dict(car_slug="lamborghini-huracan-tecnica", name="5.2L Naturally Aspirated V10",
         description="Legendary 5.2L atmospheric V10 generating 640 hp with pure naturally aspirated sound.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="lamborghini-huracan-tecnica", name="5.2L V10 Corsa Exhaust & ECU Tune",
         description="Free-flow lightweight exhaust and aggressive engine management unleashing 665 hp.",
         price_modifier=2_200_000, horsepower_modifier=25, top_speed_modifier=5,
         acceleration_modifier=-0.1, handling_modifier=0, braking_modifier=0),

    # EQS 580
    dict(car_slug="eqs-580", name="Dual Permanently Synchronous Electric Motors",
         description="Dual electric motors delivering 523 hp and instantaneous all-wheel torque.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="eqs-580", name="Dual Electric Motors Acceleration Boost",
         description="High-output inverter calibration increasing power to 568 hp with quicker pedal response.",
         price_modifier=600_000, horsepower_modifier=45, top_speed_modifier=5,
         acceleration_modifier=-0.3, handling_modifier=0, braking_modifier=0),

    # Ferrari 296 GTB
    dict(car_slug="ferrari-296-gtb", name="3.0L Twin-Turbo V6 Plug-in Hybrid",
         description="Wide 120-degree twin-turbo 2.9L V6 with MGU-K electric motor delivering 830 hp.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="ferrari-296-gtb", name="3.0L V6 Hybrid Assetto Corsa Calibration",
         description="Race-derived turbo wastegate mapping and higher electric discharge yielding 860 hp.",
         price_modifier=2_800_000, horsepower_modifier=30, top_speed_modifier=5,
         acceleration_modifier=-0.1, handling_modifier=1, braking_modifier=0),

    # Mazda 3
    dict(car_slug="mazda-3", name="2.5L e-Skyactiv G",
         description="Naturally aspirated 2.5L 4-cylinder with cylinder deactivation and 186 hp.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="mazda-3", name="2.5L Skyactiv-G Turbo",
         description="Dynamic pressure turbocharger boosting output to 226 hp with generous low-rpm torque.",
         price_modifier=250_000, horsepower_modifier=40, top_speed_modifier=10,
         acceleration_modifier=-0.9, handling_modifier=0, braking_modifier=0),
]

PACKAGES = [
    # GLC 300e
    dict(car_slug="glc-300e", name="Standard Comfort Setup",
         description="Balanced air suspension and comfort road calibration.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="glc-300e", name="AMG Line Dynamic Package",
         description="Stiffened sports suspension, larger front brakes, and steering tuning.",
         price_modifier=450_000, horsepower_modifier=0, top_speed_modifier=2,
         acceleration_modifier=-0.1, handling_modifier=5, braking_modifier=5),

    # Porsche 911 GT3 RS
    dict(car_slug="porsche-911-gt3-rs", name="Clubsport Package",
         description="Track-ready road calibration with steel roll-cage prep.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="porsche-911-gt3-rs", name="Weissach Package",
         description="Carbon-weave anti-roll bars, magnesium suspension components, and track brakes.",
         price_modifier=3_500_000, horsepower_modifier=50, top_speed_modifier=5,
         acceleration_modifier=-0.1, handling_modifier=8, braking_modifier=8),

    # Lamborghini Huracán Tecnica
    dict(car_slug="lamborghini-huracan-tecnica", name="Strada Setup",
         description="Standard road configuration with adaptive magnetorheological damping.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="lamborghini-huracan-tecnica", name="Corsa Track Package",
         description="Firm track damping, race-spec brake cooling, and aggressive LDVI calibration.",
         price_modifier=2_500_000, horsepower_modifier=30, top_speed_modifier=4,
         acceleration_modifier=-0.1, handling_modifier=7, braking_modifier=7),

    # EQS 580
    dict(car_slug="eqs-580", name="Executive Luxury Line",
         description="Airmatic adaptive suspension with comfort-oriented tuning and acoustic glass.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="eqs-580", name="AMG Dynamic Plus Package",
         description="Dynamic air suspension calibration, sport rear-axle steering, and red brake calipers.",
         price_modifier=750_000, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=-0.1, handling_modifier=4, braking_modifier=4),

    # Ferrari 296 GTB
    dict(car_slug="ferrari-296-gtb", name="Standard GT Calibration",
         description="Standard road setup with electronic differential and side slip angle control.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="ferrari-296-gtb", name="Assetto Fiorano Package",
         description="Multimatic shock absorbers, extensive carbon-fiber weight reduction, and Michelin Cup 2R tires.",
         price_modifier=4_500_000, horsepower_modifier=35, top_speed_modifier=5,
         acceleration_modifier=-0.1, handling_modifier=9, braking_modifier=9),

    # Mazda 3
    dict(car_slug="mazda-3", name="Touring Standard Setup",
         description="Refined everyday road setup with Jinba Ittai chassis balance.",
         price_modifier=0, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=0.0, handling_modifier=0, braking_modifier=0),
    dict(car_slug="mazda-3", name="Sport Performance Package",
         description="Uprated front/rear dampers, stiffer stabilizer bar, and sport brake pads.",
         price_modifier=120_000, horsepower_modifier=0, top_speed_modifier=0,
         acceleration_modifier=-0.1, handling_modifier=4, braking_modifier=4),
]

AEROS = [
    # GLC 300e
    dict(car_slug="glc-300e", name="Standard Aerodynamics",
         description="Factory bodywork with optimized roof spoiler.",
         price_modifier=0, downforce=0, drag=0, handling_modifier=0, top_speed_modifier=0),
    dict(car_slug="glc-300e", name="Night Package Aero Styling",
         description="Gloss-black roof rails, front apron splitter, and rear diffuser fins.",
         price_modifier=150_000, downforce=10, drag=2, handling_modifier=3, top_speed_modifier=-1),

    # Porsche 911 GT3 RS
    dict(car_slug="porsche-911-gt3-rs", name="Standard GT3 RS Aero",
         description="Factory carbon swan-neck rear wing and front diffuser blades.",
         price_modifier=0, downforce=0, drag=0, handling_modifier=0, top_speed_modifier=0),
    dict(car_slug="porsche-911-gt3-rs", name="Active DRS Aero Package",
         description="Hydraulic Drag Reduction System (DRS) with active upper wing flap and underfloor diffuser flaps.",
         price_modifier=900_000, downforce=30, drag=10, handling_modifier=8, top_speed_modifier=-3),

    # Lamborghini Huracán Tecnica
    dict(car_slug="lamborghini-huracan-tecnica", name="Tecnica Fixed Wing",
         description="Factory rear wing and front Y-shaped air curtains.",
         price_modifier=0, downforce=0, drag=0, handling_modifier=0, top_speed_modifier=0),
    dict(car_slug="lamborghini-huracan-tecnica", name="High-Downforce Carbon Aero Kit",
         description="Aggressive carbon front splitter, rear wing extension, and rear underbody diffuser.",
         price_modifier=1_200_000, downforce=25, drag=8, handling_modifier=7, top_speed_modifier=-4),

    # EQS 580
    dict(car_slug="eqs-580", name="Streamline Aerodynamics",
         description="Ultra-slippery 0.20 Cd aerodynamic body contours with flush door handles.",
         price_modifier=0, downforce=0, drag=0, handling_modifier=0, top_speed_modifier=0),
    dict(car_slug="eqs-580", name="Aero Efficiency Deflector Kit",
         description="Optimized front wheel air curtains, flat underfloor paneling, and aero alloy inserts.",
         price_modifier=250_000, downforce=5, drag=-3, handling_modifier=2, top_speed_modifier=2),

    # Ferrari 296 GTB
    dict(car_slug="ferrari-296-gtb", name="Active Rear Spoiler",
         description="Integrated active rear spoiler deploying on high-downforce demand.",
         price_modifier=0, downforce=0, drag=0, handling_modifier=0, top_speed_modifier=0),
    dict(car_slug="ferrari-296-gtb", name="Assetto Fiorano High-Downforce Aero",
         description="Carbon front bumper appendages producing additional 25 kg of front downforce.",
         price_modifier=1_500_000, downforce=25, drag=8, handling_modifier=8, top_speed_modifier=-4),

    # Mazda 3
    dict(car_slug="mazda-3", name="Stock Bodywork",
         description="Clean Kodo design exterior with smooth airflow channels.",
         price_modifier=0, downforce=0, drag=0, handling_modifier=0, top_speed_modifier=0),
    dict(car_slug="mazda-3", name="Factory Sport Aero Kit",
         description="Discreet front air dam, side sill extensions, and gloss-black rear roof spoiler.",
         price_modifier=75_000, downforce=8, drag=2, handling_modifier=3, top_speed_modifier=-1),
]


def _ensure_schema(db: Session) -> None:
    """Ensure car_id column exists on option tables if running on an existing SQLite DB."""
    tables = [
        "paints", "wheels", "calipers", "interior_materials",
        "interior_colors", "seat_types", "engines", "performance_packages", "aero_packages",
    ]
    for table in tables:
        try:
            res = db.execute(text(f"PRAGMA table_info({table})")).fetchall()
            columns = [r[1] for r in res]
            if columns and "car_id" not in columns:
                db.execute(text(f"ALTER TABLE {table} ADD COLUMN car_id INTEGER REFERENCES cars(id)"))
                db.commit()
        except Exception:
            pass


def _cleanup_fictional_data(db: Session) -> None:
    """Safely remove or deactivate legacy fictional cars and options."""
    # Fictional cars
    for slug in ("vortex-x1", "apex-r", "phantom-gt"):
        old_car = db.scalar(select(Car).where(Car.slug == slug))
        if old_car:
            has_cfg = db.scalar(select(Configuration.id).where(Configuration.car_id == old_car.id))
            if has_cfg:
                old_car.is_active = False
            else:
                db.delete(old_car)

    # Legacy fictional options if unreferenced
    legacy_options = {
        Engine: ("V8", "V10", "V12", "Hybrid"),
        PerformancePackage: ("Street", "Track", "Race"),
        AeroPackage: ("Stock", "Sport", "Extreme"),
    }
    for model, names in legacy_options.items():
        fk = {
            Engine: Configuration.engine_id,
            PerformancePackage: Configuration.performance_package_id,
            AeroPackage: Configuration.aero_package_id,
        }[model]
        for opt in db.scalars(select(model).where(model.name.in_(names))).all():
            has_cfg = db.scalar(select(Configuration.id).where(fk == opt.id))
            if has_cfg:
                opt.is_active = False
            else:
                db.delete(opt)

    db.flush()


def _seed_table(db: Session, model, rows: list[dict], key: str = "name") -> int:
    existing = set(db.scalars(select(getattr(model, key))).all())
    created = 0
    for row in rows:
        if row[key] not in existing:
            db.add(model(**row))
            created += 1
    return created


def seed_database(db: Session) -> int:
    """Insert missing seed rows and link vehicle options. Safe to call repeatedly."""
    _ensure_schema(db)
    _cleanup_fictional_data(db)

    total = 0
    total += _seed_table(db, Car, CARS, key="slug")
    db.flush()

    car_slug_to_id = {c.slug: c.id for c in db.scalars(select(Car)).all()}

    def _prepare_rows(row_list: list[dict]) -> list[dict]:
        prepared = []
        for r in row_list:
            item = dict(r)
            if "car_slug" in item:
                slug = item.pop("car_slug")
                item["car_id"] = car_slug_to_id.get(slug)
            prepared.append(item)
        return prepared

    for model, rows in (
        (Paint, PAINTS),
        (Wheel, WHEELS),
        (Caliper, CALIPERS),
        (InteriorMaterial, MATERIALS),
        (InteriorColor, INTERIOR_COLORS),
        (SeatType, SEATS),
        (Engine, _prepare_rows(ENGINES)),
        (PerformancePackage, _prepare_rows(PACKAGES)),
        (AeroPackage, _prepare_rows(AEROS)),
    ):
        total += _seed_table(db, model, rows)

    db.commit()
    return total


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        print(f"Seeded {seed_database(session)} new rows.")
