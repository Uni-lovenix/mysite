conda activate py36

cd $PROJECTDIR
cp -f ~/settings.py $PROJECTDIR/mysite/

python manage.py runserver localhost:8000 --noreload
