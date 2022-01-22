from ovito.io import *
from ovito.modifiers import *
from ovito.pipeline import *
from ovito.io import import_file, export_file
from ovito.modifiers import CalculateDisplacementsModifier
import numpy

# Load input data and create a data pipeline.
pipeline = import_file(r'Path_to_xyz_file\filename.xyz', multiple_frames = True)

# Wrap at periodic boundaries:
pipeline.modifiers.append(WrapPeriodicImagesModifier())

# Displacement vectors:
pipeline.modifiers.append(CalculateDisplacementsModifier())

# Define the custom modifier function:
def modify(frame, data):

    # Access the per-particle displacement magnitudes computed by the 
    # CalculateDisplacementsModifier that precedes this user-defined modifier in the 
    # data pipeline:
    displacement_magnitudes = data.particles['Displacement Magnitude']
    particle_types = data.particles['Particle Type']
    
    # Compute MSD:
    msd = numpy.sum(displacement_magnitudes ** 2) / len(displacement_magnitudes)
    msd1 = numpy.mean(displacement_magnitudes[particle_types == 1]**2)
    msd2 = numpy.mean(displacement_magnitudes[particle_types == 2]**2)
    msd3 = numpy.mean(displacement_magnitudes[particle_types == 3]**2)
    msd4 = numpy.mean(displacement_magnitudes[particle_types == 4]**2)
    
    # Output MSD value as a global attribute: 
    data.attributes["MSD"] = msd
    data.attributes["MSD Type 1"] = msd1
    data.attributes["MSD Type 2"] = msd2
    data.attributes["MSD Type 3"] = msd3
    data.attributes["MSD Type 4"] = msd4
    print(msd, msd1, msd2, msd3, msd4)

# Insert user-defined modifier function into the data pipeline.
pipeline.modifiers.append(modify)

# Export calculated MSD value to a text file and let OVITO's data pipeline do the rest:
export_file(pipeline, r"Path_to_save_file\msd_filename.txt", 
    format = "txt/attr",
    columns = ["MSD", "MSD Type 1", "MSD Type 2", "MSD Type 3", "MSD Type 4"],
    multiple_frames = True)