CREATE EXTENSION pgcrypto;
CREATE EXTENSION pgjwt;

CREATE USER domotic_rest_api WITH NOINHERIT PASSWORD '+Dn7S-RnDEtLabutG2MtpDtbcqAp1EMuTf8KCYyPSKqb7LhqsntRsw==';
CREATE ROLE anonymous NOINHERIT;
CREATE ROLE api_perms NOINHERIT;

GRANT anonymous TO domotic_rest_api;
GRANT api_perms TO domotic_rest_api;

CREATE TYPE jwt_token AS (
  token text
);

CREATE FUNCTION jwt_test() RETURNS public.jwt_token AS $$
  SELECT public.sign(
    row_to_json(r), 'ALAnF20EW+Sw-5rNRfqINUONNNQVFbCkxteoOL-MV8H5CH3DPTdr3zNdoUr3xAnUjYS1C7ZGICaJ10dkeOEtIEXC5YSXztEiGFFaQQtF4kraI69wM3pfzUwa4I1khtXg2c+E0i6hIzuCyr3Dp+ad9c0sbViQGPP8TA1f4xaxVuxQCs4FsNSfyOxGeDG2MLvkqWRm1HWACIhJYrFrbjLJcIhwYk3xQ3g-dPsYF9VNh9ROIYSKS1AtD2ojmhFRax9yGSbBAr3YUunAmzv8yu+KvZJMF7j5AadjO90o+DAwr8xmswUqwYpw5LlpQCgaMcM1-acZHLlykHoYiW7MVpYktdTTurSkz66q-N1JQB7z3G9JkuKVWrhu4BLiCF0sVQsEJpysaTO0Kb1hKyfqPEjgicJpm0nxEvOsjumPqi4e+pQ0TXlDpWTsPyDCvK13Hv2iaOOt4YHzDhJ66k23O0Fgkat5ln5TqhZaMex8jWcogTlX7raK0ep0bZy2WHHfSbfLWarKdnx4U6kKeTI7m9YEVT9DZbkCWEw0LFgrg-6vt6tnwN5G3ICpnsjmnUSZgOfzNKlGk9D4Ks05LoleV45iht68Rzy8Nc7cya5ec3ZKCxwIecpj-0zMpJDnECyk2u8aYStucWafw1oceRtlEcfCoV010wW8kmx4+FPz7gmYDV0hg-lTSUIEpqlVZV5tEtoT0uO1c+U-EFT8NU3OjV0ZNc4OPYqHOtlkmlYhmRWVZa-vKFrCYPoqEG0wHwgOfwMJJ9vP3SzMX0hPTqFTGVUHcLfr7SQZIiKgSqOJKpj02bj+3nRacTA1ZOJW28SU2A6qU23RsyXaIxYHf497-yI1eyYS3ZFcYK8nginT+TmFPzKGEVI5VtoRrGACzsY4BRiK-EQICWvVdgZ+Vh6jyqZoxDQ6zCmCSlQuShmMCx5kaiHgTckWuvLnFn-f7Pu+Ob-+VTx6hjzQQL-UcdIHg17Y2EUcXHSgXf1C4yKs2eQ4PXDO8g66bXQty8nodUfisu+VwSJSxy7wIhvT-a-LFo3Vla7HbUtydZvLwbjwD1uq6mMx0fNMaRmaK5P-EFJj7G+hmsSOSjttF7VtZ4G5OE5UsRBPNDx2OHXm2y0Hic7+2zCP8FxkV9PbW8Fs04hK3iLl9NpL2rXBe-vFBShhxxU4JZjYWGGu+rxyULOqM2PF8eT2gEbU8BJ+db8w2GrPxKm9Q9u08XDyHZANg2Mil6sE87dAE1fBm9-mwwjTf0KbJwAg1F+Tx7f8M8ZS9i7nV1Px+f+meEE8jPRQd5SMjSkVU1EoouPzpgaN0luqewXs9qhInZqh7vU62ZF8Wqzpgu8VS0+Pdui0tPb83pISSrsdtsKdP7t8boVLDL1Hb1gxRjo2CRs4REBmqEgCNMrNIR+YInXactAoJKnwXe5MdwUJJiwP8RmFwFgn46he506awHF8tFUzvSN-94mwBV-5uj-0fR0Dml9QqXI0a1GzNFtssVpsLHIPo9GFUUnQVTVu0j+4s2yOJDoyp9L99NAyz6ILRJNkoBiwKS1QVEpeoq6XWZFeBmK9FTT7o5QUfOsArQavjAPYtfvBkGvh8EqnQCYtj2xyF2o2+ggXUGn2TL06xDKlRjmLnL74GESETzqEpnu0f6CpbrU1c9Iiq-tvkfwzZO4v9v1ZgPxcBckPfktISRulBFoVIPJMvJh1WCK4xt393kx2Z43JBMT8LBHCReNDbAMTi4lJyUT05BnOSA-YlcmgdMunzYIxBsu27OjXyKQxZ3FVa8dwtQbwVg8-JHjfaET65lvsqQa-y-aOfcT0-tErm4czzfiADFa3ckcqRRAVpn4XZ7lFqmqmpGaga8cA3cU5sjk2YdoyCVtbHiYGYLIGoFpECt76zk9ULRDQM9CVC574Ons-XLLiR3V3LpqT9TJSFHwWfvPvWXK-jWAbJgGlcpvRlqIA1I1PmdOUA7pTEmico4kju3D1uVE5bcxOjTOsrBho-JtSZKzzolWKftfstXxRVaFZk+nMFHEl7Bxj9HeH1BypPe+KXaqJMJRyymGZAVcheEtRR0vSv14lNDmGGPRZIGLSQhsQoH4RzBWRWCm2LtUy+ssbgKBhUymkfNg0ZLazwdv+8dZyjONvLfcVQO6ybGJ53lSoM913bwRK982JxsIJLkbXk2OOsudMfTRrHXI8soa6Op5gZZKTxxZU3AwyL8cXJ2l38p8VfGYPWhGSge44S+Oxyr-55RM5gclxYKq5jRHwjzZZ9YTD3hSabtYeeTbjbS8ox37yM+678xY9QNsqjcL35xB3RB7VNrTJrNutVeRcybQ9aoZIwEJ1rQ4-o2uukbkASLqekjCk9LvkR4iHBjNuFBCDX+r-YuJfAJxY85XapS2uBY-pJ6cjZoOn9mJ2pWla8bhQWJnktEyzpk6IZwiEo81w6QqXRpJIxZlmR9rRlFjIjDTuHnvTfhaxRs0g7JHR0PuWP9ueo3TFlM4EcbEKJsQOwAi-vnfKVOKioWJRAdzw-DuZHjWu9an8uj4rI+1X-zzF1+ZaXdK6B5QDQNQMhqpXD5P1lXyq160zoOnLuandGLZLHfjeH0QsEcycoXeqlIHeVhBC+kDn4P5DJLmlRuAoXq7+HVjppbCjrsTkCOXPIRnWlw0iwaiUpmOBci87jJDMKi5P7vvnCn7z1+TUqTRg1XBlb1qky7bO0aXR6Pgme28DAZha4nhuJfpCa8UOljyUDG0='
  ) AS token
  FROM (
    SELECT
      'api_perms'::text as role--,
      --extract(epoch from now())::integer + 300 AS exp
  ) r;
$$ LANGUAGE sql;
