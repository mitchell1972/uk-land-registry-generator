"""
Sample data for generating realistic test cases.
"""

# Sample addresses for UK properties
SAMPLE_ADDRESSES = [
    "42 Acacia Avenue, London, EC1A 1BB",
    "15 Windsor Road, Manchester, M1 5RD",
    "7 Royal Crescent, Bath, BA1 2LR",
    "29 Castle Street, Edinburgh, EH1 2ND",
    "8 Harbour View, Cardiff, CF10 4PA",
    "63 The Greenway, Birmingham, B4 7QE",
    "12 Victoria Terrace, Bristol, BS8 4NP",
    "5 Market Square, Oxford, OX1 3HA",
    "22 College Lane, Cambridge, CB2 1TN",
    "37 Riverside Walk, Norwich, NR1 1QE",
    "9 Meadow View, Leeds, LS1 4DB",
    "18 High Street, York, YO1 8QP",
    "77 Seafront Parade, Brighton, BN1 2LH",
    "3 Castle Hill, Newcastle, NE1 5SG",
    "25 The Promenade, Cheltenham, GL50 1NN"
]

# Sample individual names
SAMPLE_NAMES = [
    "John Smith", "Sarah Johnson", "Mohammed Khan", 
    "Emily Williams", "David Brown", "Jessica Taylor",
    "Michael Davies", "Emma Wilson", "James Anderson",
    "Olivia Thomas", "Robert Evans", "Sophia Harris",
    "William Lewis", "Isla Clark", "Benjamin Walker",
    "Charlotte Robinson", "Thomas Wright", "Amelia Hall",
    "Daniel Green", "Grace Young"
]

# Sample company names
SAMPLE_COMPANIES = [
    "Acme Properties Ltd", "Horizon Developments plc",
    "Oakwood Estates Limited", "City Centre Investments Ltd",
    "Heritage Homes Limited", "Waterfront Development Co.",
    "Metropolitan Land Holdings", "Rural Property Trust",
    "Redstone Property Investments", "Bluesky Developments Ltd",
    "Cornerstone Estates", "Urban Renewal Group plc",
    "County Land Holdings", "Premier Properties Ltd",
    "Landmark Development Corporation"
]

# Sample mortgage lenders
SAMPLE_LENDERS = [
    "HSBC Bank", "Barclays", "Lloyds Banking Group", 
    "Nationwide Building Society", "NatWest Group",
    "Santander UK", "Virgin Money", "Royal Bank of Scotland",
    "Halifax", "Yorkshire Building Society",
    "Coventry Building Society", "Metro Bank",
    "TSB Bank", "Bank of Ireland UK", "Skipton Building Society"
]

# Sample application statuses with their relative weights
APPLICATION_STATUSES = {
    "Pending": 0.3,
    "Processing": 0.3, 
    "Completed": 0.2, 
    "Rejected": 0.1, 
    "Awaiting Further Information": 0.1
}

# Sample reasons for title corrections
CORRECTION_REASONS = [
    "Address error", 
    "Name misspelling", 
    "Incorrect boundary", 
    "Missing easement", 
    "Incorrect tenure type",
    "Incorrect plan reference",
    "Clerical error in register",
    "Missing restrictive covenant",
    "Incorrect property extent",
    "Duplicate registration"
] 