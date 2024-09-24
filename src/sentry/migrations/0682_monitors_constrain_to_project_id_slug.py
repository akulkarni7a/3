# Generated by Django 5.0.3 on 2024-03-27 20:02

from django.db import migrations, models

from sentry.new_migrations.migrations import CheckedMigration


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production. For
    # the most part, this should only be used for operations where it's safe to run the migration
    # after your code has deployed. So this should not be used for most operations that alter the
    # schema of a table.
    # Here are some things that make sense to mark as post deployment:
    # - Large data migrations. Typically we want these to be run manually by ops so that they can
    #   be monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   have ops run this and not block the deploy. Note that while adding an index is a schema
    #   change, it's completely safe to run the operation after the code has deployed.
    is_post_deployment = True

    dependencies = [
        ("sentry", "0681_unpickle_authenticator_again"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    [
                        'CREATE UNIQUE INDEX CONCURRENTLY "sentry_monitor_project_id_slug_1f4d3dc3_uniq" ON "sentry_monitor" ("project_id", "slug");',
                        'ALTER TABLE "sentry_monitor" ADD CONSTRAINT "sentry_monitor_project_id_slug_1f4d3dc3_uniq" UNIQUE USING INDEX "sentry_monitor_project_id_slug_1f4d3dc3_uniq";',
                        'CREATE INDEX CONCURRENTLY "sentry_moni_organiz_a62466_idx" ON "sentry_monitor" ("organization_id", "slug");',
                        'ALTER TABLE "sentry_monitor" DROP CONSTRAINT "sentry_monitor_organization_id_slug_c4ac3a42_uniq";',
                    ],
                    reverse_sql=[
                        'CREATE UNIQUE INDEX CONCURRENTLY "sentry_monitor_organization_id_slug_c4ac3a42_uniq" ON "sentry_monitor" ("organization_id", "slug");',
                        'ALTER TABLE "sentry_monitor" ADD CONSTRAINT "sentry_monitor_organization_id_slug_c4ac3a42_uniq" UNIQUE USING INDEX "sentry_monitor_organization_id_slug_c4ac3a42_uniq";',
                        'ALTER TABLE "sentry_monitor" DROP CONSTRAINT "sentry_monitor_project_id_slug_1f4d3dc3_uniq";',
                        'DROP INDEX CONCURRENTLY "sentry_moni_organiz_a62466_idx";',
                    ],
                    hints={"tables": ["sentry_monitor"]},
                ),
            ],
            state_operations=[
                migrations.AlterUniqueTogether(
                    name="monitor",
                    unique_together={("project_id", "slug")},
                ),
                migrations.AddIndex(
                    model_name="monitor",
                    index=models.Index(
                        fields=["organization_id", "slug"], name="sentry_moni_organiz_a62466_idx"
                    ),
                ),
            ],
        ),
    ]
