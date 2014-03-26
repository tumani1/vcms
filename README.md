# Setup App #

    - install libs

        `pip install -r ./requirements.txt`

    - create db

        `fab setup_db_locally`

    - sybcdb

        `python ./manage.py syncdb`

    - migrate

        `python manage.py migrate`

    - run server

        `python manage.py runserver`
