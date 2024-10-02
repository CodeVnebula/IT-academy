import os
import matplotlib.pyplot as plt
from manage_data import ManageData
from config import SCRIPT_LOCATION, PLOTS_DIR

class Visualizer:
    def __init__(self):
        self.__md = ManageData()
        self.__plot_png_loc = '{}/plots/{}.png'
    
    def plot_avg_score_each_subject_across_semesters(self, save_plot=False):
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        avg_scores_of_each_subj = self.__md.avg_score_each_subject_across_semesters()
        avg_scores_of_each_subj.plot(kind='bar', figsize=(8, 5), color=colors)
        plt.title('Average Score of Each Subject Across All Semesters')
        plt.ylabel('Average Score')
        plt.xlabel('Subject')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_plot:
            self.save_plot_to_png('avg_score_each_subject_across_semesters')
        
        plt.show()
        
    def plot_overall_average_score_trend_across_semesters(self, save_plot=False):
        avg_score_trend = self.__md.overall_average_score_trend_across_semesters()
        avg_score_trend.plot(kind='line', marker='o', figsize=(8, 5), color='#1f77b4')
        plt.title('Overall Average Score Trend Across Semesters')
        plt.ylabel('Average Score')
        plt.xlabel('Semester')
        plt.xticks(rotation=0)
        plt.grid(True)
        plt.tight_layout()
        
        if save_plot:
            self.save_plot_to_png('overall_average_score_trend_across_semesters')
        
        plt.show()
        
    def save_plot_to_png(self, plot_name):
        if not os.path.exists(PLOTS_DIR):
            os.makedirs(PLOTS_DIR)
        plt.savefig(self.__plot_png_loc.format(SCRIPT_LOCATION, plot_name))
        