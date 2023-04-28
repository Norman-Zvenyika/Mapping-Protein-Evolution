# Set the ClustalW2 executable path
CLUSTALW2 = ./src/clustalw2

# Create output directory
OUTPUT_DIR = clustalW2Output

# Input and output filenames
INPUT_FASTA = data/example.fasta
ALIGNED_FASTA = $(OUTPUT_DIR)/aligned.fasta

# .dnd file output
DND_OUTPUT = $(OUTPUT_DIR)/example.dnd

# Create output directory if it doesn't exist
create_output_dir:
	mkdir -p $(OUTPUT_DIR)

clust:
	$(CLUSTALW2) -INFILE=$(INPUT_FASTA) -OUTFILE=$(ALIGNED_FASTA) -OUTPUT=FASTA
	mv data/example.dnd $(OUTPUT_DIR)/example.dnd

run:
	python3 src/main.py

clean:
	rm -f results/*
	rm -f $(ALIGNED_FASTA) $(DND_OUTPUT)
	rm -f clustalW2Output/*.txt