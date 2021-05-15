-- Creation of organization table
CREATE TABLE IF NOT EXISTS dim_organization (
  organization_key varchar(50) NOT NULL,
  organization_name varchar(250) NOT NULL,
  created_at timestamp,
  PRIMARY KEY (organization_key)
);

-- Creation of events stage table
CREATE TABLE IF NOT EXISTS stg_events (
  id varchar(50),
  event_type varchar(250),
  username  varchar(250),
  user_email varchar(250),
  user_type varchar(250),
  organization_name varchar(250),
  plan_name varchar(250),
  received_at timestamp
);