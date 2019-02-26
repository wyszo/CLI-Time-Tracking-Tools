import unittest
import os
from unittest.mock import MagicMock

from logsWriter import LogsWriter, DateFormatter


class LogsWriterTestCase(unittest.TestCase):

	def test_create_dir_if_doesnt_exist(self):
		os.mkdir = MagicMock()

		# Given: log directory doesn't exist
		os.path.isdir = lambda dir: False

		# When: createLogsDir called
		sut = LogsWriter('mockDirName')
		sut.createLogsDir()

		# Then: mkdir should be called
		self.assertTrue(os.mkdir.called)

	def test_create_dir_if_it_exist(self):
		os.mkdir = MagicMock()

		# Given: directory exists
		os.path.isdir = lambda dir: True

		# When: createLogsDir called
		sut = LogsWriter('mockDirName')
		sut.createLogsDir()

		# Then: mkdir should NOT be called
		self.assertFalse(os.mkdir.called)


class DateFormatterTestCase(unittest.TestCase):
	def test_currentDate_returns_in_correct_format(self):
		date = DateFormatter().today()
		format_template = "yyyy-mm-dd"

		# check same length
		self.assertTrue(len(date) == len(format_template))

		# check if dashes are in correct places
		self.assertTrue(date[4] == date[7] == '-')

		# check if there are just digits apart from dashes
		date_no_dashes = date.replace('-','')
		self.assertTrue(date_no_dashes.isdigit())

if __name__ == '__main__':
	unittest.main()
