import asyncio
import logging


logger = logging.getLogger(__name__)

clients = {}


def validate_client(reader, writer):
	task = asyncio.Task(server_to_client(reader, writer))
	clients[task] = (reader, writer)

	def server_done(task):
		del clients[task]
		writer.close()
		logger.info("End Connection")

	logger.info("New Connection")
	task.add_done_callback(server_done)



async def server_to_client(reader, writer):
	#First say hello to client to confirm connection
	writer.write("HELLO\n".encode())

	#Client should respond within 5sec, otherwise timeout
	mydata, pending = await asyncio.wait(reader.read(), timeout=5)

	if mydata is None:
		logger.warning("Expected WORDDDDD, recieved None")
		return

	mydata_1 = mydata.decode().rstrip()
	logger.info("Recieved  {}".format(mydata_1))
	if mydata_1 != "WORDDDDD":
		logger.warning("Expected WORDDDDD, but recieved {}".format(mydata_1))

	#Echo back from server till client sends bye
	i = 0
	#Send READY message to client
	writer.write("READY\n".encode())
	while True:
		i = i + 1
		mydata1, pending = await asyncio.wait(reader.read(), timeout=5)
		if mydata1 is None:
			logger.warning("No data recieved")
			return

		mydata_2 = mydata1.decode().rstrip()
		if mydata_2.upper() == "BYE":
			writer.write("BYE\n".encode())
			break
		response = ("ECHO {}: {}".format(i, mydata_2[::-1]))
		writer.write(response.encode())


async def main():
	loop = asyncio.get_event_loop()
	svr = asyncio.start_server(validate_client, host=None, 4000)
	loop.run_until_complete(svr)
	loop.run_forever()


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