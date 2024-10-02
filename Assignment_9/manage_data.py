import os
import pandas as pd
from config import SCRIPT_LOCATION, RESOURCES_DIR

class ManageData:
    def __init__(self):
        self.__script_location = SCRIPT_LOCATION
        self.__data_to_read_loc = f'{self.__script_location}/data/student_scores_random_names.csv'
        self.__avg_scores_per_semester_loc = f'{self.__script_location}/resources/average_scores_per_semester.xlsx'
        self.__df = self.__read_data()
        
    def __read_data(self):
        try:
            df = pd.read_csv(self.__data_to_read_loc)
            return df
        except FileNotFoundError:
            print(f"Error: The file '{self.__data_to_read_loc}' was not found.")
            return None
        except PermissionError:
            print(f"Error: Permission denied when trying to read '{self.__data_to_read_loc}'.")
            return None
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            return None
        except pd.errors.ParserError:
            print("Error: There was a problem parsing the CSV file.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        
    def get_failed_students(self):
        if self.__df is not None:
            failed_students = self.__df[self.__df[
                ['Math', 'Physics', 'Chemistry', 'Biology', 'English']].lt(50).any(axis=1)]
            return failed_students['Student'].unique().tolist()
        return None
    
    def get_avg_scores_per_semester(self):
        if self.__df is not None:
            avg_scores_per_semester = self.__df. \
            groupby('Semester')[['Math', 'Physics', 'Chemistry', 'Biology', 'English']].mean().round(2)
            self.__save_avg_scores_per_semester(avg_scores_per_semester)
            return avg_scores_per_semester
        return None
    
    def get_highest_avg_student(self):
        if self.__df is not None:
            self.__df['Average_Score'] = self.__df[['Math', 'Physics', 'Chemistry', 'Biology', 'English']].mean(axis=1)
            return self.__df.groupby('Student')['Average_Score'].mean().idxmax()
        return None
    
    def get_lowest_avg_subject(self):
        if self.__df is not None:
            subject_avg = self.__df[['Math', 'Physics', 'Chemistry', 'Biology', 'English']].mean()
            return subject_avg.idxmin()
        return None
    
    def __save_avg_scores_per_semester(self, avg_scores_per_semester=None):
        if not os.path.exists(RESOURCES_DIR):
            os.makedirs(RESOURCES_DIR)
        if avg_scores_per_semester is not None:
            try:
                avg_scores_per_semester.to_excel(self.__avg_scores_per_semester_loc, index=True)
                return True
            except PermissionError:
                print(f"Error: Permission denied when trying to write '{self.__avg_scores_per_semester_loc}'.")
                return False
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return False

    @staticmethod
    def __is_improving(group):
        subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'English']
        for subject in subjects:
            if group[subject].is_monotonic_increasing:
                return True
        return False
    
    def get_improving_students(self):
        if self.__df is not None:
            df_sorted = self.__df.sort_values(by=['Student', 'Semester'])
            improving_students = df_sorted.groupby('Student') \
            .filter(self.__is_improving)['Student'].unique()
            return improving_students.tolist()
        return None
    
    def avg_score_each_subject_across_semesters(self):
        if self.__df is not None:
            subject_avg = self.__df[
                ['Math', 'Physics', 'Chemistry', 'Biology', 'English']].mean()
            return subject_avg
        return None
    
    def overall_average_score_trend_across_semesters(self):
        if self.__df is not None:
            self.__df['Average_Score'] = self.__df[
                ['Math', 'Physics', 'Chemistry', 'Biology', 'English']].mean(axis=1)
            return self.__df.groupby('Semester')['Average_Score'].mean()
        return None
    