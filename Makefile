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
	rm -f smalloutput.pdf

plot:
	python3 scripts/plot_progress.py

log:
	pdfinfo output.pdf -isodates | grep -E "(CreationDate|Pages|File size)" | xargs echo >> logs/size_log.txt
	tail -1 logs/size_log.txt

build:
	latexmk -f thesis.tex -view=pdf -c
	cp thesis.pdf output.pdf

buildold:
	pdflatex -shell-escape -jobname output -draftmode thesis.tex -interaction=batchmode
	pdflatex -shell-escape -jobname output thesis.tex -interaction=batchmode
	bibtex output
	makeindex thesis.tex
	pdflatex -shell-escape -jobname output -draftmode thesis.tex -interaction=batchmode
	pdflatex -shell-escape -jobname output thesis.tex 
	mkdir -p tmp
	mv *.{ind,blg,out,bbl,log,ilg,aux,toc} tmp/

# single spaced small version
small:
	pdflatex -shell-escape -jobname smalloutput "\def\myownflag{}\input{thesis}" -interaction=batchmode
	# mv -f *.{out,log,aux,toc,4ct,4tc,tmp,xref} tmp/
	mv -f *.{out,log,aux,toc} tmp/

push:
	git commit -a -m "update"
	git push
