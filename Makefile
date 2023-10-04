all: plot pdf

.PHONY: clean

plot:
	python3 getdata.py

newdata:
	python3 getdata.py --new-data

pdf:
	mkdir pdfs
	cp */*.pdf pdfs/.
clean:
	rm -r */ 

cleandata:
	rm data.csv
	
fresh: clean cleandata

new:
	newdata pdf
	
