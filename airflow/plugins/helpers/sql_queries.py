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
                received_at timestamp,
                data_check_failed varchar(1)
            );
        """)

    target_organization_fact_table_create = ("""
                CREATE TABLE IF NOT EXISTS public.fact_organization (
                    id SERIAL,
                    organization_key varchar(50),
                    event_date date,
                    user_created_count integer,
                    user_updates_count integer,
                    user_deleted_count integer 
                );
            """)

    target_date_dimension_table_create = ("""
                CREATE TABLE IF NOT EXISTS public.dim_date (
                    date_dim_id SERIAL,
                    date_actual DATE NOT NULL,
                    epoch BIGINT NOT NULL,
                    day_suffix VARCHAR(4) NOT NULL,
                    day_name VARCHAR(9) NOT NULL,
                    day_of_week INT NOT NULL,
                    day_of_month INT NOT NULL,
                    day_of_quarter INT NOT NULL,
                    day_of_year INT NOT NULL,
                    week_of_month INT NOT NULL,
                    week_of_year INT NOT NULL,
                    week_of_year_iso VARCHAR(10) NOT NULL,
                    month_actual INT NOT NULL,
                    month_name VARCHAR(9) NOT NULL,
                    month_name_abbreviated VARCHAR(3) NOT NULL,
                    quarter_actual INT NOT NULL,
                    quarter_name VARCHAR(9) NOT NULL,
                    year_actual INT NOT NULL,
                    first_day_of_week DATE NOT NULL,
                    last_day_of_week DATE NOT NULL,
                    first_day_of_month DATE NOT NULL,
                    last_day_of_month DATE NOT NULL,
                    first_day_of_quarter DATE NOT NULL,
                    last_day_of_quarter DATE NOT NULL,
                    first_day_of_year DATE NOT NULL,
                    last_day_of_year DATE NOT NULL,
                    mmyyyy VARCHAR(6) NOT NULL,
                    mmddyyyy VARCHAR(10) NOT NULL,
                    weekend_indr BOOLEAN NOT NULL
                );
            """)

    target_user_dimension_table_create = ("""
                CREATE TABLE IF NOT EXISTS public.dim_user (
                    id SERIAL,
                    username varchar(250),
                    user_email varchar(250),
                    user_type varchar(250),
                    plan_name varchar(250),
                    created_at timestamp                      
                );
            """)

    target_user_dimension_table_create = ("""
                CREATE TABLE IF NOT EXISTS public.dim_user_history (
                    id SERIAL,
                    username varchar(250),
                    user_email varchar(250),
                    user_type varchar(250),
                    plan_name varchar(250),
                    created_at timestamp              
                );
            """)