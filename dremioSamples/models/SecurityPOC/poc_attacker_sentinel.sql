{#
  SECURITY_POC — see README.md and SECURITY_POC_ANALYSIS.md in dremioSamples/
  Attacker-authored MODEL file. The victim's `dbt run` (per official docs flow)
  creates this persistent VIEW inside the victim's own Dremio space using the
  victim's PAT. The Jinja below is rendered by dbt on the victim's machine:
    - target.user     = the username item from profiles.yml the docs told them to create
    - target.dremio_space = the Dremio space from the same profile block
    - run_started_at  = timestamp of the victim's run
  All columns are benign. Nothing destructive ships in this repo.
#}
select
  'SECURITY_POC nvk0x: ATTACKER-AUTHORED model executed by victim dbt run (official docs flow)'   as evidence_type,
  'github.com/dremio-brock/DremioDBTSample — unclaimed/claimable 2023-11-16 until 2024-12-06'      as takeover_reference,
  'https://docs.getdbt.com/guides/build-dremio-lakehouse'                                          as official_docs_source,
  '{{ (target.user | default("profile-user-not-exposed") | string | replace("'", "")) }}'          as executed_as_profile_user,
  '{{ (target.dremio_space | default("profile-space-not-exposed") | string | replace("'", "")) }}' as victim_dremio_space,
  '{{ run_started_at }}'                                                                           as executed_at_parse_time,
  'the same position can execute unrestricted attacker SQL — see README capability note'            as capability_note
