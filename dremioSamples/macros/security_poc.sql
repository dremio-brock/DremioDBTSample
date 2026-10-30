{#
  SECURITY_POC marker macro — dremio-brock/DremioDBTSample
  Repo installed via the OFFICIAL dbt docs guide:
    https://docs.getdbt.com/guides/build-dremio-lakehouse ("Getting started", step 1)
  All statements below are benign reads. Nothing destructive ships in this repo.
  Researcher: @nvk0x — coordinated disclosure to dbt Labs.
#}
{% macro security_poc_hook(phase) %}

    {% do log(
        "SECURITY_POC nvk0x: the ATTACKER-AUTHORED macro (macros/security_poc.sql) executing "
        ~ phase ~ " hook inside the VICTIM'S dbt project (cloned per official docs instructions). "
        ~ "profile user=" ~ (target.user | default('not-exposed')) ~ " "
        ~ "parse-time=" ~ run_started_at ~ " "
        ~ "docs-source=https://docs.getdbt.com/guides/build-dremio-lakehouse",
        info=True
    ) %}

    {% do log(
        "SECURITY_POC nvk0x: the hook SQL below is ATTACKER-CHOSEN — it executes against the "
        ~ "victim's Dremio project using the victim's PAT (profile 'dremioSamples', 'cloud_dev'). "
        ~ "In a real attack this statement would be arbitrary attacker SQL, not this benign marker.",
        info=True
    ) %}

    {% if phase == 'on-run-start' %}
        {% do return("SELECT 'SECURITY_POC_on-run-start_ATTACKER_CHOSEN_SQL' AS security_poc_marker") %}
    {% else %}
        {% do return("SELECT 'SECURITY_POC_on-run-end_ATTACKER_CHOSEN_SQL' AS security_poc_marker") %}
    {% endif %}

{% endmacro %}
