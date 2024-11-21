import unittest
import pandas as pd
from Ingestionnotebook import read_and_clean_employee_data

#test

class TestIngestionNotebookWithBusinessRules(unittest.TestCase):

    def setUp(self):
        """
        Setup test data and mock file paths.
        """
        self.file_path = "test_employee.csv"

    def tearDown(self):
        """
        Cleanup after tests.
        """
        import os
        os.remove(self.file_path)

    def write_test_file(self, data):
        """
        Utility function to write test data to a file.
        """
        with open(self.file_path, "w") as f:
            f.write(data)

    def test_employee_id_validation(self):
        """
        Test that only positive and unique employee IDs are retained.
        """
        sample_data = """EmpID,FirstName,LastName,Salary
1,John,Garcia,100000
-2,Alex,Garcia,80008
3,Kim,Brown,63106
1,Taylor,Smith,90000"""
        self.write_test_file(sample_data)

        result = read_and_clean_employee_data(self.file_path)

        expected_data = {
            "EmpID": [1, 3],
            "FirstName": ["John", "Kim"],
            "LastName": ["Garcia", "Brown"],
            "Salary": [100000, 63106]
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(result, expected_df)

    def test_salary_validation(self):
        """
        Test that salary values are within valid range.
        """
        sample_data = """EmpID,FirstName,LastName,Salary
1,John,Garcia,100000
2,Alex,Garcia,250000
3,Kim,Brown,-5000"""
        self.write_test_file(sample_data)

        result = read_and_clean_employee_data(self.file_path)

        expected_data = {
            "EmpID": [1],
            "FirstName": ["John"],
            "LastName": ["Garcia"],
            "Salary": [100000]
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(result, expected_df)

    def test_name_validation(self):
        """
        Test that names contain only alphabetic characters.
        """
        sample_data = """EmpID,FirstName,LastName,Salary
1,John123,Garcia,100000
2,Alex,Garcia123,80008
3,Kim,Brown,63106"""
        self.write_test_file(sample_data)

        result = read_and_clean_employee_data(self.file_path)

        expected_data = {
            "EmpID": [3],
            "FirstName": ["Kim"],
            "LastName": ["Brown"],
            "Salary": [63106]
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(result, expected_df)

    def test_duplicate_removal(self):
        """
        Test that duplicate rows are removed.
        """
        sample_data = """EmpID,FirstName,LastName,Salary
1,John,Garcia,100000
2,Alex,Garcia,80008
1,John,Garcia,100000"""
        self.write_test_file(sample_data)

        result = read_and_clean_employee_data(self.file_path)

        expected_data = {
            "EmpID": [1, 2],
            "FirstName": ["John", "Alex"],
            "LastName": ["Garcia", "Garcia"],
            "Salary": [100000, 80008]
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(result, expected_df)

if __name__ == "__main__":
    unittest.main()
