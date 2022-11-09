curl -X POST -u "apikey:-wf8diqQ04TukZMsHIqMubVmNUdadCI_KZUZstIXSIJp" \
	--header "Content-Type: application/json" \
	--data '{ "url": "https://santiagonzalez.wordpress.com/2021/03/20/murcia-como-metafora/", "features": { "sentiment": {}, "categories": {}, "concepts": {}, "entities": {}, "keywords": {} } }' \
       	"https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/6dea0787-b7c0-496c-b8f4-343edddb8ad9/v1/analyze?version=2019-07-12"

