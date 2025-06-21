PYTHON = python3
SPHINXBUILD = $(PYTHON) -m sphinx
BUILDDIR = _build
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .
SPHINXBUILD = $(PYTHON) -m sphinx

.PHONY: help clean html

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  clean     to clean the build directory"

clean:
	rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
