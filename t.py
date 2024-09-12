text = """
  DWORD        bV5Size;
  LONG         bV5Width;
  LONG         bV5Height;
  WORD         bV5Planes;
  WORD         bV5BitCount;
  DWORD        bV5Compression;
  DWORD        bV5SizeImage;
  LONG         bV5XPelsPerMeter;
  LONG         bV5YPelsPerMeter;
  DWORD        bV5ClrUsed;
  DWORD        bV5ClrImportant;
  DWORD        bV5RedMask;
  DWORD        bV5GreenMask;
  DWORD        bV5BlueMask;
  DWORD        bV5AlphaMask;
  DWORD        bV5CSType;
  CIEXYZTRIPLE bV5Endpoints;
  DWORD        bV5GammaRed;
  DWORD        bV5GammaGreen;
  DWORD        bV5GammaBlue;
  DWORD        bV5Intent;
  DWORD        bV5ProfileData;
  DWORD        bV5ProfileSize;
  DWORD        bV5Reserved;
"""
lines = text.strip().splitlines()
result = {}

# Iterate over the lines and populate the dictionary
for line in lines:
    line = line.strip().replace(";", "")  # Remove semicolons and extra spaces
    dtype, name = line.split()            # Split into data type and variable name
    result[name] = dtype.lower()          # Add to dictionary, converting dtype to lowercase

# Custom print to match the desired format
print("map = {")
for i, (key, value) in enumerate(result.items()):
    comma = ',' if i < len(result) - 1 else ''
    print(f"    '{key}': '{value}'{comma}")
print("}")