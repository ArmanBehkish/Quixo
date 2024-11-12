@echo off
echo Testing API endpoint...
curl --location --request POST 'https://api.zebedee.io/v0/payments' ^
--header 'Content-Type: application/json' ^
--header 'apikey: JY2knFEHU13TxAPqqSH240nx7aao4OrN' ^
--data-raw '{
    "invoice": "lnbc450n1p0yeytspp55yrs0j42wnkw0qutr8e0tgsf2yplxs9986t5gqmfpn7mfd0ckc8sdzq2pshjmt9de6zqen0wgsrgdfqwp5hsetvwvsxzapqwdshgmmndp5hxtnsd3skxefwxqzjccqp2sp5pyccqt6apxelz62d2ndrt0ssahndpcua4wklea80glaczx80t3wqrzjqfn4cln8jwe4dh4dmscddrmd6sdw6hzkn702l6ghwvr8lhad0ez5vzt8vyqqf2sqqqqqqqlgqqqqqqgq9q9qy9qsqqeft09gryr80aaghm7rmh7eeqfl7hxlcynp99730yk7qh534d9nyfwp0nc628rp8hpgp23fxzj5l2aet4y6sc4t79uj3wyjxffejmvgqrmxkvr",
    "description": "My Payment Description",
    "callbackUrl": "https://http://127.0.0.1:5000/zbd-callback",
    "internalId": "11af01d0cb33faa6b8304b8"
}'
echo API test completed.
pause
