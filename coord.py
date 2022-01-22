from ovito.io import import_file, export_file
import numpy as np
from ovito.io import *
from ovito.modifiers import *
from ovito.pipeline import *

# Load input data and create a data pipeline.
pipeline = import_file('path_to_file/filename.xyz', multiple_frames = True)

# Select type:
pipeline.modifiers.append(SelectTypeModifier(types = {1, 4}))

# Coordination analysis:
pipeline.modifiers.append(CoordinationAnalysisModifier(
    cutoff = 2.84, # bond length 
    number_of_bins = 100, 
    partial = True, 
    only_selected = True))

# def modify(frame, output):
#     ptypes = output.particles["Particle Type"] 
pipeline.modifiers.append(ExpressionSelectionModifier(expression ='ParticleType ==4 && Coordination==6'))
# print('Timestep', 'SelectExpression.num_selected') 

#export_file(pipeline,r"ate a data pipeline.
pipeline = export_file(pipeline, r"path_to_save_file\Zr6.txt", 'txt',
            columns = ['SelectExpression.num_selected'], 
            multiple_frames = True)
# data = pipeline.compute()