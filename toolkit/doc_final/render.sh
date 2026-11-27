cd /home/claude/doc
for c in "$@"; do
  for k in 0 1 2 3 4 5; do python3 doc.py $c part $k 6 & done; wait
  python3 doc.py $c final 6
done
echo ALLDONE
