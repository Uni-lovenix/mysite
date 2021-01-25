conda activate py36

cd $PROJECTDIR
cp -f ~/settings.py $PROJECTDIR/mysite/

gunicorn -w 4 --timeout 600 -b localhost:8000 mysite.wsgi
