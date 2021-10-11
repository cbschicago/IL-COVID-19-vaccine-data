.PHONY: all data graphics

all: data graphics

data: \
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

graphics: \
		src/plot/idph_persons_fully_vaccinated_cumulative.py \
		src/plot/idph_persons_fully_vaccinated_daily.py \
		src/plot/full_vaccination_by_county.py
	log=output/log/plot_log.txt ; \
	> $$log ; \
	python -c "import datetime; print(datetime.datetime.today().isoformat())" > $$log ; \
	echo >> $$log ; \
	for SCRIPT in $^ ; \
	do \
		echo $$SCRIPT >> $$log ; \
		python $$SCRIPT >> $$log ; \
	done ;

force-refresh: src/update_graphics.py
	python $^ > output/log/refresh_log.txt
