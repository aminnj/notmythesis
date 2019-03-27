FILE=thesis

all: $(FILE).pdf

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
	rm -f ${FILE}.pdf


$(FILE).pdf: thesis.tex bib/thesis.bib sty/*.sty
	pdflatex -shell-escape $(FILE).tex
	pdflatex -shell-escape $(FILE).tex
	makeindex $(FILE).tex
	bibtex $(FILE)
	pdflatex -shell-escape $(FILE).tex
	pdflatex -shell-escape $(FILE).tex
	mkdir -p tmp
	mv *.{ind,blg,out,bbl,log,ilg,aux,toc} tmp/
