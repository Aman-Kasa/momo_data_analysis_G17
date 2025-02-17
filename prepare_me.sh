#!/usr/bin/env sh
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Checking and installing required packages...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${GREEN}Installing Python3...${NC}"
    sudo apt-get install -y python3
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "${GREEN}Installing pip3...${NC}"
    sudo apt-get install -y python3-pip
fi

if ! command -v mysql &> /dev/null; then
    echo -e "${GREEN}Installing MySQL server...${NC}"
    sudo apt-get install -y mysql-server
fi

echo -e "${GREEN}Installing Python packages...${NC}"
pip3 install mysqlclient mysql-connector-python flask flask_cors python-dotenv

echo -e "${GREEN}Starting MySQL server...${NC}"
sudo service mysql start

echo -e "${GREEN}Loading environment variables...${NC}"
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo -e "${GREEN}.env file not found. Please create it with the required environment variables.${NC}"
    exit 1
fi

echo -e "${GREEN}Setting up the database...${NC}"
mysql -u root -p$MYSQL_PASSWD < prepare.sql

echo -e "${GREEN}Database is ready${NC}"