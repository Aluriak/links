source venv/bin/activate
python3 add_next.py
git add content/articles
curdate=$(date)
git commit "new link ($curdate)"
make publish
echo OK
