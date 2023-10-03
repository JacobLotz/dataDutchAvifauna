all: plot pdf

.PHONY: clean

plot:
	python3 getdata.py
new:
	python3 getdata.py --new-data
	pdf
pdf:
	mkdir pdfs
	cp */*.pdf pdfs/.
clean:
	rm -r */ 

cleandata:
	rm data.csv
	
fresh: clean cleandata

	
