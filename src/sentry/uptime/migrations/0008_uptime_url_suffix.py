# Generated by Django 5.0.8 on 2024-08-16 22:25

from django.db import migrations, models

from sentry.new_migrations.migrations import CheckedMigration


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production.
    # This should only be used for operations where it's safe to run the migration after your
    # code has deployed. So this should not be used for most operations that alter the schema
    # of a table.
    # Here are some things that make sense to mark as post deployment:
    # - Large data migrations. Typically we want these to be run manually so that they can be
    #   monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   run this outside deployments so that we don't block them. Note that while adding an index
    #   is a schema change, it's completely safe to run the operation after the code has deployed.
    # Once deployed, run these manually via: https://develop.sentry.dev/database-migrations/#migration-deployment

    is_post_deployment = False

    dependencies = [
        ("uptime", "0007_update_detected_subscription_interval"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    """
                    ALTER TABLE "uptime_uptimesubscription" ADD COLUMN "url_domain" character varying(255) NOT NULL DEFAULT '';
                    """,
                    reverse_sql="""
                ALTER TABLE "uptime_uptimesubscription" DROP COLUMN "url_domain";
                """,
                    hints={"tables": ["uptime_uptimesubscription"]},
                ),
                migrations.RunSQL(
                    """
                    ALTER TABLE "uptime_uptimesubscription" ADD COLUMN "url_domain_suffix" character varying(255) NOT NULL DEFAULT '';
                    """,
                    reverse_sql="""
                ALTER TABLE "uptime_uptimesubscription" DROP COLUMN "url_domain_suffix";
                """,
                    hints={"tables": ["uptime_uptimesubscription"]},
                ),
                migrations.RunSQL(
                    """
                    ALTER TABLE "uptime_uptimesubscription" ADD COLUMN "host_whois_orgname" character varying(255) NOT NULL DEFAULT '';
                    """,
                    reverse_sql="""
                ALTER TABLE "uptime_uptimesubscription" DROP COLUMN "host_whois_orgname";
                """,
                    hints={"tables": ["uptime_uptimesubscription"]},
                ),
                migrations.RunSQL(
                    """
                    ALTER TABLE "uptime_uptimesubscription" ADD COLUMN "host_whois_orgid" character varying(255) NOT NULL DEFAULT '';
                    """,
                    reverse_sql="""
                ALTER TABLE "uptime_uptimesubscription" DROP COLUMN "host_whois_orgid";
                """,
                    hints={"tables": ["uptime_uptimesubscription"]},
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="uptimesubscription",
                    name="url_domain",
                    field=models.CharField(db_index=True, default="", max_length=255),
                ),
                migrations.AddField(
                    model_name="uptimesubscription",
                    name="url_domain_suffix",
                    field=models.CharField(db_index=True, default="", max_length=255),
                ),
                migrations.AddField(
                    model_name="uptimesubscription",
                    name="host_whois_orgname",
                    field=models.CharField(db_index=True, default="", max_length=255),
                ),
                migrations.AddField(
                    model_name="uptimesubscription",
                    name="host_whois_orgid",
                    field=models.CharField(db_index=True, default="", max_length=255),
                ),
            ],
        )
    ]
