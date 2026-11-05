from cleaner import TexasPermit
from pydantic import ValidationError
import psycopg2
CONNECTION_STRING = "postgresql://postgres.bguarcoalntqfijvzudp:Hassano53_Silent@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres?sslmode=require"

raw_permits = [
  {"permit_number": "TDLR-2026-011", "county": "Harris", "trade": "Electrical", "contractor": "Test Electric LLC", "issue_date": "2026-05-06", "value": 150000},
  {"permit_number": "TDLR-2026-012", "county": "Travis", "trade": "Plumbing", "contractor": "Austin Plumb Pros", "issue_date": "2026-05-06", "value": 80000},
  {"permit_number": "TDLR-2026-013", "county": "  travis  ", "trade": "  hvac  ", "contractor": "  cool air llc  ", "issue_date": "2026-05-07", "value": 90000},
  {"permit_number": "TDLR-2026-014", "county": "Dallas", "trade": "Electrical", "contractor": "Dallas Power Co", "issue_date": "2026-05-07", "value": 120000},
  {"permit_number": "TDLR-2026-015", "county": "Harris", "trade": "Electrical", "contractor": "Harris High Voltage", "issue_date": "2026-05-07", "value": 220000},
  {"permit_number": "TDLR-2026-016", "county": "Bexar", "trade": "Plumbing", "contractor": "Alamo Pipes", "issue_date": "2026-05-08", "value": 75000},
  {"permit_number": "TDLR-2026-017", "county": "Dallas", "trade": "ELECTRICAL", "contractor": "Power LLC", "issue_date": "2026-05-08", "value": 110000},
  {"permit_number": "TDLR-2026-018", "county": "Travis", "trade": "Electrical", "contractor": "Travis Electric", "issue_date": "2026-05-08", "value": 200000},
  {"permit_number": "TDLR-2026-019", "county": "Harris", "trade": "Electrical", "contractor": "   ", "issue_date": "2026-05-09", "value": 100000},
  {"permit_number": "TDLR-2026-020", "county": "Tarrant", "trade": "Electrical", "contractor": "Tarrant Electric", "issue_date": "2026-05-09", "value": 95000},
  {"permit_number": "TDLR-2026-021", "county": "Dallas", "trade": "Plumbing", "contractor": "Dallas Plumbing Pro", "issue_date": "2026-05-10", "value": 185000},
  {"permit_number": "TDLR-2026-022", "county": "Bexar", "trade": "Plumbing", "contractor": "Pipe Pros", "issue_date": "2026-05-10", "value": -50000},
  {"permit_number": "TDLR-2026-023", "county": "Harris", "trade": "Electrical", "contractor": "Harris Sparks", "issue_date": "2026-05-10", "value": 130000},
  {"permit_number": "TDLR-2026-024", "county": "Tarrant", "trade": "Hvac", "contractor": "Tarrant Cool", "issue_date": "2026-05-11", "value": 65000},
  {"permit_number": "BAD-025", "county": "Tarrant", "trade": "Electrical", "contractor": "Bad LLC", "issue_date": "2026-05-11", "value": 75000},
]

valid_list = []
invalid_count = 0
for raw in raw_permits:
    try:
        permit = TexasPermit.model_validate(raw)
        valid_list.append(permit)
    except ValidationError:
        invalid_count += 1

print("Pydantic:", len(valid_list), "valid", invalid_count, "invalid")

conn = psycopg2.connect(CONNECTION_STRING)
cur = conn.cursor()

cur.execute("TRUNCATE texas_permits;")
conn.commit()

for permit in valid_list:
    d = permit.model_dump()
    cur.execute(
        "INSERT INTO texas_permits (permit_number, trade, county, contractor_name, issue_date, value) VALUES (%s,%s,%s,%s,%s,%s)",
        (d['permit_number'], d['trade'], d['county'], d['contractor'], d['issue_date'], d['value'])
    )
conn.commit()

cur.execute("SELECT COUNT(*) FROM texas_permits;")
print("C1 COUNT:", cur.fetchone())
cur.execute("SELECT county, COUNT(*) FROM texas_permits GROUP BY county;")
print("C2 GROUP BY:", cur.fetchall())
cur.execute("SELECT permit_number, value FROM texas_permits WHERE county='Harris' AND trade='Electrical' ORDER BY value DESC LIMIT 3;")
print("C3 Top3 Harris Electrical:", cur.fetchall())

conn.close()