CREATE USER domotic_rest_api WITH NOINHERRIT PASSWORD 'RESTAPITEST';
CREATE ROLE api_perms NOINHERRIT;
CREATE ROLE anonymous NOINHERRIT;

GRANT api_perms TO domotic_rest_api;
GRANT anonymous TO domotic_rest_api;

GRANT SELECT ON groundwater TO api_perms;
GRANT SELECT ON water_pump TO api_perms;
GRANT SELECT ON device TO api_perms;
GRANT SELECT ON component TO api_perms;

GRANT UPDATE (pump_time, groundwatersensor_id, target_groundwater_value) ON water_pump TO api_perms;
GRANT UPDATE (name) ON device TO api_perms;

GRANT EXECUTE ON FUNCTION jwt_test( ) TO anonymous; 


CREATE OR REPLACE TYPE jwt_token AS (
  token text
)

CREATE OR REPLACE FUNCTION jwt_test ( ) RETURNS jwt_token AS $$
    SELECT public.sign(
        row_to_json(r), current_setting('app.settings.jwt_secret') 
    ) AS token
    FROM ( 
        SELECT 'api_perms'::text as role 
    ) r;
$$ LANGUAGE plpgsql 