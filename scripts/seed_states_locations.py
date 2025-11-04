"""
Seed script to populate states and sample locations
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.models import Base, State, Location, Tenant
from app.models.location import FacilityType, ActType


def seed_states(db: Session):
    """Seed Indian states"""
    states_data = [
        {"name": "Andhra Pradesh", "code": "AP"},
        {"name": "Telangana", "code": "TG"},
        {"name": "Karnataka", "code": "KA"},
        {"name": "Tamil Nadu", "code": "TN"},
        {"name": "Maharashtra", "code": "MH"},
        {"name": "Delhi", "code": "DL"},
        {"name": "Haryana", "code": "HR"},
        {"name": "Punjab", "code": "PB"},
        {"name": "Odisha", "code": "OD"},
        {"name": "West Bengal", "code": "WB"},
        {"name": "Gujarat", "code": "GJ"},
        {"name": "Rajasthan", "code": "RJ"},
        {"name": "Uttar Pradesh", "code": "UP"},
        {"name": "Madhya Pradesh", "code": "MP"},
        {"name": "Kerala", "code": "KL"},
    ]

    print("Seeding states...")
    for state_data in states_data:
        # Check if state already exists
        existing = db.query(State).filter(State.code == state_data["code"]).first()
        if not existing:
            state = State(**state_data)
            db.add(state)
            print(f"  ✓ Added state: {state_data['name']} ({state_data['code']})")
        else:
            print(f"  - State already exists: {state_data['name']} ({state_data['code']})")

    db.commit()
    print(f"States seeding complete!\n")


def seed_sample_locations(db: Session):
    """Seed sample locations for demo tenant"""

    # Get demo tenant
    tenant = db.query(Tenant).filter(Tenant.name == "Demo Company").first()
    if not tenant:
        print("Demo tenant not found. Please run seed_data.py first.")
        return

    # Get states
    telangana = db.query(State).filter(State.code == "TG").first()
    karnataka = db.query(State).filter(State.code == "KA").first()
    maharashtra = db.query(State).filter(State.code == "MH").first()
    tamilnadu = db.query(State).filter(State.code == "TN").first()
    haryana = db.query(State).filter(State.code == "HR").first()

    if not all([telangana, karnataka, maharashtra, tamilnadu, haryana]):
        print("Required states not found. Please seed states first.")
        return

    locations_data = [
        {
            "name": "Hyderabad SEZ",
            "city": "Hyderabad",
            "state_id": telangana.id,
            "facility_type": FacilityType.SEZ,
            "act_type": ActType.CONTRACT_LABOUR,
            "address_line1": "Plot No. 123, Hi-Tech City",
            "address_line2": "Phase 2, HITEC City",
            "postal_code": "500081",
            "tenant_id": tenant.id,
        },
        {
            "name": "Hyderabad STP",
            "city": "Hyderabad",
            "state_id": telangana.id,
            "facility_type": FacilityType.STP,
            "act_type": ActType.SHOPS_ESTABLISHMENT,
            "address_line1": "Tower B, Cyber Towers",
            "address_line2": "Madhapur",
            "postal_code": "500081",
            "tenant_id": tenant.id,
        },
        {
            "name": "Bangalore SEZ",
            "city": "Bangalore",
            "state_id": karnataka.id,
            "facility_type": FacilityType.SEZ,
            "act_type": ActType.CONTRACT_LABOUR,
            "address_line1": "Electronic City",
            "address_line2": "Phase 1, Hosur Road",
            "postal_code": "560100",
            "tenant_id": tenant.id,
        },
        {
            "name": "Bangalore STP",
            "city": "Bangalore",
            "state_id": karnataka.id,
            "facility_type": FacilityType.STP,
            "act_type": ActType.SHOPS_ESTABLISHMENT,
            "address_line1": "Outer Ring Road",
            "address_line2": "Marathahalli",
            "postal_code": "560037",
            "tenant_id": tenant.id,
        },
        {
            "name": "Pune SEZ Unit-1",
            "city": "Pune",
            "state_id": maharashtra.id,
            "facility_type": FacilityType.SEZ,
            "act_type": ActType.CONTRACT_LABOUR,
            "address_line1": "Rajiv Gandhi Infotech Park",
            "address_line2": "Hinjewadi Phase 1",
            "postal_code": "411057",
            "tenant_id": tenant.id,
        },
        {
            "name": "Pune SEZ Unit-2",
            "city": "Pune",
            "state_id": maharashtra.id,
            "facility_type": FacilityType.SEZ,
            "act_type": ActType.FACTORIES,
            "address_line1": "Rajiv Gandhi Infotech Park",
            "address_line2": "Hinjewadi Phase 2",
            "postal_code": "411057",
            "tenant_id": tenant.id,
        },
        {
            "name": "Pune STP",
            "city": "Pune",
            "state_id": maharashtra.id,
            "facility_type": FacilityType.STP,
            "act_type": ActType.SHOPS_ESTABLISHMENT,
            "address_line1": "Magarpatta City",
            "address_line2": "Hadapsar",
            "postal_code": "411013",
            "tenant_id": tenant.id,
        },
        {
            "name": "Chennai Office",
            "city": "Chennai",
            "state_id": tamilnadu.id,
            "facility_type": FacilityType.REGULAR,
            "act_type": ActType.SHOPS_ESTABLISHMENT,
            "address_line1": "Tidel Park",
            "address_line2": "Taramani",
            "postal_code": "600113",
            "tenant_id": tenant.id,
        },
        {
            "name": "Gurgaon STP",
            "city": "Gurgaon",
            "state_id": haryana.id,
            "facility_type": FacilityType.STP,
            "act_type": ActType.SHOPS_ESTABLISHMENT,
            "address_line1": "DLF Cyber City",
            "address_line2": "Sector 25",
            "postal_code": "122002",
            "tenant_id": tenant.id,
        },
        {
            "name": "Mumbai Office",
            "city": "Mumbai",
            "state_id": maharashtra.id,
            "facility_type": FacilityType.REGULAR,
            "act_type": ActType.SHOPS_ESTABLISHMENT,
            "address_line1": "BKC Complex",
            "address_line2": "Bandra Kurla Complex",
            "postal_code": "400051",
            "tenant_id": tenant.id,
        },
    ]

    print("Seeding sample locations...")
    for loc_data in locations_data:
        # Check if location already exists
        existing = db.query(Location).filter(
            Location.name == loc_data["name"],
            Location.tenant_id == tenant.id
        ).first()

        if not existing:
            location = Location(**loc_data)
            db.add(location)
            print(f"  ✓ Added location: {loc_data['name']} - {loc_data['city']}")
        else:
            print(f"  - Location already exists: {loc_data['name']}")

    db.commit()
    print(f"Sample locations seeding complete!\n")


def main():
    """Main seeding function"""
    print("=" * 80)
    print("SEEDING STATES AND LOCATIONS")
    print("=" * 80)
    print()

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Create database session
    db = SessionLocal()

    try:
        # Seed states
        seed_states(db)

        # Seed sample locations
        seed_sample_locations(db)

        print("=" * 80)
        print("SEEDING COMPLETE!")
        print("=" * 80)
        print()
        print("Summary:")
        print(f"  Total States: {db.query(State).count()}")
        print(f"  Total Locations: {db.query(Location).count()}")
        print()

    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
