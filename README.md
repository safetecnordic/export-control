# exportcontrol

Info site for the Norwegian Export Control law.

## Project setup

1. Make sure you have Python 3.10 installed (https://www.python.org/downloads/)

```
python3 --version
```

2. Clone the repo (and navigate into it)

```
git clone https://github.com/cdp-group4/exportcontrol.git
cd exportcontrol
```

3. Set up Python virtual environment (to isolate dependencies)

```
python3 -m venv venv
```

4. Activate virtual environment

```
source venv/bin/activate
```

5. Install dependencies

```
pip install -r requirements.txt
```

6. Set up linting and formatting in VSCode

   - Install Python extension (https://marketplace.visualstudio.com/items?itemName=ms-python.python)
   - Open settings (File -> Preferences -> Settings)
   - Search `flake8` -> check `Python > Linting: Flake8 Enabled`
   - Search `formatting` -> choose `black` in `Python > Formatting Provider`
   - Search `format on save` -> check `Editor: Format On Save`


7. Make migrations 
   ```
   python manage.py migrate
   ```

8. Create admin user
   ```
   ./manage.py createsuperuser --username=admin --email=admin@example.com
   ```