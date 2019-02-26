import unittest
from dateformatter import DateFormatter


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
