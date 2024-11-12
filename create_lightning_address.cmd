@echo off
echo Creating Lightning Address...
curl --location --request POST 'https://api.zebedee.io/v0/lightning-addresses' ^
--header 'Content-Type: application/json' ^
--header 'apikey: JY2knFEHU13TxAPqqSH240nx7aao4OrN' ^
--data-raw '{
    "description": "Lightning Address BITQUIXO"
}'
echo Lightning Address creation completed.
pause
