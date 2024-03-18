from preprocessing import Preprocessing
from inference import SemanticSegmentation
from post_segmentation_script import PostProcessing
from measure import MeasureTree
from report_writer import ReportWriter
import glob
import tkinter as tk
import tkinter.filedialog as fd
import os
from datetime import datetime


def FSCT(
    parameters,
    preprocess=True,
    segmentation=True,
    postprocessing=True,
    measure_plot=True,
    make_report=False,
    clean_up_files=False,
):
    print("Current point cloud being processed: ", parameters["point_cloud_filename"])
    if parameters["num_cpu_cores"] == 0:
        print("Using default number of CPU cores (all of them).")
        parameters["num_cpu_cores"] = os.cpu_count()
    print("Processing using ", parameters["num_cpu_cores"], "/", os.cpu_count(), " CPU cores.")

    if preprocess:
        print(datetime.now().strftime("%H:%M:%S")) 
        preprocessing = Preprocessing(parameters)
        preprocessing.preprocess_point_cloud()
        del preprocessing

    if segmentation:
        print(datetime.now().strftime("%H:%M:%S")) 
        sem_seg = SemanticSegmentation(parameters)
        sem_seg.inference()
        del sem_seg

    if postprocessing:
        print(datetime.now().strftime("%H:%M:%S")) 
        object_1 = PostProcessing(parameters)
        object_1.process_point_cloud()
        del object_1

    if measure_plot:
        print(datetime.now().strftime("%H:%M:%S")) 
        measure1 = MeasureTree(parameters)
        measure1.run_measurement_extraction()
        del measure1

    if make_report:
        print(datetime.now().strftime("%H:%M:%S")) 
        report_writer = ReportWriter(parameters)
        report_writer.make_report()
        del report_writer

    if clean_up_files:
        print(datetime.now().strftime("%H:%M:%S")) 
        report_writer = ReportWriter(parameters)
        report_writer.clean_up_files()
        del report_writer


def directory_mode():
    root = tk.Tk()
    point_clouds_to_process = []
    directory = fd.askdirectory(parent=root, title="Choose directory")
    unfiltered_point_clouds_to_process = glob.glob(directory + "/**/*.las", recursive=True)
    for i in unfiltered_point_clouds_to_process:
        if "FSCT_output" not in i:
            point_clouds_to_process.append(i)
    root.destroy()
    return point_clouds_to_process


def file_mode():
    root = tk.Tk()
    print(datetime.now().strftime("%H:%M:%S")) 
    point_clouds_to_process = fd.askopenfilenames(
        parent=root, title="Choose files", filetypes=[("LAS", "*.las"), ("LAZ", "*.laz"), ("CSV", "*.csv")]
    )
    root.destroy()
    return point_clouds_to_process
