# data-cleaning-pipeline — Month 3

Clean, validated pipeline for dummy Texas permits using Pydantic and Supabase. Handles messy county, trade, contractor and blocks invalid records that static inserts can't.

Target: 15 dummy raw Texas permits with dirty extra spaces, wrong casing, empty contractor, negative value, invalid permit number — not real TDLR, test data for validation logic.

Features:

Validates permit number format, trade, value, required fields
Blocks extra fields not defined and auto-trims spaces
Cleans messy county, trade, contractor with strip and title case
Separates valid and invalid records with clear error handling
Converts clean data for Supabase storage
Supabase TRUNCATE + INSERT + COUNT + GROUP BY + ORDER BY Top3
Handles 12 valid 3 invalid — empty, negative, invalid format blocked

Installation: pip install -r requirements.txt

Usage: python pipeline.py

Output: Supabase texas_permits — COUNT 12, GROUP BY Harris 3 Travis 3 Dallas 3 Bexar 1 Tarrant 2, Top3 220k 200k 185k — dummy data test

Stack: Python, Pydantic V2, Supabase PostgreSQL Tokyo ap-northeast-1, psycopg2

License: MIT
