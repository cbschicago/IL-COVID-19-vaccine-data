GENERATED_FILES: output/acs2019_5yr_B01003_05000US17021_simplified.geojson

.PHONY: all cleanup

all: $(GENERATED_FILES)

output/acs2019_5yr_B01003_05000US17021_simplified.geojson: input/acs2019_5yr_B01003_05000US17021.geojson
	npx mapshaper $< -simplify dp 10% keep-shapes -o format=geojson $@

cleanup:
	rm output/*