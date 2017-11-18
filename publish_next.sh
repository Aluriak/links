source venv/bin/activate
python3 publish_next.py --method=random
git add content/articles
curdate=$(date)
git commit -m "new link ($curdate)"
make publish
echo OK
