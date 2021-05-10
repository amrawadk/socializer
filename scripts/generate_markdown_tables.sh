find docs_src -name \*.csv -print0 | while read -d $'\0' file
do
    csvtomd "$file" > $(sed 's/csv/md/' <<< "$file")
done