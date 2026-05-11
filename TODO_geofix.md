# AINTA Fixes: GeoIP DB & Streamlit Warning

## Status
- [x] DATA directory ready
- [ ] Fix Streamlit warning
- [ ] Download GeoIP DB (manual)
- [ ] Test system

## Step 1: DATA Dir
DATA exists.

## Step 2: Fix DataFrame Warning
Editing dashboard.py to astype(object) columns.

## Step 3: GeoIP DB Download (REQUIRED for maps)
1. Free account: https://www.maxmind.com/en/geolite2/signup
2. License Key from https://account.maxmind.com/
3. PowerShell (run as admin if needed):
```
cd DATA
$key = 'YOUR_LICENSE_KEY'
Invoke-WebRequest -Uri \"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=$key&suffix=tar.gz\" -OutFile geolite2.tar.gz
tar -xzf geolite2.tar.gz --strip-components=1
Move-Item 'GeoLite2-City.mmdb' .
Remove-Item geolite2.tar.gz, GeoLite2-City_*
```
Or browser: Generate download link, extract GeoLite2-City.mmdb to DATA/.

## Step 4: Test
```
python run_system.py
```
Expect: No GeoIP errors, maps show locations, no DF warnings.

## Step 5: Update TODO ✅ all, delete this file.

Updated: $(date)
