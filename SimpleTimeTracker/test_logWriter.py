
import unittest
from unittest.mock import MagicMock
import os

from logswriter import LogsWriter


class LogsWriterTestCase(unittest.TestCase):

	def test_create_dir_if_doesnt_exist(self):
		os.mkdir = MagicMock()

		# Given: log directory doesn't exist
		os.path.isdir = lambda dir: False

		# When: create_logs_dir called
		sut = LogsWriter('mockDirName', 'mockLogName')
		sut.create_logs_dir()

		# Then: mkdir should be called
		self.assertTrue(os.mkdir.called)

	def test_create_dir_if_it_exist(self):
		os.mkdir = MagicMock()

		# Given: directory exists
		os.path.isdir = lambda dir: True

		# When: create_logs_dir called
		sut = LogsWriter('mockDirName', 'mockLogName')
		sut.create_logs_dir()

		# Then: mkdir should NOT be called
		self.assertFalse(os.mkdir.called)


if __name__ == '__main__':
	unittest.main()
