target: registration-district.tsv \
	../../maps/gss.tsv

clean:
	rm -f registration-district.tsv
	rm -f ../../maps/gss.tsv

registration-district.tsv:
	curl -ks https://geoportal.statistics.gov.uk/datasets/ab365dcd27c64d04bcda8c5c019657a0_0.csv \
	| csvformat -T \
	> $@

registration-district-map.tsv:
	curl -ks https://geoportal.statistics.gov.uk/datasets/5a44fa3bc2894f968b711c194f74c2e7_0.csv \
	| csvformat -T \
	> $@

district-county-map.tsv:
	curl -ks https://geoportal.statistics.gov.uk/datasets/180a69233de94a8da3fb6a8a4959fcc7_0.csv \
	| csvformat -T \
	> $@

../../maps/gss.tsv: borough-and-unitary-authority-map.tsv county-map.tsv
	csvstack borough-and-unitary-authority-map.tsv county-map.tsv > $@

borough-and-unitary-authority-map.tsv: registration-district-map.tsv
	# join by GSS code to get local-authority borough code
	csvjoin -tc LAD16CD,gss registration-district-map.tsv ../../../local-authority-data/maps/gss.tsv \
	| csvcut -C name \
	| csvcut -c local-authority,LAD16CD,LAD16NM,REGD16CD,REGD16NM \
	| csvsort \
	| uniq \
	| csvformat -T > map-with-borough-local-authority.tsv
  # join by local-authority code to get district
	(\
	echo "gss,registration-district,name,registration-district-name" \
	&& csvjoin -tc local-authority map-with-borough-local-authority.tsv ../../../local-authority-data/maps/registration-district.tsv \
	| csvcut -c REGD16CD,registration-district,REGD16NM,name \
	| sed 's/REGD16CD.*//' \
	| awk 'NF' \
	| sort -u \
	| sed 's/W20000002,811.*//' \
	| sed 's/W20000003,805.*//' \
	| awk 'NF' \
	) \
	| csvformat -T \
	> $@ && rm -f map-with-borough-local-authority.tsv

county-map.tsv: registration-district-map.tsv district-county-map.tsv
	# join by GSS borough code to get GSS county code
	csvjoin -tc LAD16CD,1 registration-district-map.tsv district-county-map.tsv \
	| csvcut -C 1,2,5,6,9,10,11,14 \
	| csvsort \
	| uniq \
	| csvformat -T > map-with-county-gss.tsv

	# join by GSS county code to get county local-authority code
	csvjoin -tc gss,CTY16CD ../../../local-authority-data/maps/gss.tsv map-with-county-gss.tsv \
	| csvcut -C name \
	| csvcut -c local-authority,CTY16CD,CTY16NM,REGD16CD,REGD16NM \
	| csvsort \
	| uniq \
	| csvformat -T > map-with-county-local-authority.tsv

	(\
	echo "gss,registration-district,name,registration-district-name" \
	&& csvjoin -tc local-authority map-with-county-local-authority.tsv ../../../local-authority-data/maps/registration-district.tsv \
	| csvcut -c REGD16CD,registration-district,REGD16NM,name \
	| sed 's/REGD16CD.*//' \
	| sort -u \
	| awk 'NF' \
	) \
	| csvformat -T \
	> $@ && rm -f map-with-county-gss.tsv && rm -f map-with-county-local-authority.tsv