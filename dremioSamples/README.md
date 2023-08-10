Welcome to your new dbt project!

### Using the starter project for Dremio
pip install dbt-dremio

follow the prompt to configure your dremio instance

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


### Known Bugs:
schema cannot contain dots or spaces. To work around this modify the {python_home}/Lib/site-packages/dbt/adapters/dremio/relation.py change line 51 to:

<code> return '"' + identifier + '"' </code>

### To Do:
Add pre run script to prepare Dremio Sample Source.
1. add source
2. Format sources 
    1. <code>Sample."NYC-weather.csv"</code>
   2. <code>Sample."samples.dremio.com"."Dremio University".sample_data</code>