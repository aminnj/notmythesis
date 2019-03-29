all: build log
.PHONY: clean 

clean:
	rm -rf *.blg 
	rm -rf *.out 
	rm -rf *.bbl 
	rm -rf *.log
	rm -rf *.ind
	rm -rf *.ilg
	rm -rf *.lot
	rm -rf *.lof
	rm -rf *.idx
	rm -rf *.aux
	rm -rf *.toc
	rm -f thesis.pdf
	rm -f output.pdf

log:
	pdfinfo output.pdf -isodates | grep -E "(CreationDate|Pages|File size)" | xargs echo >> logs/size_log.txt

build:
	pdflatex -shell-escape -jobname output thesis.tex 
	pdflatex -shell-escape -jobname output thesis.tex 
	makeindex thesis.tex
	bibtex output
	pdflatex -shell-escape -jobname output thesis.tex 
	pdflatex -shell-escape -jobname output thesis.tex 
	mkdir -p tmp
	mv *.{ind,blg,out,bbl,log,ilg,aux,toc} tmp/
