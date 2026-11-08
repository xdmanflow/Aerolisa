# Data sources

| Source | Content | Access | Terms | Committed? |
|---|---|---|---|---|
| NASA C-MAPSS | Simulated turbofan run-to-failure data (FD001–FD004) | NASA Prognostics Center of Excellence data repository; manual download into `data/raw/cmapss/` | Public NASA dataset | Only a tiny truncated slice in `sample_data/` |
| OpenSky Network REST API | Flights by aircraft, state vectors | OAuth2 client credentials (API client created on the OpenSky account page); daily credit limits | OpenSky terms of use (non-commercial research) | Never. Samples in `sample_data/` are synthetic |
| OpenSky aircraft database | icao24 → registration, typecode, operator, serial number | Download from OpenSky | OpenSky terms | Never |
| OurAirports | Airports, coordinates, codes | ourairports.com data downloads | Public domain | Tiny sample only |
| Eurocontrol performance data | Delays by airport and cause, punctuality | ansperformance.eu downloads | Eurocontrol terms | Never |
| Airbus orders & deliveries | Monthly public figures | airbus.com | Airbus site terms | Never |
| FAA AMT Handbooks (General, Airframe, Powerplant) | Maintenance knowledge for the copilot | faa.gov | US government works (public domain) | No (downloaded at runtime) |

## Checksums
Record SHA-256 of every manually downloaded file here at M0 so pipelines can verify inputs.

| File | SHA-256 |
|---|---|
| | |

## OpenSky usage rules for Aerolisa
- Respect each endpoint's maximum time window and the daily credit budget; the source module enforces a budget.
- Cache raw responses in `data/raw/opensky/`; never re-fetch a day already fetched.
- Never publish raw OpenSky data; publish only aggregates (cycles per day, counts) in the app and reports.
- Credentials: `credentials.json` or `OPENSKY_CLIENT_ID` / `OPENSKY_CLIENT_SECRET` in `.env`, both git-ignored.

## Simulation disclaimer (shown in the app)
Engines are NASA C-MAPSS simulations assigned to real airframes for demonstration. Their health has no relation to the real engines of those aircraft.
