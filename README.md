# data-cleaning-pipeline — Month 3
Pydantic bouncer + Supabase pipeline for Texas permits. Cleans dirty county/trade/contractor before INSERT, dedupes by permit_number UNIQUE.

Target: TDLR Texas permits 15 raw dicts — tests cleaning of "  travis  ", "  hvac  ", "ELECTRICAL", empty "   ", -50000, BAD-025.

Features:

Pydantic BaseModel with Field pattern ^TDLR-\d{4}-\d{3}$, Literal Electrical/Plumbing/Hvac, gt>0, min_length 1
ConfigDict extra='forbid' str_strip_whitespace True
field_validator mode='before' strip().title() for county/trade/contractor
model_validate raw dict -> valid_list + ValidationError handling
model_dump model -> dict for Supabase INSERT into contractor_name
Supabase TRUNCATE + INSERT + COUNT + GROUP BY + ORDER BY Top3
Handles 12 valid 3 invalid with proper error types string_pattern_mismatch, greater_than, string_too_short, literal_error

Installation: pip install -r requirements.txt

Usage: python pipeline.py

Output: Supabase texas_permits COUNT 12, GROUP BY Harris 3 Travis 3 Dallas 3 Bexar 1 Tarrant 2, Top3 Harris Electrical 220k 150k 130k

Stack: Python, Pydantic V2, Supabase PostgreSQL Tokyo ap-northeast-1, psycopg2

License: MIT