all: plot

.PHONY: clean

plot:
	python3 getdata.py
new:
	python3 getdata.py --new-data
