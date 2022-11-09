curl -X POST -u "apikey:FyKXNEmsqY6p5hHzkQLOhUdPkJ89FRXOzyC217ikdEky" \
	--header "Content-Type: application/json" \
	--header "Accept: audio/wav" \
	--data "{\"text\":\"hello world\"}" \
	--output hello_world.wav \
	"https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/0642d19b-5f35-49aa-a53c-34fb024a4331/v1/synthesize"

