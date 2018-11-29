import random
import asyncio
import logging

logger = logging.getlogger(__name__)

clients = {}


def create_connection(host, port):

	task = asyncio.Task(handle_client(host, port))

	clients[task] = (host, port)

	def client_done(task):
		del clients[tasks]
		logger.info("Clients Task Finished")
		if len(clients) == 0:
			log.info("Emppty client, stopping loop")
			loop = asyncio.get_event_loop()
			loop.stop()

	logger.info("New Client Task")
	task.add_done_callback(client_done())


async def client_to_server(host, port):
	logger.info("connecting to {} on port {}".format(host, port))
	reader, writer = await asyncio.open_connection(host=host, port=port)
	logger.info("Connected to {}:{}".format(host, port))

	try:
		#Client expecting Hello response from server, timeout after 5seconds
		data, pending = await asyncio.wait(reader.read(), timeout=5)
		if data is None:
			logger.warning("No response recieved")
			return

		mydata = data.decode().rstrip()
		logger.info("Recieved {}".format(mydata))

		if mydata != "HELLO":
			logger.warning("Expected HELLO, but recieved {}".format(mydata))
			return

		#send a word to check if server is ready and wait
		writer.write("WORDDDDD\n".encode())

		#wait 5sec for READY from the server
		data_1, pending  = await asyncio.wait(reader.read(), timeout=5)

		if data_1 is None:
			logger.warning("Expected READY, but recieved None")
			return

		mydata1 = data_1.decode().rstrip()
		if mydata1 != "READY":
			logger.warning("Expected READY, but recieved {}".format(mydata1))
			return


		all_message = ['Hello Server', 'Howdy!', 'Hi Localhost', 'Whats up?']

		#Randomly pick a message to send to the and get a reply back
		for val in range(len(all_message)):
			msg = random.choice(all_message)
			writer.write(("{}\n".format(msg)).encode())
			data_2, pending = await asyncio.wait(reader.read(), timeout=5)

			if data_2 is None:
				logger.warning("Echo received None")
				return
			mydata2 = data_2.decode().rstrip()
			logger.info(mydata2)
		#Gracefully disconnect
		writer.write("BYE\n".encode())

		#recieve BYE confirmation

		bye_data, pending = await asyncio.wait(reader.read(), timeout=5)
		bye_data_1 = bye_data.decode().rstrip()
		logger.info("Recieved {}".format(bye_data_1))
	finally:
		log.info("Disconnecting from {}:{}".format(host, port))
		writer.close()
		logger.info("Disconnected from {}:{}".format(host, port))



async def main():
	logger.info("Starting MAIN function")
	loop = asyncio.get_event_loop()
	my_loop = [create_connection('localhost', 4000) for i in range(100)]
	loop.run_until_complete(asyncio.wait(my_loop))
	loop.close()


if __nmae__ == '__main__':
	logger = logging.getlogger("")
	formatter = logging.Formatter("%(asctime)s %(levelname)s " + "[%(module)s:%(lineold)d] %(message)s")

	#console logging
	logger.setLevel(logging.DEBUG)
	lg = logging.StreamHandler()
	lg.setLevel(logging.DEBUG)

	lg.setFormatter(formatter)
	logger.addHandler(lg)
	main()


