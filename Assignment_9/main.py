import os
from manage_data import ManageData
from visualizer import Visualizer
from config import SCRIPT_LOCATION, RESOURCES_DIR

def run():
    md = ManageData()
    visualizer = Visualizer()
    
    print("__ Following are the tasks that can be performed: __\n")
    while True:
        print("1. Get failed students")
        print("2. Get average scores per semester")
        print("3. Get the student with the highest average score")
        print("4. Get the subject with the lowest average score")
        print("5. Get students who are improving")
        print("6. Plot average score of each subject across semesters")
        print("7. Plot overall average score trend across semesters")
        print("8. Exit")
        
        choice = input("Enter the number corresponding to the task you want to perform: ")
        
        match choice:
            case '1':
                failed_students = md.get_failed_students()
                if failed_students is not None:
                    if len(failed_students) > 50:
                        print("\nNumber of failed students is large. Choose option:")
                        print("    1. Print all failed students anyway!")
                        print("    2. Print only the first 50 failed students.")
                        print("    3. Save failed students to a file.")
                        print("    4. Skip")
                        
                        while True:
                            choice_of_choice_one = input("    Enter the number corresponding to the option you want to choose: ")
                            
                            match choice_of_choice_one:
                                case '1':
                                    print(f"    Printing all {len(failed_students)} failed students:")
                                    print_students(failed_students)
                                    break
                                case '2':
                                    print("    Printing only the first 50 failed students:")
                                    print_students(failed_students[:50])
                                    break
                                case '3':
                                    print("    Saving failed students to a file.")
                                    save_students_to_file(failed_students, 'failed_students')
                                    print("    Failed students saved to /resources/'failed_students.txt'.")
                                    break
                                case '4':
                                    print("    Skipping...")
                                    break
                                case _:
                                    print("    Invalid choice.")
                                    break
                        print()
                    else:
                        print("\nFailed students:")
                        print_students(failed_students)          
                else:
                    print("Error: No data available.")
            
            case '2':
                avg_scores_per_semester = md.get_avg_scores_per_semester()
                if avg_scores_per_semester is not None:
                    print("\nAverage scores per semester:")
                    print(avg_scores_per_semester)
                    print("\nAverage scores per semester saved to /resources/'average_scores_per_semester.xlsx'.")
                else:
                    print("Error: No data available.")
                print()
            
            case '3':
                student = md.get_highest_avg_student()
                if student is not None:
                    print(f"\n   - Student with the highest average score: {student}")
                else:
                    print("Error: No data available.")
                print()
            
            case '4':
                subject = md.get_lowest_avg_subject()
                if subject is not None:
                    print(f"\n   - Subject with the lowest average score: {subject}")
                else:
                    print("Error: No data available.")
                print()
            
            case '5':
                improving_students = md.get_improving_students()
                if improving_students is not None:
                    print("\nImproving students:")
                    if len(improving_students) > 50:
                        print("\nNumber of improving students is large. Choose option:")
                        print("    1. Print all improving students anyway!")
                        print("    2. Print only the first 50 improving students.")
                        print("    3. Save improving students to a file.")
                        print("    4. Skip")
                        
                        while True:
                            choice_of_choice_five = input("    Enter the number corresponding to the option you want to choose: ")
                            
                            match choice_of_choice_five:
                                case '1':
                                    print(f"    Printing all {len(improving_students)} improving students:")
                                    print_students(improving_students)
                                    break
                                case '2':
                                    print("    Printing only the first 50 failed students:")
                                    print_students(improving_students[:50])
                                    break
                                case '3':
                                    print("    Saving failed students to a file.")
                                    save_students_to_file(improving_students, 'improving_students')
                                    print("    Improving students saved to /resources/'improving_students.txt'.")
                                    break
                                case '4':
                                    print("    Skipping...")
                                    break
                                case _:
                                    print("    Invalid choice.")
                                    break
                        print()
                    else:
                        print("\nImproving students:")
                        print_students(improving_students)
                else:
                    print("Error: No data available.")
        
            case '6':
                print("\n    Plotting average score of each subject across semesters...")
                visualizer.plot_avg_score_each_subject_across_semesters(save_plot=save_plot())
                
                
            case '7':
                print("\n    Plotting overall average score trend across semesters...")
                visualizer.plot_overall_average_score_trend_across_semesters(save_plot=save_plot())
            
            case '8':
                print("Exiting...")
                break
            
            case _:
                print("Invalid choice.")
                print()


def save_students_to_file(students, file_name):
    if not os.path.exists(RESOURCES_DIR):
        os.makedirs(RESOURCES_DIR)
    with open(f'{SCRIPT_LOCATION}/resources/{file_name}.txt', 'w') as f:
        for student in students:
            f.write(student + '\n')

def print_students(students):
    for i, student in enumerate(students):
        print("    ", i+1, " - ", student)

def save_plot():
    print("    1. Save and show plot")
    print("    2. Skip and show plot")
    choice = input("    Enter the number corresponding to the option you want to choose: ")
    if choice == '1':
        print("    Plot saved to /plots/.")
        return True
    print("    Skipping...")
    return False
        
if __name__ == '__main__':
    run()
        