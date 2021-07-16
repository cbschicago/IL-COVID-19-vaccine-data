.PHONY: all

all: \
		src/scrapers/get_cdph_citywide_by_day.py \
		src/scrapers/get_cdph_zip_code_current.py \
		src/scrapers/get_idph_administration_current.py \
		src/scrapers/get_idph_cumulative_daily.py \
		src/scrapers/get_idph_demographics.py \
		src/scrapers/get_indiana_dph_cumulative_daily.py
	log=output/log/log.txt ; \
	> $$log ; \
	python -c "import datetime; print(datetime.datetime.today().isoformat())" > $$log ; \
	echo >> $$log ; \
	for SCRIPT in $^ ; \
	do \
		echo $$SCRIPT >> $$log ; \
		python $$SCRIPT >> $$log ; \
	done ;
