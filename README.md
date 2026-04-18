# Dynamic VPN everyday

A Google App Engine service that scrapes [VPN Gate](https://www.vpngate.net) for OpenVPN configs, filters them by country/bandwidth/session criteria, and emails the results as a `.zip` attachment twice daily.

## How it works

| Step | What happens |
|------|-------------|
| **Scrape** | Submits the VPN Gate filter form and parses the server table, filtering by country, minimum bandwidth, and minimum session count |
| **Download** | Concurrently fetches `.ovpn` config files and patches them with a `data-ciphers` directive for OpenVPN 2.5+ compatibility |
| **Email** | Zips all configs and sends them via SMTP to a BCC list, with an L2TP server summary table in the email body |

## Configuration

All runtime settings (target URL, country list, SMTP credentials, recipient list, etc.) live in **Google Cloud Firestore**. The only required environment variable is `GOOGLE_CLOUD_PROJECT`.

| Firestore collection | Contents |
|----------------------|----------|
| `parameter/param_1` | URL, bandwidth threshold, session threshold, protocols, timeouts, SMTP credentials, access key |
| `country` | Active country filter codes (`code_2`) |
| `mail` | Active recipient email addresses |

## Running the job

**Automatic** — App Engine cron fires `/process` at 01:00 and 13:00 (Asia/Shanghai) as configured in `cron.yaml`.

**HTTP trigger**

```
GET /process?access_key=<key>
```

**Locally**

```bash
GOOGLE_CLOUD_PROJECT=<project> uv run python -m cmd.run_now [email@example.com ...]
```

## Development

```bash
uv sync --all-groups          # install dependencies

uv run pytest -m "not integration"   # unit tests (no external services)
uv run pytest -m integration         # integration tests (requires Firestore access)

uv run ruff check .           # lint
uv run ruff format .          # format
```