    all: compile

compile: classifier.c headers.h
	@echo Compiling classifier.
	gcc -g -o classifier classifier.c -lm

clean:
	@echo Deleting files.
	rm -f classifier
	rm -f *.csv
	rm -f *.png

.PHONY: clean