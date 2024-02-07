pip3 install Django
pip3 install xmltodict
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations WikiModel
python3 manage.py migrate WikiModel
python3 manage.py load_wiki_xml