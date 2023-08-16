Welcome to your new dbt project!

### Using the sample project for Dremio 
This project will help build a Dremio Sample Dremio semantic layer that can be deployed to multiple enviormnets quickly


### Setup Dremio
- Add dremio samples source
- Promote Samples."samples.dremio.com"."NYC-weather.csv" as csv with a header
- Promote Samples."samples.dremio.com"."Dremio University"."sample_data" as parquet

### Setup DBT
pip install dbt-dremio

Follow the prompt to configure your dremio profiles.yml


Try running the following commands:
- dbt run
- dbt test


### Extra
Modify your profile to include multiple environments

```
dremioSamples:
  outputs:
    dev:
      dremio_space: dev
      dremio_space_folder: no_schema
      object_storage_path: dev
      object_storage_source: $scratch
      password: dremio123
      port: 9047
      software_host: localhost
      threads: 1
      type: dremio
      use_ssl: false
      user: dremio
    test:
      dremio_space: test
      dremio_space_folder: no_schema
      object_storage_path: test
      object_storage_source: $scratch
      password: dremio123
      port: 9047
      software_host: localhost
      threads: 1
      type: dremio
      use_ssl: false
      user: dremio
    prod:
      dremio_space: prod
      dremio_space_folder: no_schema
      object_storage_path: prod
      object_storage_source: $scratch
      password: dremio123
      port: 9047
      software_host: localhost
      threads: 1
      type: dremio
      use_ssl: false
      user: dremio
  target: dev
```

- dbt run --target test
- dbt run --target prod


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


### Known Bugs:
schema cannot contain dots or spaces. To work around this, follow the instructions in this issue thread: https://github.com/dremio/dbt-dremio/issues/203
