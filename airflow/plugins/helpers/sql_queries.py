class SqlQueries:
    target_organization_dimension_table_create = ("""
            CREATE TABLE IF NOT EXISTS public.dim_organization (
                id SERIAL UNIQUE,
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
                data_validation_failed varchar(1)
            );
        """)

    target_organization_report_table_create = ("""
                CREATE TABLE IF NOT EXISTS public.org_user_report (
                    id SERIAL UNIQUE,
                    organization_id int,
                    event_date date,
                    user_created_count int,
                    user_updated_count int,
                    user_deleted_count int,
                    CONSTRAINT fk_org_id
                        FOREIGN KEY (organization_id)
                            REFERENCES public.dim_organization(id)
                );
            """)

    target_user_dimension_table_create = ("""
                CREATE TABLE IF NOT EXISTS public.user (
                    id SERIAL UNIQUE,
                    organization_id int,
                    username varchar(250),
                    user_email varchar(250),
                    user_type varchar(250),
                    plan_name varchar(250),
                    is_active varchar(1),
                    created_at timestamp,
                    CONSTRAINT fk_user_org_id
                        FOREIGN KEY (organization_id)
                            REFERENCES public.dim_organization(id)                      
                );
            """)

    target_user_dimension_history_table_create = ("""
                CREATE TABLE IF NOT EXISTS public.user_events (
                    id SERIAL UNIQUE,
                    user_id int,
                    event_type varchar(250),
                    created_at timestamp              
                );
            """)

    data_validation_rule_org_name_missing = ("""
            UPDATE public.staging_events
            SET data_validation_failed = 'Y'
            WHERE organization_name IS NULL
            AND DATE(received_at) = '%s';
        """)

    data_validation_rule_user_name_missing = ("""
                UPDATE public.staging_events
                SET data_validation_failed = 'Y'
                WHERE username IS NULL
                AND DATE(received_at) = '%s';
            """)

    update_user_table = ("""
                UPDATE public.user
                SET is_active = 'N'
                WHERE username||organization_name IN 
                (SELECT username||organization_name
                FROM public.staging_events
                WHERE DATE(received_at) = '%s'
                AND data_validation_failed IS NULL);
    
    """)

    load_data_into_user_table = ("""
            INSERT INTO public.user
            SELECT public.dim_organization.id AS organization_id,
                    username,
                    user_email,
                    user_type,
                    plan_name,
                    'Y' AS is_active,
                    received_at AS created_at
            FROM public.staging_events,
            public.dim_organization
            WHERE public.staging_events.organization_name = public.dim_organization.organization_name
            AND DATE(received_at) = '%s'
            AND data_validation_failed IS NULL;
    """)

    load_data_into_user_event_table = ("""
            INSERT INTO public.user_events
            SELECT public.user.id AS user_id,
                    public.staging_events.event_type AS event_type
                    received_at AS created_at
            FROM public.staging_events,
            public.user
            WHERE public.staging_events.username = public.user.username
            AND DATE(received_at) = '%s'
            AND data_validation_failed IS NULL
            AND public.user.is_active = 'Y';
            """)

    load_data_into_fact_table = ("""
                    INSERT INTO public.org_user_report
                    SELECT public.dim_organization.id AS organization_id,
                        MAX('%s') AS event_date,
                        COUNT(user_created) AS user_created,
                        COUNT(user_updated) AS user_updated,
                        COUNT(user_deleted) AS user_deleted
                    FROM 
                        (SELECT public.staging_events.organization_name AS organization_name,
                                CASE
                                WHEN public.staging_events.event_date = 'User Created' THEN 1
                                ELSE 0
                                END AS user_created,
                                CASE
                                WHEN public.staging_events.event_date = 'User Updated' THEN 1
                                ELSE 0
                                END AS user_updated,
                                CASE
                                WHEN public.staging_events.event_date = 'User Deleted' THEN 1
                                ELSE 0
                                END AS user_deleted 
                                FROM public.staging_events
                                WHERE DATE(public.staging_events.received_at) = '%s'
                                AND data_validation_failed IS NULL
                        ) temp_tab,
                        public.dim_organization
                    WHERE  temp_tab.organization_name = public.dim_organization.organization_name
                    GROUP BY 1;
    """)
