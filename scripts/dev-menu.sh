#!/bin/bash

clear
ROOT_DIRETORY="$(pwd)"

CONTAINER_PYTHON=skoob
CONTAINER_POSTGRES=psql
# CONTAINER_ADMINER=adminer
# CONTAINER_PGADMIN=pgadmin

CONTAINERS="$CONTAINER_PYTHON $CONTAINER_POSTGRES"

COMPOSE_FILE=docker-compose.dev.yml

COLUMNS=1
PS3=$'\nSelect: '
select OPTIONS in \
    "Start Server" \
    "Run Tests" \
    "Create Super User" \
    "Stop Server" \
    "Show Logs" \
    "Open $CONTAINER_PYTHON Container" \
    "Delete Containers" \
    "Delete Data" \
    "Delete Images and Containers" \
    "Close"; do

case $OPTIONS in

    "Start Server")
        clear
        sudo docker compose -f $COMPOSE_FILE up -d
        echo ""

        echo "Server Running..."
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Run Tests")
        clear
        sudo docker container exec -it $CONTAINER_PYTHON python3 manage.py test
        echo ""

        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Create Super User")
        clear
        sudo docker container exec -it $CONTAINER_PYTHON python3 manage.py createsuperuser
        echo ""

        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Stop Server")
        clear
        echo "Stopping $CONTAINERS..."

        sudo docker container stop $CONTAINERS

        echo ""
        echo "Containers stopped."
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Show Logs")
        clear
        echo "Ctrl+C to Close"

        sudo docker logs -f $CONTAINER_PYTHON

        read -p "[Press Enter to Close]"
        clear

        COLUMNS=1
        ;;

    "Open $CONTAINER_PYTHON Container")
        clear
        echo "Ctrl+D to Exit Container"

        sudo docker exec -it $CONTAINER_PYTHON  sh

        read -p "[Press Enter to Close]"
        clear

        COLUMNS=1
        ;;

    "Delete Containers")
        clear

        sudo docker compose -f $COMPOSE_FILE down

        echo ""
        echo "Containers and Volumes Deleted."
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Delete Data")
        clear

        sudo rm -rf $ROOT_DIRETORY/data/postgres/data

        echo ""
        echo "Data deleted."
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Delete Images and Containers")
        clear

        sudo docker compose -f $COMPOSE_FILE down --rmi 'all'

        echo ""
        echo "Environment Deleted."
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Close")
        clear
        break
        COLUMNS=1
        ;;
esac
done