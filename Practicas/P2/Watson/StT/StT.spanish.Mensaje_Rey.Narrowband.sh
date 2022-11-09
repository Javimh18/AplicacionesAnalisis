curl -X POST -u "apikey:_m_ygizLpIXx96DKZg7GqfgoJK-1Hgw4mbzYcU27QUpz" \
	--header "Content-Type: audio/mp3" \
	--data-binary @mensaje-de-navidad-de-su-majestad-el-rey-2020.mp3 \
	--output "Mensaje_del_rey_StT.json" \
	"https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/899315cf-8053-4f99-8e7c-2c89bb3c11f5/v1/recognize?model=es-ES_NarrowbandModel"

