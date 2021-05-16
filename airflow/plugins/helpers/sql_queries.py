class SqlQueries:
    target_organization_dimension_table_create = ("""
            CREATE TABLE IF NOT EXISTS public.dim_organization (
                organization_key varchar(50) NOT NULL,
                organization_name varchar(250) NOT NULL,
                created_at timestamp,
                PRIMARY KEY (organization_key)
            );
        """)

    staging_events_table_create = ("""
            CREATE TABLE IF NOT EXISTS public.staging_events (
                id varchar(50),
                event_type varchar(250),
                username  varchar(250),
                user_email varchar(250),
                user_type varchar(250),
                organization_name varchar(250),
                plan_name varchar(250),
                received_at timestamp
            );
        """)
