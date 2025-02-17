# Momo Data Analysis Group-17

![momo MTN](https://techfocus24.com/mtn-momo-vodafone-cash-enable-merchant-i/)

## Overview
This project is designed for analyzing Momo data. It leverages various data analysis techniques and tools to provide insights and visualizations.

## Repository Structure
- `api/`: Contains the Flask API implementation.
- `scripts/`: Python scripts for data analysis.
- `data/`: Sample datasets used for analysis.
- `docs/`: Documentation files.
- `tests/`: Unit tests for the project.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Aman-Kasa/momo_data_analysis_G17.git
    cd momo_data_analysis_G17
    ```

2. Install dependencies:
    ```sh
    pip3 install -r requirements.txt
    ```

## Usage
1. Start the Flask API:
    ```sh
    python3 api.py
    ```

2. Access the API at `http://127.0.0.1:5000`.

## Deployment
1. SSH into your server and navigate to the project directory:
    ```sh
    ssh ubuntu@your-server-ip
    cd /home/ubuntu/momo_data_analysis_G17
    ```

2. Install necessary dependencies:
    ```sh
    sudo apt update
    sudo apt install python3 python3-pip nginx -y
    pip3 install -r requirements.txt
    ```

3. Configure Nginx and run the app with Gunicorn:
    ```sh
    sudo nano /etc/nginx/sites-available/default
    ```
    Add the configuration:
    ```nginx
    server {
        listen 80;
        server_name your_domain_or_ip;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```
    Save and exit the file, then restart Nginx:
    ```sh
    sudo systemctl restart nginx
    ```

4. Run the Flask app with Gunicorn:                 
    ```sh 
    pip3 install gunicorn
    gunicorn -w 4 -b 127.0.0.1:8000 api:app
    ```
    OR
    run the Db_saver.py
    then run the api.py
    next open the live server on 
    python api.py 
                @##* Serving Flask app 'api'
                @##* Running on http://127.0.0.1:8000

## Contributing 
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License.

## Contact
For inquiries, please contact [Aman-Kasa](https://github.com/Aman-Kasa).