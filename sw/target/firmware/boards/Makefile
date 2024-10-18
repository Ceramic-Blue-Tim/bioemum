ARCH ?= all
MSG_ERR_ARCH := "Invalid architecture specified. Use 'zynqmp' or 'versal'."

# subdirectories of kr260 under source directory - one per app
ifeq ($(ARCH), zynqmp)
APPS := $(wildcard kr260/*/)
else ifeq ($(ARCH), versal)
APPS := $(wildcard vpk120/*/)
else
@echo $(MSG_ERR_ARCH)
exit 1
endif

# Determine bitstream extension
ifeq ($(ARCH), zynqmp)
BSTEXT := bit
else ifeq ($(ARCH), versal)
BSTEXT := pdi
else
@echo $(MSG_ERR_ARCH)
exit 1
endif

# *.bit, *.dtsi, *.xclbin and shell.json files under these specific directories
BITS := $(wildcard $(patsubst %,%*.$(BSTEXT),$(APPS)))
DTSIS := $(wildcard $(patsubst %,%*.dtsi,$(APPS)))
XCLBINS := $(wildcard $(patsubst %,%*.xclbin,$(APPS)))
JSONS := $(wildcard $(patsubst %,%shell.json,$(APPS)))

# *.dtbo files to generate
DTBOS := $(patsubst %.dtsi,%.dtbo,$(DTSIS))

%.dtbo: %.dtsi
	dtc -I dts -O dtb -o $@ $<

# *.bif template
ifeq ($(ARCH), zynqmp)
BIF_TEMPLATE := template_zynqmp.bif
else ifeq ($(ARCH), versal)
BIF_TEMPLATE := template_versal.bif
else
@echo $(MSG_ERR_ARCH)
exit 1
endif

# *.bif and *.bins files to generate
BIFS := $(patsubst %.$(BSTEXT),%.bif,$(BITS))
BINS := $(patsubst %.$(BSTEXT),%.bin,$(BITS))

%.bif: %.$(BSTEXT)
	sed 's#@BIT@#$<#' <$(BIF_TEMPLATE) >$@

%.bin: %.bif
	bootgen -image $< -arch $(ARCH) -o $@ -w

default: all

all: bins dtbos
bins: $(BINS)
dtbos: $(DTBOS)

clean:
	rm -f $(BIFS)
	rm -f $(BINS)
	rm -f $(DTBOS)

INSTALLDIR := $(DESTDIR)/lib/firmware/xilinx

ifeq ($(ARCH), zynqmp)
install: $(BINS) $(DTBOS) $(XCLBINS) $(JSONS)
	for f in $^; do \
	    file=$$(basename $$f); \
	    app=$$(basename $$(dirname $$f)); \
	    board=$$(basename $$(dirname $$(dirname $$f))); \
	    install -D -m 644 \
	        $$f $(INSTALLDIR)/$$board-$$app/$$file; \
	done
else ifeq ($(ARCH), versal)
install: $(BITS) $(DTBOS)
	for f in $^; do \
	    file=$$(basename $$f); \
	    app=$$(basename $$(dirname $$f)); \
	    board=$$(basename $$(dirname $$(dirname $$f))); \
	    install -D -m 644 \
	        $$f $(INSTALLDIR)/$$board-$$app/$$file; \
	done
else
	@echo $(MSG_ERR_ARCH)
	exit 1
endif

.PHONY: default all bins dtbos clean install

