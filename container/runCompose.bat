set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose -p App_AIS up -d --build
pause
docker-compose -p App_AIS down
