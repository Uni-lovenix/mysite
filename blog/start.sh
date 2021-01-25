conda activate py36

cd $PROJECTDIR
cp ~/settings.py $PROJECTDIR/mysite/

python manage.py runserver localhost:8000 --noreload