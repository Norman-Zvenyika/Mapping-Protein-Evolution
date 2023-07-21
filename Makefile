# Makefile for Phylogenetic Tree Construction

# Create necessary directories if they do not exist
.PHONY: create_dirs
create_dirs:
	@mkdir -p results

# Run the program
.PHONY: run
run: clean create_dirs
	@python3 src/main.py

# Clean up output files
.PHONY: clean
clean:
	@rm -f results/*