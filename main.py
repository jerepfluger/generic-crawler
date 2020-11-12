# #!venv/bin/python
# # -*- encoding: utf-8 -*-
#
# import signal
# import sys
#
# import helpers.logger as log
# from api import ApiThread
# from worker import Worker
#
# worker = None
#
#
# def main():
#     global worker
#
#     api = ApiThread()
#     worker = Worker
#     worker.start
#     api.run()
#
#     worker.stop
#     worker.join
#
#
# def mainn():
#     worker = Worker
#     worker.run
#
#
# def sig_handler(sign, frame):
#     log.logger.info('Received signal {}. Stopping the app...'.format(sign))
#     if worker is not None:
#         worker.stop()
#         worker.join()
#     sys.exit(0)
#
#
# if __name__ == '__main__':
#     signal.signal(signal.SIGTERM, sig_handler)
#     main()
