#!/usr/bin/env python
#
# Raccoon
#
# Tk Virtual Screening Interface for AutoDock
#
# v.1.0.0  Stefano Forli
#
# Copyright 2009, Molecular Graphics Lab
# 	The Scripps Research Institute
#
#
#################################################################
#
# Hofstadter's Law: It always takes longer than you expect,
#                   even when you take Hofstadter's Law 
#                   into account.
#
#	The Guide is definitive. Reality is frequently inaccurate.
#		Douglas Adams 
#
#################################################################
#
#     This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
#

version = "1.0  "


# enable the Debug mode by setting this to "True"
DEBUG = False

import glob
import os
from Tkinter import *
from tkFileDialog   import askopenfilename, askdirectory, asksaveasfilename
import tkMessageBox
import Pmw
import Tkinter 
import tarfile
import zipfile
import platform
import shutil # for shutil.copy2
import string
import datetime
from base64 import b64decode
from random import sample # potentially useless
from random import choice
from numpy import sqrt

try:
	# MolKit stuff
	# from the prepare_ligand code
	from MolKit import Read
	from AutoDockTools.MoleculePreparation import AD4LigandPreparation, AD4ReceptorPreparation, AD4FlexibleReceptorPreparation
	
	# from the prepare_gpf code
	from AutoDockTools.GridParameters import GridParameters, grid_parameter_list4
	from AutoDockTools.GridParameters import GridParameter4FileMaker
	from AutoDockTools.atomTypeTools import AutoDock4_AtomTyper

	

	# from the prepare_flexres code
	from MolKit.protein import ProteinSet, ResidueSet
	from MolKit.molecule import BondSet
	from MolKit.stringSelector import CompoundStringSelector
	
	from AutoDockTools.MoleculePreparation import AD4FlexibleReceptorPreparation
except:
	#print "I'm sorry, MolKit is required for running Raccooon"	
	tkMessageBox.showerror("MolKit error!", ("Impossible to find the MolKit module.\n\nMGLTools is required to run Raccoon but is either \
misconfigured or not installed.\n\nPlease install it, or try to run Raccoon with:\n\n $MGLROOT/bin/pythonsh raccoon.py"))
	exit(1)	

try:
	# from the prepare_dpf code
	from AutoDockTools.DockingParameters import DockingParameters, genetic_algorithm_list4_2, \
	                genetic_algorithm_local_search_list4_2, local_search_list4_2,\
	                simulated_annealing_list4_2
except:
	tkMessageBox.showerror("MGL Tools error!", ("Raccoon needs a version of MGLTools\n\n>= 1.5.4."))
	exit(1)


LOGO_BASE64='''\
R0lGODlhXgFFAPcAAAAAAA4ODg8BABIAAB4AABEPEBERERsbGw8NEB8hICIAAC4AAjAAAT0AAC0b
GiIiIiwsLCcpKDIyMjw8PC4wLyEfIEEAAE4AAFcAAWYAAXEAAHsCA1cvLUA+QUJCQkxMTEZIR1JS
UlxcXFdZWFBQT19gYmJiYmtra2lpZXFwbnJycnx8fHl5dW5vb2BgXjtO+TtS7TpV6ztT9TRL60JM
/EJZ7ERV8kRU/URa/UlV9UpV/EtZ9Uxa+kRZ81Jb/FRa+0ti/U1p/Epj9VNj/lNq/Vps/lhl+VRx
/lxz/V16/lJm7mF0/mN7/Wp8/mZy93J8/GNp/3+AgmWB/WuE/W6I/XOF/XOL/XmO/nqG9nuT/XeS
/YQBAZcAAJUyMqkAAKkWFrQAALsBAboJCrUXFqolJac2N7MoKLQyMrk2Nq0wL65AP5dVVpBxcqpG
RqtWVbRISLdXVrNQT7FgXKdoZ6V6ebpjY7p5ebdvb8IAAcwAAcgJCckZGNQAAdsAAdoLC9kJCdYQ
DtQUE9MYF9MNEM8eIcE6OdIiIuMBAesAAOAHCPIAAP0AAP4ODv8SEc8gHcNWVspmZtF5eNpVVoB/
grt/gYGAfoGBgYyMjIeHiJOTk5ycnJyWlZKOjp+goqSbmreHh7SPj6KgnaOjo6ysrKinp7Snp7Gu
sLOzs729vbi4uK6vsJ6gn4SL+oWa/Yqc/YaU/ZKd/pWY/Yyi/pOj/puk/pur/pam+J6y/L6+waOr
/ams/qSm/KOy/auz/q26/Ki197S7/bm9/LC1/b3AwLzF+7zK/bbC+7/Q/sSHh9GQkMimp8S5uNax
s+Kur8agn8TDv8PCw8vLy8jHxs7Qzc/Q0tHNzdrFwtDRztPT09vb29fX18/O08PL/MrN/cLF/MzS
/cvU+tLV/dTZ/Nrc/dDV9d7f4d7g3tzh/dTh/t/g4uPc2+jFxuDf7+Hh3uPj4+zr7Ofn6OLk/OXp
/ers/O3w7uzx/evy+PDu7vDu9fDw7fPz8/P0/fX5/Pn2+/7+/vj49iH5BAAAAAAALAAAAABeAUUA
AAj+AP0JHEiwoMGDBvshXMiwocOHECNKnEixosWLGDNq3Mhx4j+CHwuGPDiyo8mTKFOqXMmypUuN
JV/KnEmzps2bDRXWPPeNG7hz9vbx+1gyJs6jSJMqhejO3TudK/W9m6oPqktwtWrdusXLWLGv6OrV
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
'''

# System identification
system_info = platform.uname()
if DEBUG: print system_info
system = system_info[0]


root = Tk()
root.title('Raccoon | AutoDock VS')
Pmw.initialise()

nb = Pmw.NoteBook(root)
p1 = nb.add('Ligand(s)')
p2 = nb.add('Receptor(s)')
p3 = nb.add('Maps')
p4 = nb.add('Docking')
p5 = nb.add('VS Generation')
nb.pack(padx=3, pady=5, fill=BOTH, expand=1)


# Font settings
## Courier-related settings
if system == "Windows":
	courier = "Courier New"
	courier_size = "6"
	cygwin = BooleanVar()
	cygwin.set(False)
else:
	courier = "Courier"
	courier_size = "9"

courier_style = "roman"

# For the hand-breake function
StopImmediately = BooleanVar()
StopImmediately.set(False)

receptorFileList = []
DirJournal = []

# Ligand preparation options

# AutoDock atom type list
# 	this dictionary is updated with the atom types found
# 	in the selected ligands, and used to evaluate dir's
#	of cached maps
## Warning: atomic weights are inaccurate and there
#           is no account for merged non-polar H's
#
#
# TODO check for more accurate atomic weights

AtypeList = {   # count  MW
		'H'      : [ 0,  1    ],
		'HD'     : [ 0,  1    ],
		'HS'     : [ 0,  1    ],
		'C'      : [ 0,  12   ],
		'A'      : [ 0,  12   ],
		'N'      : [ 0,  14   ],
		'NA'     : [ 0,  14   ],
		'NS'     : [ 0,  14   ],
		'OA'     : [ 0,  16   ],
		'OS'     : [ 0,  16   ],
		'F'      : [ 0,  19   ],
		'Mg'     : [ 0,  24   ],
		'MG'     : [ 0,  24   ],
		'P'      : [ 0,  31   ],
		'SA'     : [ 0,  32   ],
		'S'      : [ 0,  32   ],
		'Cl'     : [ 0,  35.4 ],
		'CL'     : [ 0,  35.4 ],
		'Ca'     : [ 0,  40   ],
		'CA'     : [ 0,  40   ],
		'Mn'     : [ 0,  55   ],
		'MN'     : [ 0,  55   ],
		'Fe'     : [ 0,  56   ],
		'FE'     : [ 0,  56   ],
		'Zn'     : [ 0,  65.4 ],
		'ZN'     : [ 0,  65.4 ],
		'Br'     : [ 0,  80   ],
		'BR'     : [ 0,  80   ],
		'I'      : [ 0, 126   ],
		'e'      : [ 1,   0   ], # always 1 by default
		'd'      : [ 1,   0   ]  # always 1 by default
		}

# The Great Book of Ligands
LigandDictionary = {}
# its general structure is:
# {'filename' : {
#		"Atypes"	: list
#		"TORSDOF"	: int
#		"HbD"		: int
#		"HbA"		: int
#		"MW"		: float
#		"Nat"		: int
#		"NotStdAT"	: bool
#		"accepted"	: bool }
#		}

ResidueRotatableBondTable = {
		'GLY'	: [ 0, [""] ],
		'ALA'	: [ 0, [""] ],
		'PRO'	: [ 0, [""] ],
		'VAL'	: [ 1, ["C"] ],
		'LEU'	: [ 2, ["C"] ],
		'SER'	: [ 2, ["C", "OA", "HD"] ],
		'THR'	: [ 2, ["C", "OA", "HD"] ],
		'CYS'	: [ 2, ["C", "SA", "HD"] ],
		'ASN'	: [ 2, ["", "", ""] ],
		'PHE'	: [ 2, ["A", "C"] ],
		'TRP'	: [ 2, ["C", "A", "N", "HD"] ],
		'HIE'	: [ 2, ["C", "A", "NA", "N", "HD"] ],
		'HIS'	: [ 2, ["C", "A", "NA", "N", "HD"] ],
		'ASP'	: [ 2, ["C", "OA"] ],
		'ILE'	: [ 2, ["C"] ],
		'GLN'	: [ 3, ["C", "OA","N","HD"] ],
		'TYR'	: [ 3, ["C", "A", "OA", "HD"] ],
		'GLU'	: [ 3, ["C", "OA"] ],
		'MET'	: [ 3, ["C", "S"] ],
		'ARG'	: [ 4, ["C", "N", "HD"] ],
		'LYS'	: [ 5, ["C", "N", "HD"] ] }

# Filtering preview labels
TotalNumberLigandsMsg = StringVar()
TotAcceptedLigandsMsg = StringVar()
TotRejectedLigandsMsg = StringVar()
TotalAcceptedLigands = IntVar()


AutoDockMaxTORSDOF = IntVar()
AutoDockMaxTORSDOF.set(32)

FlexResTORSDOF = IntVar()
FlexResTORSDOF.set(0)
FlexResTypes = []

seriously = BooleanVar() # filtering or just previewing
DoRejectATypes = BooleanVar()
DoRejectATypes.set(True)
HbDmin = IntVar() # HydBond DONOR 
HbDmin.set(0)   
HbDmax = IntVar()
HbDmax.set(99)
HbAmin = IntVar() # HydBond ACCEPTOR
HbAmin.set(0)   
HbAmax = IntVar()
HbAmax.set(99)
MWmin = IntVar()   # Molecular weight
MWmin.set(0)
MWmax = IntVar()
MWmax.set(9999)
NatMin = IntVar() # Number of heavy atoms
NatMin.set(0) 
NatMax = IntVar()
NatMax.set(999)
TORSDOFmin = IntVar()
TORSDOFmin.set(0)
TORSDOFmax = IntVar()
TORSDOFmax.set(32)
FilterSet = StringVar()
FilterSet.set("Default")

# Grid settings
AutoGridBin = StringVar()
AutoGridBin.set("")
GPFkeywords = [
		'npts',  
		'parameter_file',
		'gridfld',
		'spacing',
		'receptor_types',
		'ligand_types',
		'receptor',
		'gridcenter',
		'smooth',
		'map',
		'elecmap',
		'dsolvmap',
		'dielectric'
		]

mapDir = None # The path of the cached maps

GPFParameterFile = StringVar()
DPFParameterFile = StringVar()

DPFkeywords = [
		'autodock_parameter_version',
		'outlev',
		'parameter_file',
		'intelec',
		'seed',
		'ligand_types',
		'fld',
		'map',
		'elecmap',
		'desolvmap',
		'move',
		'about',
		'axisangle0',
		'tran0',
		'quat0',
		'dihe0',
		'ndihe',
		'tstep',
		'qstep',
		'dstep',
		'torsdof',
		'unbound',
		'rmstol',
		'extnrg',
		'e0max',
		'ga_pop_size',
		'ga_num_evals',
		'ga_num_generations',
		'ga_elitism',
		'ga_mutation_rate',
		'ga_crossover_rate',
		'ga_window_size',
		'ga_cauchy_alpha',
		'ga_cauchy_beta',
		'output_pop_file',
		'set_ga',
		'sw_max_its',
		'sw_max_succ',
		'sw_max_fail',
		'sw_rho',
		'sw_lb_rho',
		'ls_search_freq',
		'set_sw1',
		'set_psw1',
		'ga_run',
		'analysis'
		]


# Default DPF
default_docking_parameter_file = """autodock_parameter_version 4.2       # used by autodock to validate parameter set
outlev 1                             # diagnostic output level
intelec                              # calculate internal electrostatics
seed pid time                        # seeds for random generator
ligand_types HD OA                   # atoms types in ligand
fld receptor.maps.fld                # grid_data_file
map receptor.HD.map                  # atom-specific affinity map
map receptor.OA.map                  # atom-specific affinity map
elecmap receptor.e.map               # electrostatics map
desolvmap receptor.d.map             # desolvation map
move ligand.pdbqt                    # small molecule
about 0.378 0.6623 0.648             # small molecule center
tran0 random                         # initial coordinates/A or random
axisangle0 random                    # initial orientation
dihe0 random                         # initial dihedrals (relative) or random
tstep 2.0                            # translation step/A
qstep 50.0                           # quaternion step/deg
dstep 50.0                           # torsion step/deg
torsdof 0                            # torsional degrees of freedom
rmstol 2.0                           # cluster_tolerance/A
extnrg 1000.0                        # external grid energy
e0max 0.0 10000                      # max initial energy; max number of retries
ga_pop_size 150                      # number of individuals in population
ga_num_evals 2500000                 # maximum number of energy evaluations
ga_num_generations 27000             # maximum number of generations
ga_elitism 1                         # number of top individuals to survive to next generation
ga_mutation_rate 0.02                # rate of gene mutation
ga_crossover_rate 0.8                # rate of crossover
ga_window_size 10                    # 
ga_cauchy_alpha 0.0                  # Alpha parameter of Cauchy distribution
ga_cauchy_beta 1.0                   # Beta parameter Cauchy distribution
set_ga                               # set the above parameters for GA or LGA
sw_max_its 300                       # iterations of Solis & Wets local search
sw_max_succ 4                        # consecutive successes before changing rho
sw_max_fail 4                        # consecutive failures before changing rho
sw_rho 1.0                           # size of local search space to sample
sw_lb_rho 0.01                       # lower bound on rho
ls_search_freq 0.06                  # probability of performing local search on individual
set_psw1                             # set the above pseudo-Solis & Wets parameters
unbound_model bound                  # state of unbound ligand
ga_run 10                            # do this many hybrid GA-LS runs
analysis                             # perform a ranked cluster analysis"""


# Ligand Import default options
LigandListLabel = StringVar()
LigandListLabel.set('Import ligands...')

# PrepareLigand options defaults
ChargeSet = StringVar()
ChargeSet.set("gasteiger")
Repair = StringVar()
Repair.set("")
Cleanup = StringVar()
Cleanup.set("nphs_lps")
BackboneRotatable = BooleanVar()
BackboneRotatable.set(True)
AmideRotatable = BooleanVar()
AmideRotatable.set(False)
GuanidiniumRotatable = BooleanVar()
GuanidiniumRotatable.set(False)
LargestFrag = BooleanVar()
LargestFrag.set(False)
AttachFrag = BooleanVar()
AttachFrag.set(False)
LockTors = BooleanVar()
LockTors.set(False)

LIGAND_SET = False # define if ligand filenames have been set

#### Receptor options

# default receptor structure multiplicity (one/many)
TargetPDBQT = StringVar()
RCstatus = IntVar()
RCstatus.set(0) # Initial option is "single conformation
RecFilename = StringVar()
RecFilename.set("[ none ]")

# Variables defining if either the single or the multiple receptor
# conformations have been defined
SingleReceptorSet = BooleanVar()
SingleReceptorSet.set(False)
MultiReceptorSet = BooleanVar()
MultiReceptorSet.set(False)

RecChargeSet = StringVar()
RecChargeSet.set('gasteiger')

RecCleanNPH = StringVar()
RecCleanNPH.set("_nphs")
RecCleanLP = StringVar()
RecCleanLP.set("_lps")
RecCleanWAT = StringVar()
RecCleanWAT.set("_waters")
RecCleanStdRes = BooleanVar()
RecCleanStdRes.set(False) 
RecDelAlternate = StringVar()
RecDelAlternate.set("")
RecRepairOptionsSet = StringVar()
RecRepairOptionsSet.set("add H (if missing)")

# default flexible residues (y/n)
FlexResDefined = BooleanVar()
DoFlex = IntVar()
DoFlex.set(0)
DoFlexFromWhat = IntVar()
DoFlexFromWhat.set(-1) # values are 1 for "from file" and 2 "from selection"
FlexResFileName = StringVar()
FlexResFileName.set("")
ResidueStatusLoaded = StringVar()
ResidueStatusSelected = StringVar()
ResidueStatusLoaded.set("")
ResidueStatusSelected.set("")
ResidueStatus = StringVar()
ListFlexResiduesNames = StringVar()
FlexResSelected = StringVar()


### AutoGrid options
AutoGridWhen1, AutoGridWhen2, AutoGridWhen3 = None, None, None
GPFfilename = StringVar()
GPFfilename.set("[ no GPF loaded ]")
CacheMapDirName = StringVar()
CacheMapDirName.set("[ none ]")
mapFileList = []
MapSource = IntVar()
MapSource.set(0)
CacheMapPolicy = StringVar()

CacheMapFrame, GPFframe, CacheMapHandleNow, CacheMapHandle = None, None, None, None

# values for DoCachedMaps
# 0 : no maps defined
# 1 : maps defined and checked
DoCachedMaps = BooleanVar()


# Docking menu params
dockMenuSettings = None
DPFfilename = StringVar()
DPFfilename.set("[ no DPF loaded ]")
DPFedit, DPFcontent = None, None


# Docking/DPF default settings 
DPFgroupTemplate, DPFgroupSimple, DPFgroupSmart, DPFgroupTemplate, DPFgroupComplex = None, None, None, None, None

DPF_group = None
DPF_INFO = None
InfoFrame = None
DockMenuSetting = None
DPFSpeed = IntVar()

Info = None
numGen = None
EnEval = None
simple_settings = None
simple_settings_info = None
EnEval = None
OpenDPF = None
docking_set = None
CheckTDOF = None
CheckVOL = None
complex_gen_info = None
complex_eval_info = None

# Final destination directory
JobDirectory = StringVar()
JobDirectory.set("")
JobDirectoryInfo = StringVar()
JobDirectoryInfo.set("")

# System options
TargetOS = StringVar()
TargetOS.set("lin")
LinuxScriptLevel = StringVar()
LinuxScriptLevel.set("master script for starting the VS")
PBStime = StringVar()
PBStime.set("24:00:00")
PBShowmanyruns = IntVar()
PBShowmanyruns.set(1)
TarFile = StringVar()
TarFile.set('[disabled]')

# Load session defaults
LoadLig = BooleanVar()
LoadLig.set(True)
LoadFilter = BooleanVar()
LoadFilter.set(True)
LoadRec = BooleanVar()
LoadRec.set(True)
LoadFlex = BooleanVar()
LoadFlex.set(True)
LoadMap = BooleanVar()
LoadMap.set(True)
LoadDock = BooleanVar()
LoadDock.set(True)
LoadGen = BooleanVar()
LoadGen.set(True)


# Save session defaults
SaveLig = BooleanVar()
SaveLig.set(True)
SaveFilter = BooleanVar()
SaveFilter.set(True)
SaveRec = BooleanVar()
SaveRec.set(True)
SaveFlex = BooleanVar()
SaveFlex.set(True)
SaveMap = BooleanVar()
SaveMap.set(True)
SaveDock = BooleanVar()
SaveDock.set(True)
SaveGen = BooleanVar()
SaveGen.set(True)


RecStatus = "[ not yet selected ]"

# Summary page variables
LigandSummary = StringVar()
ReceptorSummary = StringVar()
MapsSummary = StringVar()
DockingSummary = StringVar()
JobsSummary = StringVar()

LigandSummary.set(( " [ none ] "))
ReceptorSummary.set( " [ none ] " )
MapsSummary.set((" [ none ] "))
DockingSummary.set(" [ none ] ")
JobsSummary.set(" ")

def InfoInit():
	global InfoMessage, InfoBar, InfoText
	# Initialize the info-bar at the bottom of the root
	InfoMessage = StringVar()
	InfoText = Label(root, textvariable = InfoMessage, font=("Helvetica", 10))
	InfoText.pack(padx = 2, pady = 2, expand='no', fill='x')
	InfoMessage.set('Welcome to Raccoon | AutoDock VS')

def raccoon():
	data = [
		"UilvYnVzdCBBKXV0b0RvY2sgQyloZW1pY2FsIEMpb21wb3VuZCBPKXJnYW5pemF0aW9uIGFuZCBPKXB0aW1pemF0aW9uIE4pb3RlYm9vaw==",
		"Uil1bm5pbmcgQSlmdGVyIEMpaGVtaWNhbCBDKWhpbWVyYXMgTyl2ZXIgTylic2N1cmUgTilpbWJp",
		"UilvbWFudGljbHkgQSlkZGljdGVkIEMpYWxjdWxhdGlvbnMgQylhcmVmdWxseSBPKWZmZXJpbmcgTylwZW5pbmcgTilvdmVsdGllcw==",
		"UilhcGlkIEEpdXRvbWF0aWMgQylyZWF0aW9uIG9mIEMpbHVzdGVycyBPKWNjYXNpb25hbGx5IE8pYnNlcnZlZCBpbiBOKWF0dXJl",
		"UilldHVybmluZyBBKWJyb3VwdGx5IGEgQyktc2hlbGwgQylvbW1hbmQgTyl1dHB1dCBPKXBlcmF0aXZlbHkgTil1bGxpZmllZA==",
		"UillZnJhaW4gQSlic3RydXNlIEMpb21tb24gQylvbXB1dGF0aW9ucyBPKWZ0ZW4gTylwZXJhdGlvbmFsbHkgTilveGlvdXM=",
		"UillbGVhc2luZyBBKWxsZWdlZGx5IEMpcml0aWNhbCBDKW9tcHJlc3Npb25zIE8pdmVya2lsbHMgTylic3RydWN0ZWQgTillZWRz",
		"Uillc3RsZXNzIEEpbmltYWwgQylyYXZpbmcgQyloZW1pY2FscyBPKXV0IE8pZiBOKW93aGVyZQ==",
		"UilldHJpZXZpbmcgQSltYXppbmcgQylvbXBvdW5kcyBPKXZlcndoZWxtcyBPKXV0Y3J5aW5nIE4pdW1iZXJz",
		"Uil1biBBKXV0b2RvY2ssIEMpaGVjayBDKWx1c3RlcnMsIE8pYnNlcnZlLCBPKXJkZXIgYW5kIE4pb2Q=",
		"UilldmVhbGluZyBBKW5vdGhlciBDKW9tcG91bmQgQylhbiBPKWNjdXIgTyliZWRpZW50bHkgTilvdw==",
		"UilhY2Nvb24gQSl1dG9tYXRlIEMpb21wdXRhdGlvbmFsIEMpaGVtaXN0cnkgTylwZXJhdGlvbnMgTyluIE4pb2Rlcw==",
		"UillbWFyY2FibGUgQSljdGlvbnMgQylvbnN0YW50bHkgQyl1dCBPKWZmIE8pYm5veGlvdXMgTillZ290aWF0aW9ucw==",
		"UillZHVuZGFudCBBKWN0aW9ucyBDKWxlYXJseSBDKWF1c2UgTyl2ZXItcHJvZHVjdGlvbiBPKWYgTilvaXNl",
		"UilldmlldyBBKWxsIEMpb25zdGFudHMsIEMpaGVjayBPKXV0IE8pcHByZXNzZWQgTil1bWJlcnM=",
		"UillbWVtYmVyOiBBKW55IEMpb25jZXB0IEMpb3VsZCBPKXV0c3RhbmQuLi4gTylyIE4pb3Q="
		]
	return "\n"+b64decode(data[choice(range(0, len(data)))])+"\n"

def about():  

	GNU=""" This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
	"""

	logo = StringVar()
	logo.set("""          ________________________________________________________________ 

    __________//___________________________/////___________________/____________  
    _________/__/__________________________/____/__________________/____________  
    ________/____/___________/_____________/_____/_________________/____________  
    ________/____/__/_____/_/////___/////__/_____/__/////___/////__/___/________  
    _______/______/_/_____/__/_____/_____/_/_____/_/_____/_/_____/_/_//_________  
    _______////////_/_____/__/_____/_____/_/_____/_/_____/_/_______//_/_________  
    _______/______/_/____//__/___/_/_____/_/____/__/_____/_/_____/_/___/________  
    _______/______/__////_/___///___/////__/////____/////___/////__/____/_______  
 
          ________________________________________________________________
                                        ______ 
                                       /      \\ 
                                      /        \\ 
                                     /          \\  
                                     \\    /\\    / 
                                      \\  /  \\  / 
                                       \\/ /\\ \\/ 
                                        /\\  \\ 
                                      /\\  \\__\\ 
                                     /  \\__\\ 
                                    /____\\
						 
                        ______________________________________ 
                       |                                      |
                       |         Raccoon | AutoDock VS        |
                       |            version %4s             |
                       |              (c) 2009                |
                       |    The Scripps Research Institute    |
                       |                                      |
                       |          Stefano Forli, TSRI         |
                       |            Ruth Huey, TSRI           |
                       |______________________________________|""" % version )


	AboutWin = Toplevel(root)
	AboutWin.title("About Raccoon | AutoDockVS")
	AboutWin.winfo_toplevel().resizable(NO,NO)
	
	Label(AboutWin, textvar = logo, font = (courier, courier_size, ), justify = LEFT ).pack()
	Frame(AboutWin, height = 2, bd = 1, relief = SUNKEN).pack(fill = X, padx = 5 , pady = 3)
	Label(AboutWin, text = " "+raccoon()+" ", justify = LEFT, font = ('Courier', 10, 'bold')).pack()
	Frame(AboutWin, height = 2, bd = 1, relief = SUNKEN).pack(fill = X, padx = 5 , pady = 3)
	Label(AboutWin, text = "Manual pages and version updates could be *potentially* found at this address:", font = ('Helvetica', 9, 'roman')).pack()
	Label(AboutWin, text = "http://www.scripps.edu/~forli/").pack(padx = 5)
	Button(AboutWin, height = 2, text = "Close", command = lambda: AboutWin.destroy()).pack(fill = X, padx = 15, pady = 3, anchor = S, side = BOTTOM )
	return


def makemenu(win):
    top = Menu(win)       
    win.config(menu=top)
    
    file = Menu(top, tearoff=0)
    file.add_command(label='Load VS configuration...',command=LoadLogWindow, underline=0)
    file.add_command(label='Save VS configuration...',command=SaveLogWindow, underline=0)
    file.add_separator()
    file.add_command(label='Import ligand list file...',command=ImportLigList, underline=0)
    file.add_command(label='Export ligand list file...',command=ExportLigList, underline=0)
    file.add_separator()
    file.add_command(label='Quit', command=confirm, underline=0)
    top.add_cascade(label='File', menu=file, underline=0)

    setup = Menu(top, tearoff=0)
    setup.add_command(label='Split a MOL2', command=SplitMol2, underline=0)

    top.add_cascade(label='Utilities', menu=setup, underline=0)

    help = Menu(top, tearoff=0)
    help.add_command(label='About Raccoon', command=about, underline=0)
    top.add_cascade(label='Help', menu=help, underline=0)

def LoadLogWindow():
	def Done():
		LoadOptWin.destroy()
		LoadLog(logname)
	DisableInterface()
	logname = askopenfilename(parent = root, title = "Select a Raccoon log to load...", filetypes=[("Raccoon Log", "*.log")])
	if not logname:
		EnableInterface()
		return False
	DisableInterface()
	LoadOptWin = Toplevel(root)
	LoadOptWin.title("LOAD session")
	LoadOptWin.winfo_toplevel().resizable(NO,NO)
	Label(LoadOptWin, text = "Select data to be imported\nfrom the file:", justify = LEFT).grid(row = 1, column = 0, columnspan = 3, sticky = N, padx = 5, pady = 5)
	Checkbutton(LoadOptWin, text = "Ligands list", variable = LoadLig).grid(row = 2, column = 1, columnspan = 2, sticky = W)
	Checkbutton(LoadOptWin, text = "Filter set", variable = LoadFilter).grid(row = 3, column = 1, columnspan = 2, sticky = W, padx = 15)
	Checkbutton(LoadOptWin, text = "Receptors list", variable = LoadRec).grid(row = 4, column = 1, columnspan = 2, sticky = W)
	Checkbutton(LoadOptWin, text = "Flexible residues", variable = LoadFlex).grid(row = 5, column = 1, columnspan = 2, sticky = W, padx = 15)
	Checkbutton(LoadOptWin, text = "Map parameters", variable = LoadMap).grid(row = 6, column = 1, columnspan = 2, sticky = W)
	Checkbutton(LoadOptWin, text = "Docking parameters", variable = LoadDock).grid(row = 7, column = 1, columnspan = 2, sticky = W)
	Button(LoadOptWin, text = "OK", command = Done).grid(row = 10, column = 1, columnspan = 1, sticky = W, padx = 10, pady= 10)
	Button(LoadOptWin, text = "Cancel", command = lambda: LoadOptWin.destroy()).grid(row = 10, column = 2, sticky = W, padx = 10, pady= 10)
	EnableInterface()


def LoadLog(logname):
	# DEBUG = True
	if LoadLig.get() + LoadRec.get() + LoadFlex.get() + LoadMap.get() + LoadDock.get() + LoadGen.get() + LoadFilter.get() == 0:
			return
	logfile = open(logname, 'r').readlines()
	# Check that is an original Raccoon(TM) LogFile(TM)
	# with an advanced and sofisticated text scanning...
	raccoon, virtual, screening = False, False, False
	for line in logfile:
		if "Raccoon" in line:
			raccoon = True
		if "Virtual" in line:
			virtual = True
		if "Screening" in line:
			screning = True
	if raccoon:
		if virtual:
			if screening:
				pass
	else:
		tkMessageBox.showerror("Error!", ("The loaded file is not a Raccoon VS file"))
		return False
	if DEBUG: print logfile[-1]

	################################
	# Start importing all the params
	################################

	# Load the filters
	if LoadFilter.get():
		try:
			for index in range(38, 44):
				logfile[index] = logfile[index].rsplit() # clean up the line from space and \n's
				if DEBUG: print "LOAD_SESSION: filter params => ", logfile[index]
			# Hb donor max-min
			HbDmin.set(int(logfile[38][-3])), HbDmax.set(int(logfile[38][-1]))
			# Hb acceptor max-min
			HbAmin.set(int(logfile[39][-3])), HbAmax.set(int(logfile[39][-1]))
			# MW max-min
			MWmin.set(int(logfile[40][-3])), MWmax.set(int(logfile[40][-1]))
			# Nat max-min
			NatMin.set(int(logfile[41][-3])), NatMax.set(int(logfile[41][-1]))
			# TORSDOF max-min
			TORSDOFmin.set(int(logfile[42][-3])), TORSDOFmax.set(int(logfile[42][-1]))
			# Filter non-AD atom types
			if logfile[43][-1] == "True":
				DoRejectATypes.set(True)
			else:
				DoRejectATypes.set(False)
		except:
			tkMessageBox.showerror("Error!", ("Problems loading the filter settings."))
			if (tkMessageBox.askokcancel("Warning", ("Error while loading the filter settings.\nSkip loading filters and continue loading the log file?") == 0 )):
				return False
	
	if LoadRec.get():
		# Load the target structure
		receptor_list = []
		try:
			for line in logfile:
				if line[0:7] == "TARGET>":
					filename = line.split("TARGET>")[-1]
					filename = filename.strip()
					receptor_list.append(filename)
					if DEBUG: print "LOAD_SESSION> found receptor: |%s|" % receptor_list[0]
		except:
			tkMessageBox.showerror("Error!", ("Unable to load the receptor structure(s)."))
			return False
		if len(receptor_list) > 1:
			RCstatus.set(1)
			ReceptorOptions()
			try:
				openReceptor(receptor_list)
			except:
				if (tkMessageBox.askokcancel("Warning", ("Error while loading the receptor structures.\nSkip receptor loading and continue loading the log file?") == 0 )):
					return False

		elif len(receptor_list) == 1:
			RCstatus.set(0)
			ReceptorOptions()
			try:
				openSingleReceptor(receptor_list[0]) 
			except:
				if (tkMessageBox.askokcancel("Warning", (("Error while loading the receptor structure:\n %s\n\nSkip receptor loading and continue loading the log file?") % receptor_list[0]))) == 0:
					return False

	# Load flexible residues info		
	if LoadFlex.get():
		try:
			for line in logfile:
				if line[0:5] == "FLEX>":
					DoFlex.set(1)
					SetFlexibleMode() 
					# loaded from file
					if "file" in line:
						if DEBUG: print "LOAD_SESSION: got flex from file", line.split(":", 1)[1][:-1].split("\t")[1]
						DoFlexFromWhat.set(1)
						SetFlexibleResidueFile(line.split(":", 1)[1][:-1].split("\t")[1])
						break

					# generated from selection
					if "selection" in line:
						if DEBUG: print "LOAD_SESSION: got flex from selection", line.split(":", 1)[1][:-1]
						DoFlexFromWhat.set(2)
						ListFlexResiduesNames.set(line.split(":", 1)[1][:-1])
						ParseFlexSelection()
						break
		except:
			tkMessageBox.showwarning("Flexible residues", ("There is a problem in reading the flexible residues information."))

	# Load the GPF setup
	defer_map_check = False
	if LoadMap.get():
		# identify the grid mode
		mode = ""
		for line in logfile:
			if "Grid mode :" in line:
				mode = line.split(":")[1]
				break
		if DEBUG: print "LOAD_SESSION> the grid mode is |%s|"% mode
		if "calculated in each job" in mode:
			if DEBUG :print "	applying map mode 0"
			MapMenu()
			AutoGridWhen1.invoke() 
		if "calculated now" in mode:
			if DEBUG: print "	applying map mode 1"
			MapMenu()
			if not system == "Windows":
				AutoGridWhen2.invoke() 
			else:
				AutoGridWhen1.invoke()
		if "use pre-calculated" in mode:
			if DEBUG: print "	applying map mode 2 ( deferring map check)"
			defer_map_check = True
	
		# Cached maps policy
		if MapSource.get() >= 1 or defer_map_check:
			if ">copied<" in mode:
				CacheMapPolicy.set("Make copies [ use more disk space ]")
				if DEBUG: print "	set map policy to COPIES"
			if ">linked<" in mode:
				CacheMapPolicy.set("Make symbolic links [ save disk space ]")
				if DEBUG: print "	set map policy to LINKS"
	
		# load GPF if needed
		if MapSource.get() <= 1:
			GPFcontent.config(state = NORMAL)
			GPFcontent.delete(1.0, END) 
			for line in logfile:
				if line[0:4] == "GPF>":
					line = line.split('GPF>\t')[1]
					GPFcontent.insert(END, line)
					GPFfilename.set((" Grid parms from %s " % logname))
			GPFcontent.config(state = DISABLED)
			GPFedit.config(state = ACTIVE)
			setGPFtags()

		# get the autogrid binary specified if needed
		if MapSource.get() == 1:
			for line in logfile:
				if "AutoGrid binary file" in line:
					line = line.split("|")
					if not line[1] == "":
						if not GetAutoGrid(line[1]):
							if not (tkMessageBox.askokcancel("Warning", ("Unable to find the AutoGrid binary file specified\
in the log:\n\n%s\n\nSkip the binary specification and continue or cancel log loading?" % line[1]) == 0 )):
								return False
	if LoadDock.get():
		# Load the DPF setup
	
		# identify the docking mode
		for line in logfile:
			if "Docking mode :" in line:
				line = line.split(">")[1]
				mode = line.split("<")[0]
				break
	
		if mode == "generated from template" in mode:
			docking_set.set("From template...")
			docking_setup_interface(None)
			DPFcontent.config(state = NORMAL)
			DPFcontent.delete(1.0, END) 
			for line in logfile:
				if line[0:4] == "DPF>":
					line = line.split('DPF>\t')[1]
					DPFcontent.insert(END, line)
					DPFfilename.set((" Docking parms from %s " % logname))
			DPFcontent.config(state = DISABLED)
			DPFedit.config(state = ACTIVE)
			setDPFtags()

					# Add a check for parameter files specified here...
	
	if LoadLig.get():
		# Load the ligands
		ligand_list = []
		for line in logfile:
			if line[0:7] == "LIGAND>":
				line = line.rsplit("\n", 1)[0]
				ligand_list.append(line.split("LIGAND> ")[1])
		if len(ligand_list) >= 1:
			openLigand(ligand_list)

		# define the cached maps dir and test them (it needs to be done *after* ligands
		# have been imported to check if maps are missing)
		if defer_map_check:
			MapMenu()
			for line in logfile:
				if "Grid cache dir" in line:
					cache_dir = line.split("   Grid cache dir : ")[1][:-1]
					if DEBUG :
						print "    (Deferred map checking)	found cache dir : |%s|"% cache_dir
						print "    List of map files:"
						print glob.glob(os.path.join(cache_dir, "*map*"))
					opendirMaps(cache_dir)
			AutoGridWhen3.invoke() 
	InfoMessage.set("Log file loaded successfully")


def SaveLogWindow():
	DisableInterface()

	def Done():
		SaveOptWin.destroy()
		SaveLog(logname)
		return True

	keepasking = True
	while keepasking:
		logname = asksaveasfilename(parent = root, title = "Select the Raccoon log filename to save...", filetypes = [('Raccoon log file', '*.log'), ("Any file...", "*")] ,  defaultextension=".log") 
		if logname:
			if DEBUG: print "here I should save the file log..."
			InitializeLog(None, logname)
			EnableInterface()
			return True
		else:
			EnableInterface()
			return False

	DisableInterface()
	SaveOptWin = Toplevel(root)
	SaveOptWin.title("SAVE session")
	SaveOptWin.winfo_toplevel().resizable(NO,NO)
	Label(SaveOptWin, text = "Select data to be saved in the file:", justify = LEFT).grid(row = 1, column = 0, columnspan = 3, sticky = N, padx = 5, pady = 5)
	Checkbutton(SaveOptWin, text = "Ligands list", variable = SaveLig).grid(row = 2, column = 1, columnspan = 2, sticky = W)
	Checkbutton(SaveOptWin, text = "Receptors list", variable = SaveRec).grid(row = 3, column = 1, columnspan = 2, sticky = W)
	Checkbutton(SaveOptWin, text = "Flexible residues", variable = SaveFlex).grid(row = 4, column = 1, columnspan = 2, sticky = W, padx = 15)
	Checkbutton(SaveOptWin, text = "Map parameters", variable = SaveMap).grid(row = 5, column = 1, columnspan = 2, sticky = W)
	Checkbutton(SaveOptWin, text = "Docking parameters", variable = SaveDock).grid(row = 6, column = 1, columnspan = 2, sticky = W)
	Checkbutton(SaveOptWin, text = "Generation options", variable = SaveGen).grid(row = 7, column = 1, columnspan = 2, sticky = W)
	Button(SaveOptWin, text = "OK", command = Done).grid(row = 9, column = 1, columnspan = 1, sticky = W, padx = 10, pady= 10)
	Button(SaveOptWin, text = "Cancel", command = lambda: SaveOptWin.destroy()).grid(row = 9, column = 2, sticky = W, padx = 10, pady= 10)
	EnableInterface()



def SetJobDirectory(dir = None): 
	"""General opendir function useful for setting 
	the finaloutput dir
	"""
	dir_accepted = False
	if dir:
		DirName = dir
	else:
		while not dir_accepted:
			DirName = askdirectory()
			if DirName:
				try:
					if os.path.exists(DirName):
						if len(glob.glob(os.path.join(DirName, "*"))):
							if tkMessageBox.askyesno('Output directory','The selected directory is not empty.\nAre you sure you want to use it?'):
								dir_accepted = True
						else:
							dir_accepted = True
					else:
						if tkMessageBox.askokcancel('Output directory','The selected directory doesn\'t exist.\nDo you want to create it?'):
							os.makedirs(DirName, 0755)
							dir_accepted = True
					if dir_accepted:
						JobDirectory.set(DirName)
						JobDirectoryInfo.set(CheckDiskSpace(DirName))
						TheCheck()
						return
				except:
					tkMessageBox.showerror("Error!", ("The directory:\n%s\n is not accessible" % DirName))
					JobDirectory.set("")
					JobDirectoryInfo.set("")
					TheCheck()
					return
			else:
				TheCheck()
				return


def CheckDiskSpace(path):
	if system == "Windows": # Warning: cover your eyes 'cause this workaround is extremely ugly (...but works)
		if DEBUG: print "CHECKDISKSPACE> this is path", path
		dir_list = "dir \"%s\"" % path
		command = os.popen2(dir_list)
		output = command[1].readlines()
		if DEBUG: print "CHECKDISKSPACE> output", output
		diskspace = output[-1].split()[-3]
		if DEBUG: print "CHECKDISKSPACE> diskspace", diskspace
		available = str(diskspace.replace(".", "")) # total bytes (for EU support)
		available = str(diskspace.replace(",", "")) # total bytes (for USA support)


	elif system == "Linux" or system == "Darwin":
		disk = os.statvfs(path)
		capacity = disk.f_bsize * disk.f_blocks
		available = disk.f_bsize * disk.f_bavail
		used = disk.f_bsize * (disk.f_blocks - disk.f_bavail)
	else:
		return "[ disk space not available ]"

	if available > 1073741824:
		unit = " Gb"
		factor = 1073741824
	else:
		unit = " Mb"
		factor = 1048576

	calculated_space = "%5.2f" % (float(available)/float(factor))
	if DEBUG: print calculated_space
	available_space = "[ "+str(calculated_space)+unit+" available disk space ]" 
	return available_space

#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#### Ligand (p1) functions #####

def countLigands(): 
	verbose = False
	if verbose or DEBUG: print "this would be the dictionary lenght:", len(LigandDictionary)

	# If there are no ligands just return
	if len(LigandDictionary) < 1:
		LigandListLabel.set('Import ligands...')
		AutoGridWhen3.config(state = DISABLED)
		AutoGridWhen1.invoke()
		TotalAcceptedLigands.set(0)
		return

	# start counting...
	ligand_conscription = 0
	for item in LigandDictionary.keys():
		if LigandDictionary[item]["accepted"]:
			ligand_conscription += 1

	# choices
	if ligand_conscription < 1:
		tag = " Ligands accepted : %s / %s " % ( str(ligand_conscription), str(len(LigandDictionary)))
		LigandListLabel.set(tag)
		# Color the label by red...
		AutoGridWhen3.config(state = DISABLED)
		AutoGridWhen1.invoke()
		return


	else:
		tag = " Ligands accepted : %s / %s " % ( str(ligand_conscription), str(len(LigandDictionary)))
		LigandListLabel.set(tag)
		if RCstatus.get() == 0:
			if SingleReceptorSet.get():
				AutoGridWhen3.config(state = NORMAL)
		if RCstatus.get() == 1:
			AutoGridWhen3.config(state = NORMAL)
		return


def openLigand(ligFile = None): # Now unified loader for all the supported formats
	# The input is a list
	got_some = False
	if not ligFile:
		ligFile = askopenfilename(parent = root, title = "Select one or more PDBQT, PDB or (multi)MOL2", filetypes=[("Ligand PDBQT", "*.pdbqt"), ("PDB", "*.pdb"), ("Mol2", "*.mol2"), ("Any file type...", "*")], multiple = 1)
	if ligFile:
		# now any filter can be applied in the openfilename interface ("*" included)
		pdb_list, pdbqt_list, mol2_list = [], [], []
		for file in ligFile:
			if file.split(".")[-1] == "pdb": pdb_list.append(file)
			if file.split(".")[-1] == "pdbqt": pdbqt_list.append(file)
			if file.split(".")[-1] == "mol2": mol2_list.append(file)
		# PDB
		for filename in pdb_list:
			output_file = filename[:-3]+"pdbqt" # path/filename.pdbqt
			if genPDBQT(filename, output_file):
				got_some = True
				LigandRegistration(output_file)
				# Re-check map cache folder if is defined
				if mapDir and MapSource.get() == 2:
					openDirMaps(mapDir)
			else:
				tkMessageBox.showwarning("PDB Error", ("There is a problem in the input, please check the ligand:\n%s" % filename ))
				break
		# MOL2
		for filename in mol2_list:
			openMultiMol2(filename)
		# PDBQT
		if pdbqt_list:
			list_of_accepted = checkPDBQTligList(pdbqt_list)
			if list_of_accepted:
				got_some = True
				for ligand in list_of_accepted:
					LigandRegistration(ligand)

	# Ligands will be filtered every time (at least because of the TDOF)
	if got_some:
		InfoMessage.set( "Ligands imported successfully.")
	FilterLigands(True)
	countLigands()
	# Re-check map cache folder if is defined
	if mapDir and MapSource.get() == 2:
		openDirMaps(mapDir)
	TheCheck()

def openMultiMol2(ligFile = None):
    # -import both single- and multi-MOL2
	# -accept both input file or none
    # -check for the number of molecules in the MOL2
    # -find a suitable place for splitting the molecules
    # -convert them
    # -add them to the list
    #
	if not ligFile: 
		ligFile = askopenfilename(parent = root, title = "Select a Mol2...", filetypes=[("Mol2", "*.mol2", "MOL2")])
	if ligFile:
		count_mols = CheckMultiMol2(ligFile)
		if not count_mols:
			tkMessageBox.showwarning("Mol2 Error", ("%s doesn't contain any Mol2 structures." % ligFile))
		if count_mols == 1: # it's a single Mol2
			output_file = ligFile[:-4]+"pdbqt" # path/filename.pdbqt
			if genPDBQT(ligFile, output_file):
				LigandRegistration(output_file)
			else:
				tkMessageBox.showerror("Error!", ("Problems converting the MOL2: %s" % ligFile))

		if count_mols > 1: # it's a multiMol2
			if count_mols >= 100:
				WARNING = "\n\n[ Warning: this will take some time ]"
			else:
				WARNING = ""
			if not tkMessageBox.askokcancel('Multi-structure MOL2 file',('A multi-structure file MOL2 containing %d ligands was found. Proceed to split and convert it to PDBQT?%s' % (count_mols, WARNING))):
				return
			output_dir = askdirectory(parent = root, title = ("MOL2: Split and convert %d molecules in the following dir..."% count_mols) , initialdir = os.path.dirname(ligFile))
			if not output_dir:
				tkMessageBox.showinfo(title="MOL2 splitting", message =( "The splitting process of %s has been cancelled by the user" % ligFile))
				return
			
			name = os.path.basename(ligFile)[:-5] # get rid of path and extension ".mol2" (stem)
			
			outputDirMOL2 = output_dir+os.sep+name+os.sep+"mol2"
			outputDirPDBQT = output_dir+os.sep+name+os.sep+"pdbqt"
			# attempt to create the Mol2 output dir
			try:
				if not os.path.exists(outputDirMOL2):
					os.makedirs(outputDirMOL2, 0755)
			except:
				tkMessageBox.showerror("Error!", ("I can't create the output dir:\n%s" % outputDirMol2))
				if DEBUG: print "ERROR> mol2 import process died"
				# break


			# split the mol2 files
			DisableInterface()
			to_be_imported = SplitMol2(ligFile, outputDirMOL2)
			if to_be_imported:
				if DEBUG: print "i'm gong to import", to_be_imported
				# attempt to create the PDBQT output dir
				try:
					if not os.path.exists(outputDirPDBQT):
						os.makedirs(outputDirPDBQT, 0755)
				except:
					tkMessageBox.showerror("Error!", ("I can't create the output dir:\n%s" % outputDirPDBQT))
					if DEBUG: print "ERROR> pdbqt import process died"
					#break
				message = Message(text = "I'm going to convert"+str(count_mols)+"molecules")
				processed = 0
				for ligand in to_be_imported:
					name = os.path.basename(ligand)[:-5]
					output_file = outputDirPDBQT+os.sep+name+".pdbqt" # path/filename.pdbqt
					InfoMessage.set(("Generating PDBQT for %s ...") % name)
					root.update()
					if genPDBQT( ligand, output_file ):
						LigandRegistration(output_file)
						processed += 1
					else:
						tkMessageBox.showerror("Error!", ("Some problem occurred in converting the file:\n%s\n Import process aborted." % ligand))
						break
			EnableInterface()
			if processed == count_mols:
				# Re-check map cache folder if is defined
				if mapDir and MapSource.get() == 2:
					openDirMaps(mapDir)
				tkMessageBox.showinfo(title = "MultiMol2-to-PDBQT", message = ("%d ligands successfully imported from\n%s" % (count_mols, ligFile)))
			else:
				tkMessageBox.showwarning(title = ligFile, message = ("Some problem occurred.\n %d out of %d structures accepted." % (processed, count_mols) )  )
				

def CheckMultiMol2(filename):
	# simple function for checking the number oou
	# multiple structures in the mol2
	count = 0
	try:
		multimol2 = open(filename, 'r')
		for line in multimol2:
			if "@<TRIPOS>MOLECULE" in line:
				count += 1
		if count == 0:
			return False
		else:
			return count
	except:
		tkMessageBox.showwarning("Mol2 Error", "The file doesn't contain any Mol2 structures.")
		return False

def SplitMol2 (filename = None, outdir = None):
	# split a multi-mol2 in the specified directory
	utility_mode = False
	# This is for using the splitting function as an utility:
	if not filename:
		filename = askopenfilename(parent = root, title = "Select a Mol2...", filetypes=[("Mol2", "*.mol2", "MOL2")])
		utility_mode = True
	if not filename:
		return
	# end of utility mode

	buffer = []
	count = 0
	zinc_found = False
	splitted_mols = []
	total = CheckMultiMol2(filename)
	# Also this is for using the splitting function as an utility
	if not outdir:
		outdir = askdirectory(parent = root, title = ("MOL2: Split and convert %d molecules in the following dir..."% total))
	if not outdir:
		tkMessageBox.showinfo(title="MOL2 splitting", message =( "The splitting process of %s has been cancelled by the user" % filename))
		return
	# end of utility mode

	multimol2 = open(filename, 'r') # the input
	name = os.path.basename(filename)[:-5] # needed for the stem of the output files
	try:
		if not os.path.exists(outdir):
			os.makedirs(outdir, 0755)
		InfoMessage.set(("Splitting %s ") % os.path.basename(filename) )
		root.update()
		for line in multimol2.readlines():
			if "@<TRIPOS>MOLECULE" in line:
				if len(buffer) > 1: # INCREASED FROM 0
					count += 1
					number = "%06d" % count

					if zinc_found:
						filename = outdir+os.sep+zinc_id+".mol2"
					else:
						filename = outdir+os.sep+name+"_"+str(number)+".mol2"

					output = open(filename, 'w')
					for item in buffer:
						print >>output, item[:-1]
					output.close()
					del buffer[:]
					splitted_mols.append(filename)
					zinc_found = False
					buffer.append(line)
			else:
				buffer.append(line)
			if "ZINC" in line[0:5]:
				if DEBUG: print "found zinc name |%s|" % line
				zinc_id = line.split()[0]
				zinc_found = True
		if len(buffer) > 0: # Flush the remaining buffer...
			count += 1
			number = "%06d" % count
			if zinc_found:
				filename = outdir+os.sep+zinc_id+".mol2"
			else:
				filename = outdir+os.sep+name+"_"+str(number)+".mol2"
			output = open(filename, 'w')
			for item in buffer:
				print >>output, item[:-1]
			output.close()
			zinc_found = False
			splitted_mols.append(filename)
			del buffer[:]
		if DEBUG: print "splitted", splitted_mols
		if utility_mode:
				tkMessageBox.showinfo(title="MOL2 splitting", message =( "%d molecules have been successfully created in:\n %s" % (count, outdir)))
		InfoMessage.set(("Splitting %s : DONE ") % os.path.basename(filename) )
		root.update()
		return splitted_mols
	except:
		tkMessageBox.showwarning("Error!", ("The selected directory is not accessible: %s"% outdir))
		return False
	if DEBUG : print count, "molecules processed"
		
def genPDBQT(infile, outfile):
	DisableInterface()
	# any resemblance with the prepare_ligand script is accidental
	#
	# generate a pdbqt from a directory containing the splitted mol2 
	#
    # optional parameters

	# PrepareLigand options defaults
	verbose = None
	add_bonds = False
    #-A: repairs to make: add bonds and/or hydrogens
	repairs = Repair.get()
    #-C  default: add gasteiger charges 
	charges_to_add = ChargeSet.get()
    #-p preserve charges on specific atom types
	preserve_charge_types=''
    #-U: cleanup by merging nphs_lps, nphs, lps
	cleanup  = Cleanup.get()
    #-B named rotatable bond type(s) to allow to rotate
	
	# TODO strip the code doing the incremental addition of options, 'cause most
	# likely it uses a split call internally (by Ruth?)
	SELECTED_ALLOWED_BONDS = ""
	if BackboneRotatable:
		SELECTED_ALLOWED_BONDS += "backbone"
	if AmideRotatable:
		if SELECTED_ALLOWED_BONDS:
			SELECTED_ALLOWED_BONDS += "_amide"
		else:
			SELECTED_ALLOWED_BONDS += "amide"
	if GuanidiniumRotatable:
		if SELECTED_ALLOWED_BONDS:
			SELECTED_ALLOWED_BONDS += "guanidinium"
		else:
			SELECTED_ALLOWED_BONDS += "_guanidinium"
	allowed_bonds = SELECTED_ALLOWED_BONDS
    #-r  root
	root = 'auto'
    #-o outputfilename
	outputfilename = outfile # GOOD
    #-F check_for_fragments
	check_for_fragments = LargestFrag.get()
    #-I bonds_to_inactivate
	bonds_to_inactivate = ""
    #-Z inactivate_all_torsions
	inactivate_all_torsions = LockTors.get()
    #-g attach_nonbonded_fragments
	attach_nonbonded_fragments = AttachFrag.get()
    #-m mode 
	mode = 'automatic'
    #-d dictionary
	dict = None


	try:
		mols = Read(infile)
		mol = mols[0]
	except:
		return False
	if len(mols) > 1:
		# put here the filtering
		ctr +=1
		if len(m.allAtoms) > len(mol.allAtoms):
			mol = m

	coord_dict = {}
	for atom in mol.allAtoms: coord_dict[atom] = atom.coords
	mol.buildBondsByDistance()
	if charges_to_add is not None:
		preserved = {}
		preserved_types = preserve_charge_types.split(',')
		for type in preserved_types:
			if not len(type): continue
			ats = mol.allAtoms.get(lambda x: x.autodock_element == type)
			for a in ats:
				if a.chageSet is not None:
					preserved[a] = [a.chargeSet, a.charge]
	LPO = AD4LigandPreparation(mol, mode, repairs, charges_to_add, 
                          cleanup, allowed_bonds, root, 
                          outputfilename=outputfilename,
                          dict=dict, check_for_fragments=check_for_fragments,
                          bonds_to_inactivate=bonds_to_inactivate, 
                          inactivate_all_torsions=inactivate_all_torsions,
                          attach_nonbonded_fragments=attach_nonbonded_fragments)
	if charges_to_add is not None:
		# restore the previous charges
		for atom, chargeList in preserved.items():
			atom._charges[chargeList[0]] = chargeList[1]
			atom.chargeSet = chargeList[0]
	bad_list = []
	for a in mol.allAtoms:
		if a.coords!=coord_dict[a]: bad_list.append(a)
	if len(bad_list):
		if DEBUG:
			print len(bad_list), ' atom coordinates changed!'    
			for a in bad_list:
				print a.name, ":", coord_dict[a], ' -> ', a.coords
	if mol.returnCode is not 0:
		if DEBUG: print "ERROR IN THE EXITCODE!"
		EnableInterface()
		return False
	else:
		InfoMessage.set("%s converted to PDBQT" % os.path.basename(infile))
		nb.update() # TODO Update the window with the message... but not the ROOT!
		EnableInterface()
		return True

def LigandRegistration(filename):
	# INPUT		: pdbqt file
	# OUTPUT	: nothing
	# EXTRA		: append the ligand properties to the Great Book of Ligands
	# 			  update the list of total atom types considered (for caching map)

	file = open(filename, 'r')
	ligand = file.readlines()
	file.close()
	current_atypes = []
	BAD_ATOM_TYPE = False
	MW  = 0
	HbD = 0
	HbA = 0
	Nat = 0
	status = True
	
	hbd_h = []
	hbd_candidate = []

	# Calculate all the properties
	for line in ligand:
		if 'TORSDOF' in line:
			TORSDOF = int(line.split()[1])
		if line[0:6] == 'HETATM' or line[0:4] == 'ATOM':
			# Nat += 1 # Consider to remove Hydrogens? (search on PubMed)
			atype = line.split()[-1]
			if atype not in current_atypes:
				current_atypes.append(atype)
			# Hb acceptor
			if atype == "OA" or atype == "NA" or atype == "SA":
				HbA += 1
			# Hb donor preparation
			if atype == "HD":
				#capture the hydrogens that could be bond to the Hb donor...
				hbd_h.append(line)
			else:
				# count heavy atoms
				Nat += 1

			if atype == "N" or atype == "O" or atype == "OA" or atype == "NA":
				hbd_candidate.append(line)
			try:
				MW += AtypeList[atype][1] # add the atomic weight to the total MW
			except:
				MW += 10000 # check this if it's reasonable
				BAD_ATOM_TYPE = True
				status = False # non-standard atom types are rejected by default
	# identify HBD by checking if N/O's are bound to H's
	for atom in hbd_candidate:
		for hydrogen in hbd_h:
			if dist(atom, hydrogen) <= 1.1:
				HbD += 1
				break
	if DEBUG: print "I've found %s HBD"% HbD

	# Insert the ligand in the Great Book of Ligands
	if not LigandDictionary.has_key(filename):
		# ligand is registered with properties
		LigandDictionary[filename] = {
		"Atypes"	: current_atypes,
		"TORSDOF"	: TORSDOF,
		"HbD"		: HbD,
		"HbA"		: HbA,
		"MW"		: MW,
		"Nat"		: Nat,
		"NotStdAT"	: BAD_ATOM_TYPE,
		"accepted"	: status }
		
		LigandScrolledListBox.insert('end', filename)
		if not BAD_ATOM_TYPE:
			for atype in current_atypes:
				AtypeList[atype][0] += 1  # increment the count for this atom type
				# Add a list of the non std atomt types and count it (for cached maps purposes)???
	if DEBUG:
		# Debug function for atom types...
		print "#### Atom type-DICTIONARY ####"
		for item in AtypeList.keys():
			print item, AtypeList[item][0]
		print "#### Atom type-DICTIONARY ####"


def dist(firstline, secondline):  
	# INFO   : calculate the atomic distance between two PDB atom lines
	# INPUT  : two pdb lines
	# OUTPUT : a pdb line
	coord1=[]
	coord2=[]
	temp=firstline[28:56]
	coord1=temp.split()
	temp=secondline[28:56]
	coord2=temp.split()
	# floating the strings
	for index in range(len(coord1)):
		coord1[index]=float(coord1[index])
		coord2[index]=float(coord2[index])
	measure=sqrt((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2+(coord1[2]-coord2[2])**2)
	return measure


def UpdateATDict(file_list):
	"""
	input:		list of PDBQT filenames to be excluded
	output: 	(nothing)
	operation:	update the dictionary of atom types currently
				loaded
	"""
	for ligand in file_list:
		atypes_to_be_removed = LigandDictionary[ligand]["Atypes"]
		for atype in atypes_to_be_removed:
			AtypeList[atype][0] -= 1

def clearATDict():
	# set all atom type counts to 0 (except for d and e)
	for atom in AtypeList:
		AtypeList[atom][0] = 0
	AtypeList["e"][0] = 1
	AtypeList["d"][0] = 1
	if DEBUG:
		for atom in AtypeList:
			print atom, AtypeList[atom]

def openLigandDir(ligDir = None):  
	if not ligDir:
		ligDir = askdirectory()
	if ligDir:
		# PDBQT 
		ligFiles = glob.glob(os.path.join(ligDir, "*.pdbqt"))            
		if ligFiles:
			for item in checkPDBQTligList(ligFiles):
				LigandRegistration(item)
		# PDB
		ligFiles = glob.glob(os.path.join(ligDir, "*.pdb"))
		if ligFiles:
			openLigand(ligFiles)
		# MOL2
		ligFiles = glob.glob(os.path.join(ligDir, "*.mol2"))
		if ligFiles:
	 		openLigand(ligFiles)
		# Re-check map cache folder if is defined
		if mapDir and MapSource.get() == 2:
			openDirMaps(mapDir)
		# Ligands will be filtered every time (at least because of the TDOF)
		FilterLigands(True)
		countLigands()
		TheCheck()

def openLigandDirRecursive():
	pdbqt_ligandlist = []
	mol2_ligandlist = []
	pdb_ligandlist = []
	count_pdbqt = 0
	count_mol2 = 0
	count_pdb = 0
	ligDir = askdirectory(title = "Select a directory to be scanned")
	if ligDir:
		for root, subFolders, files in os.walk(ligDir):
			for file in files:
				if file[-5:] == "pdbqt":
					pdbqt_ligandlist.append(os.path.join(root,file))
				if file[-4:] == "mol2":
					mol2_ligandlist.append(os.path.join(root,file))
				if file[-3:] == "pdb":
					pdb_ligandlist.append(os.path.join(root,file))
		if DEBUG: 
			print "This would be the ligand file list"
			print "pdbqt", pdbqt_ligandlist
			print "mol2", mol2_ligandlist
			print "pdb", pdb_ligandlist

		count_pdbqt = len(pdbqt_ligandlist)
		count_mol2 = len(mol2_ligandlist)
		count_pdb = len(pdb_ligandlist)
		total = count_pdbqt + count_mol2 + count_pdb
		if total > 1:
			if not tkMessageBox.askokcancel("Ligands found...", ("The directory contains a total of %s potential ligands:\n\n\t%s pdbqt\n\t%s mol2\n\t%s pdb.\
		\n\nStart the import process?" % (total, count_pdbqt, count_mol2, count_pdb) )):
				return
		# PDBQT 
		if count_pdbqt:
			for item in checkPDBQTligList(pdbqt_ligandlist):
				LigandRegistration(item)
		# MOL2
		if count_mol2:
	 		openLigand(mol2_ligandlist)
		# PDB
		if count_pdb:
			openLigand(pdb_ligandlist)
		# Re-check map cache folder if is defined
		if mapDir and MapSource.get() == 2:
			openDirMaps(mapDir)
		# Ligands will be filtered every time (at least because of the TDOF)
		FilterLigands(True)
		countLigands()
		TheCheck()

def removeLigand():
	ligand_index = LigandScrolledListBox.curselection() # position of ligands in the list...
	ligand_list = []
	for item in ligand_index:
		# update the list of ligands to be removed from the Great Book of Ligands
		ligand_list.append(LigandScrolledListBox.get(item))
		# remove the ligands from the visualized list
		LigandScrolledListBox.delete(item)
	UpdateATDict(ligand_list)
	for ligand in ligand_list:
		del LigandDictionary[ligand]
	countLigands()
	FilterLigands(True)
	TheCheck()

def removeReceptor():
	items = receptorScrolledListBox.getcurselection()
	# update the atom type list decrementing the atoms of each ligand
	for ligand in items:
		receptorFileList.remove(ligand)
	receptorScrolledListBox.setlist(receptorFileList) # NOT CLEAR!!!
	if len(receptorFileList) == 0:
		MultiReceptorSet.set(False)
	countReceptors()
	TheCheck()
	    
def removeAllLigands():
	if len(LigandDictionary) > 1 and not tkMessageBox.askokcancel('Delete all the ligands','Do you really want to\nremove all the ligands\nfrom the list?'):
		return
	LigandScrolledListBox.delete(0, END) 
	# Buy a new Great Book of Ligands
	for item in LigandDictionary.keys():
		del LigandDictionary[item]
	countLigands()
	clearATDict()
	TheCheck()

def checkPDBQTligList(filenamelist): 
    AcceptedFiles = []
    RejectedFiles = []
    CountAccepted = 0
    CountRejected = 0
    for file in filenamelist:
        found_ligand = 0
        found_residue = 0
        try:
            for line in open(file, 'r'):
                if line[0:4] == "ROOT":
                    found_ligand = 1
                if line[0:9] == "BEGIN_RES":
                    found_residue = 1
            if DEBUG: print "found res"
            if found_ligand == 1 and found_residue == 0:
                AcceptedFiles.append(file)
                CountAccepted += 1
            else:
                CountRejected += 1
		RejectedFiles.append(file)
	except:
            CountRejected += 1
            RejectedFiles.append(file)
    if CountAccepted == 0:
       if CountRejected == 1:
           tkMessageBox.showwarning("Error!", "The ligand is not valid.")
       else:
           tkMessageBox.showwarning("Ligands error!", "None of %d PDBQT have been accepted.\nPlease check the inputs." % CountRejected)
    if CountAccepted > 0 and CountRejected > 0:
        if tkMessageBox.askokcancel("Ligands imported", "%d\taccepted.\n%d\trejected.\n\nDo you want to inspect the list of rejected ligands?" % (CountAccepted, CountRejected)):
            RejectedWindow = Toplevel()
            RejectedWindow.title("List of rejected PDBQT's")
            scrollbar = Scrollbar(RejectedWindow)
            ListOfRejected = Listbox(RejectedWindow)
            CloseButton = Button(RejectedWindow, text = "Close", command = RejectedWindow.destroy)
            ListOfRejected.grid(column = 0, sticky = W+N+S+E)
            RejectedWindow.grid_rowconfigure(0, minsize = 300, weight = 1)
            RejectedWindow.grid_columnconfigure(0, minsize = 330, weight = 1)
            scrollbar.grid(row = 0, column = 1, sticky = S+N)
            scrollbar.config(command = ListOfRejected.yview)
            ListOfRejected.config(yscrollcommand=scrollbar.set)
            for item in RejectedFiles:
        	    ListOfRejected.insert(END, item)
            CloseButton.grid(row = 2, columnspan = 2, sticky = W+E)
    return AcceptedFiles


def checkPDBQTreclist(filenamelist): 
	AcceptedFiles = []
	RejectedFiles = []
	CountAccepted = 0
	CountRejected = 0
	for file in filenamelist:
		found_ligand = 0
		found_residue = 0
		try:
			for line in open(file, 'r'):
				if line[0:4] == "ROOT":
					found_ligand = 1
				if line[0:9] == "BEGIN_RES":
					found_residue = 1
			if found_ligand == 1 or found_residue == 1:
				CountRejected += 1
				RejectedFiles.append(file)
				if DEBUG: print file, "is bad receptor.."
			else:
				AcceptedFiles.append(file)
				CountAccepted += 1
				if DEBUG: print file, "a good receptor.."
		except:
			CountRejected += 1
			RejectedFiles.append(file)
	if CountRejected == 0:
		if CountAccepted > 1: # To suppress messages for a single ligand import
			notification = "%d receptors\nhave been accepted." % CountAccepted
			tkMessageBox.showinfo(title="PDBQT receptor imported", message=notification)
	if CountAccepted == 0:
		if CountRejected == 1:
			tkMessageBox.showwarning("Error!", "The receptor is not valid.")
		else:
			tkMessageBox.showwarning("Receptors error!", "None of %d receptors have been accepted.\nPlease check the inputs." % CountRejected)
	if CountAccepted > 0 and CountRejected > 0:
		if tkMessageBox.askokcancel("Receptors imported", "%d\taccepted.\n%d\trejected.\n\nDo you want to inspect the list of rejected structures?" % (CountAccepted, CountRejected)):
			RejectedWindow = Toplevel()
			RejectedWindow.title("List of rejected PDBQT's")
			scrollbar = Scrollbar(RejectedWindow)
			ListOfRejected = Listbox(RejectedWindow)
			CloseButton = Button(RejectedWindow, text = "Close", command = RejectedWindow.destroy)
			ListOfRejected.grid(column = 0, sticky = W+N+S+E)
			RejectedWindow.grid_rowconfigure(0, minsize = 300, weight = 1)
			RejectedWindow.grid_columnconfigure(0, minsize = 330, weight = 1)
			scrollbar.grid(row = 0, column = 1, sticky = S+N)
			scrollbar.config(command = ListOfRejected.yview)
			ListOfRejected.config(yscrollcommand=scrollbar.set)
			for item in RejectedFiles:
				ListOfRejected.insert(END, item)
			CloseButton.grid(row = 2, columnspan = 2, sticky = W+E)
	return AcceptedFiles



def CheckLigFilterOptions():
	for value in HbDmin, HbDmax, HbAmin, HbAmax, MWmin, MWmax, NatMin, NatMax, TORSDOFmin, TORSDOFmax:
		try:
			value.get()
		except:
			tkMessageBox.showwarning("Error", "Only numerical values\nare allowed ...\n Try again!\n(resetting to default)")
			FilteringDefaults(FilterSet.get())
			return False
			break
		if value.get() < 0:
			tkMessageBox.showwarning("Uhmmmm...", "In the current implementation of\nthe Universe negative values\nfor these params are not allowed...\n\nTry one of the following options:\n   - recompile the Universe\n   - use positive value\n\n[resetting to default]")
			FilteringDefaults(FilterSet.get())
			return False
			break
	if TORSDOFmax.get() + FlexResTORSDOF.get() > AutoDockMaxTORSDOF.get():
		if DEBUG: print TORSDOFmax.get(), FlexResTORSDOF.get(), AutoDockMaxTORSDOF.get()
		if FlexResTORSDOF.get() > 0:	
			tkMessageBox.showwarning("Torsion Limit Error", "AutoDock is limited to max %s rotatable bonds.\n\nThere are %s rotatable bonds already allotted for the flex residues, therefore the maximum number of rotatable bonds per ligand is set to %s." % ( AutoDockMaxTORSDOF.get(), FlexResTORSDOF.get(), AutoDockMaxTORSDOF.get() - FlexResTORSDOF.get() ))
		else:
			tkMessageBox.showwarning("Torsion Limit Error", "AutoDock is limited to max %s rotatable bonds." % ( AutoDockMaxTORSDOF.get() ))
		FilteringDefaults("TORSDOF")

	MinMax = False
	if HbDmin.get() <= HbDmax.get():
		if HbAmin.get() <= HbAmax.get():
			if MWmin.get() <= MWmax.get():
				if NatMin.get() <= NatMax.get():
					if TORSDOFmin.get() <= TORSDOFmax.get():
						MinMax = True
	if not MinMax:
		FilteringDefaults(FilterSet.get())
		tkMessageBox.showwarning("Uhmmmm...", "Guess what?\nMAX must be bigger than or equal to MIN.\n\n[resetting to default]")
		return False
	else:
		return True

def DefaultLigOptions():
	ChargeSet.set("gasteiger")
	Repair.set("")
	Cleanup.set("nphs_lps")
	BackboneRotatable.set(True)
	AmideRotatable.set(False)
	GuanidiniumRotatable.set(False)
	LockTors.set(False)
	LargestFrag.set(False)
	AttachFrag.set(False)

def LigandImportOptions(): # Options for non-PDBQT files only
	try:
		LigandOptionsWin.lift()
	except:
		LigandOptionsWin = Toplevel(root)
		LigandOptionsWin.title("PDBQT generation options")
		LigandOptionsWin.winfo_toplevel().resizable(NO,NO)

		ChargeFrame = Pmw.Group(LigandOptionsWin, tag_text = "Partial charges")
		Radiobutton(ChargeFrame.interior(), text="Add Gasteiger", variable = ChargeSet, value = "gasteiger").grid(row = 0, column = 0, sticky = W) # Default
		Radiobutton(ChargeFrame.interior(), text="Keep original", variable = ChargeSet, value = "").grid(row = 0, column = 1, sticky = W)
		ChargeFrame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = W, columnspan = 2)

		RepairFrame = Pmw.Group(LigandOptionsWin, tag_text = "Structure repair ")
		Radiobutton(RepairFrame.interior(), text = "none", variable = Repair, value = "").grid(row = 1 , column = 0, sticky = N ) # Default
		Radiobutton(RepairFrame.interior(), text = "bonds", variable = Repair, value = "bonds" ).grid(row = 1 , column = 1, sticky = N )
		Radiobutton(RepairFrame.interior(), text = "hydrogens", variable = Repair, value = "hydrogens" ).grid(row = 1 , column = 2 , sticky = N )
		Radiobutton(RepairFrame.interior(), text = "both", variable = Repair, value = "bond_hydrogens" ).grid(row = 1 , column = 3, sticky = N )
		RepairFrame.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = W, columnspan = 2)

		CleanupFrame = Pmw.Group(LigandOptionsWin, tag_text = "Structure clean-up ")
		Radiobutton(CleanupFrame.interior(), text = "\nboth\n", variable = Cleanup, value = "nphs_lps" ).grid(row = 1 , column = 3, sticky = N ) # Default
		Radiobutton(CleanupFrame.interior(), text = "merge\nnon-polar H\n", variable = Cleanup, value = "nphs" ).grid(row = 1 , column = 1, sticky = N )
		Radiobutton(CleanupFrame.interior(), text = "delete\nlone pairs\n", variable = Cleanup, value = "lps" ).grid(row = 1 , column = 2 , sticky = N )
		Radiobutton(CleanupFrame.interior(), text = "\nnone\n", variable = Cleanup, value = "").grid(row = 1 , column = 0, sticky = N ) 
		CleanupFrame.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = W, columnspan = 2)

		RotatableFrame = Pmw.Group(LigandOptionsWin, tag_text = "Activate special\nrotatable bonds")
		Label(RotatableFrame.interior(), text = " yes").grid(row = 0, column = 1, sticky = W)
		Label(RotatableFrame.interior(), text = " no      ").grid(row = 0, column = 2, sticky = W)
		Label(RotatableFrame.interior(), text = "     backbone   ").grid(row = 1, column = 0, sticky = W)
		Radiobutton(RotatableFrame.interior(), variable = BackboneRotatable, value = True ).grid(row = 1 , column = 1, sticky = W ) # Default
		Radiobutton(RotatableFrame.interior(), variable = BackboneRotatable, value = False ).grid(row = 1 , column = 2, sticky = W )
		Label(RotatableFrame.interior(), text = "     amide   ").grid(row = 2, column = 0, sticky = W)
		Radiobutton(RotatableFrame.interior(), variable = AmideRotatable, value = True ).grid(row = 2 , column = 1, sticky = W )
		Radiobutton(RotatableFrame.interior(), variable = AmideRotatable, value = False ).grid(row = 2 , column = 2, sticky = W ) # Default
		Label(RotatableFrame.interior(), text = " guanidinium   ").grid(row = 3, column = 0, sticky = W)
		Radiobutton(RotatableFrame.interior(), variable = GuanidiniumRotatable, value = True ).grid(row = 3 , column = 1, sticky = W )
		Radiobutton(RotatableFrame.interior(), variable = GuanidiniumRotatable, value = False ).grid(row = 3 , column = 2, sticky = W ) # Default
		RotatableFrame.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = W)

		Checkbutton(LigandOptionsWin, text = "Inactivate ALL active\ntorsions", variable = LockTors, indicatoron = False ).grid(row = 5 , column = 1, sticky = W)

		FragmentFrame = Pmw.Group(LigandOptionsWin, tag_text = "Fragmented structures")
		Radiobutton(FragmentFrame.interior(), text = "Keep largest fragment", variable = LargestFrag, value = True ).grid(row = 0 , column = 0, sticky = W )
		Radiobutton(FragmentFrame.interior(), text = "Keep all", variable = LargestFrag, value = False ).grid(row = 0 , column = 1, sticky = W ) # Default
		Checkbutton(FragmentFrame.interior(), text = "Attach non-bonded fragments", variable = AttachFrag, indicatoron = False).grid(row = 1 , column = 1, sticky = W)
		FragmentFrame.grid(row = 6, column = 0,  padx = 10, pady = 10, sticky = W, columnspan = 2)

		Tkinter.Button(LigandOptionsWin, text="OK", command = LigandOptionsWin.destroy, width = 50 ).grid(row = 9, column = 0, sticky = S, columnspan = 2, pady = 10, padx = 10)
		Tkinter.Button(LigandOptionsWin, text="Set defaults", command = DefaultLigOptions, width = 50).grid(row = 1, column = 0, columnspan = 3, sticky = S, pady = 10, padx = 10)

	
def LigandFilterOptions(): # Filtering files
	global LigandFilterWin, FilterSet
	try:
		LigandFilterWin.lift()
	except:
		LigandFilterWin = Toplevel(root)
		LigandFilterWin.title("Ligand filters")
		LigandFilterWin.winfo_toplevel().resizable(NO,NO)
		rejected = 0
		total = len(LigandDictionary.keys())
		for item in LigandDictionary.keys():
			if not LigandDictionary[item]["accepted"]:
				rejected += 1
		accepted = total - rejected
		msg = "Total number of ligands: %12s" % str(total)
		TotalNumberLigandsMsg.set(msg)
		msg = "Accepted ligands: %12s" % str(accepted)
		TotAcceptedLigandsMsg.set(msg)
		msg = "Rejected ligands: %12s" % str(rejected)
		TotRejectedLigandsMsg.set(msg)

		# Preset menu
		Label(LigandFilterWin, text = "Filter presets :").grid(row = 0, column = 0, columnspan = 1, sticky = W)
		PrecannedFilters = OptionMenu(LigandFilterWin, FilterSet, "Default", "Lipinski-like", "DrugLikeness", "DrugLikeness (frag)", command = lambda event : FilteringDefaults())
		PrecannedFilters.grid(row = 0, column = 1, columnspan = 1, sticky = W, pady = 10)

		FiltersFrame = Pmw.Group(LigandFilterWin, tag_text = "Molecular properties")
		Label(FiltersFrame.interior(), text = "MIN").grid(row = 1, column = 1, sticky = N)
		Label(FiltersFrame.interior(), text = "MAX").grid(row = 1, column = 2, sticky = N)

		Label(FiltersFrame.interior(), text = "H-bond donors").grid(row = 2, column = 0, sticky = W, padx = 10)
	   	HbDonors1 = Entry(FiltersFrame.interior(), width = 4, textvariable=HbDmin).grid(row=2, column = 1, sticky = W, columnspan = 1)
	   	HbDonors2 = Entry(FiltersFrame.interior(), width = 4, textvariable=HbDmax).grid(row=2, column = 2, sticky = W, columnspan = 1)
		Button(FiltersFrame.interior(), text = "Default",width = 5, command = lambda : FilteringDefaults("HbD")).grid(row = 2, column = 3, padx = 10, pady = 3)

		Label(FiltersFrame.interior(), text = "H-bond acceptors").grid(row = 3, column = 0, sticky = W, padx = 10)
	   	HbAcceptors1 = Entry(FiltersFrame.interior(), width = 4, textvariable=HbAmin).grid(row=3, column = 1, sticky = W, columnspan = 1)
	   	HbAcceptors2 = Entry(FiltersFrame.interior(), width = 4, textvariable=HbAmax).grid(row=3, column = 2, sticky = W, columnspan = 1)
		Button(FiltersFrame.interior(), text = "Default",width = 5, command = lambda : FilteringDefaults("HbA")).grid(row = 3, column = 3, padx = 10, pady = 3)

		Label(FiltersFrame.interior(), text = "Molecular weight").grid(row = 4, column = 0, sticky = W, padx = 10)
	   	HbAcceptors1 = Entry(FiltersFrame.interior(), width = 4, textvariable=MWmin).grid(row=4, column = 1, sticky = W, columnspan = 1)
	   	HbAcceptors2 = Entry(FiltersFrame.interior(), width = 4, textvariable=MWmax).grid(row=4, column = 2, sticky = W, columnspan = 1)
		Button(FiltersFrame.interior(), text = "Default",width = 5, command = lambda : FilteringDefaults("MW")).grid(row = 4, column = 3, padx = 10, pady = 3)

		Label(FiltersFrame.interior(), text = "Number of atoms").grid(row = 5, column = 0, sticky = W, padx = 10)
	   	HbAcceptors1 = Entry(FiltersFrame.interior(), width = 4, textvariable=NatMin).grid(row=5, column = 1, sticky = W, columnspan = 1)
	   	HbAcceptors2 = Entry(FiltersFrame.interior(), width = 4, textvariable=NatMax).grid(row=5, column = 2, sticky = W, columnspan = 1)
		Button(FiltersFrame.interior(), text = "Default",width = 5, command = lambda : FilteringDefaults("Nat")).grid(row = 5, column = 3, padx = 10, pady = 3)

		Label(FiltersFrame.interior(), text = "Rotatable bonds").grid(row = 6, column = 0, sticky = W, padx = 10)
	   	HbAcceptors1 = Entry(FiltersFrame.interior(), width = 4, textvariable=TORSDOFmin).grid(row=6, column = 1, sticky = W, columnspan = 1)
	   	HbAcceptors2 = Entry(FiltersFrame.interior(), width = 4, textvariable=TORSDOFmax).grid(row=6, column = 2, sticky = W, columnspan = 1)
		Button(FiltersFrame.interior(), text = "Default",width = 5, command = lambda : FilteringDefaults("TORSDOF")).grid(row = 6, column = 3, padx = 10, pady = 3)

		FiltersFrame.grid(row = 1 , column = 0, columnspan = 2, padx = 10)
	
		# Preview info frame
		PreviewFrame = Frame(LigandFilterWin, relief=GROOVE, padx = 10, pady = 10, border = 2)
		TotalLabel = Label(PreviewFrame, textvariable = TotalNumberLigandsMsg).grid(row = 1, column = 0, sticky = E)
		AcceptedLabel = Label(PreviewFrame, textvariable = TotAcceptedLigandsMsg)
		AcceptedLabel.grid(row = 2, column = 0, sticky = E)
		RejectedLabel = Label(PreviewFrame, textvariable = TotRejectedLigandsMsg)
		RejectedLabel.grid(row = 3, column = 0, sticky = E)
		
		PreviewFrame.grid(row = 1, column = 2, padx = 10)
		Checkbutton(FiltersFrame.interior(), text = "Filter ligands with non-AD atom types", variable = DoRejectATypes, onvalue = True, offvalue = False).grid(row = 7, column = 0, columnspan = 4, pady = 2)

		Button(LigandFilterWin, text = "Preview",width = 30, command = lambda : FilterLigands(False)).grid(row = 1, column = 2, sticky = N, pady = 10) #, columnspan = 3)
		Button(LigandFilterWin, text = "Apply",width = 50, height = 2, command = lambda : FilterLigands(True)).grid(row = 5, column = 0, columnspan = 3, pady = 10)



def FilteringDefaults(param = None):
	# The function set the default values for all the single parameters
 	# as well as for the entire sets.
	#
	verbose = False
	if not param:
		param = FilterSet.get()
	# calculate how many torsions are left counting the flex residues, if present
	max_tors = AutoDockMaxTORSDOF.get() - FlexResTORSDOF.get() # Include the FlexResidues into the count of max TORSDOF
	if verbose or DEBUG: print "FILTERING DEFAULTS> setting the max TORSDOF to ", max_tors

	if param == "HbD":
		if FilterSet.get() == "Default":
			HbDmin.set(0), HbDmax.set(99)
		if FilterSet.get() == "Lipinski-like":
			HbDmin.set(0), HbDmax.set(5)
		if FilterSet.get() == "DrugLikeness":
			HbDmin.set(0), HbDmax.set(5)
		if FilterSet.get() == "DrugLikeness (frag)":
			HbDmin.set(0), HbDmax.set(3)

	if param == "HbA":
		if FilterSet.get() == "Default":
			HbAmin.set(0), HbAmax.set(99)
		if FilterSet.get() == "Lipinski-like":
			HbAmin.set(0), HbAmax.set(10)
		if FilterSet.get() == "DrugLikeness":
			HbAmin.set(0), HbAmax.set(10)
		if FilterSet.get() == "DrugLikeness (frag)":
			HbAmin.set(0), HbAmax.set(6) 

	if param == "MW":
		if FilterSet.get() == "Default":
			MWmin.set(0), MWmax.set(9999)
		if FilterSet.get() == "Lipinski-like":
			MWmin.set(0), MWmax.set(500)
		if FilterSet.get() == "DrugLikeness":
			MWmin.set(160), MWmax.set(480)
		if FilterSet.get() == "DrugLikeness (frag)":
			MWmin.set(160), MWmax.set(300)

	if param == "Nat":
		if FilterSet.get() == "Default":
			NatMin.set(0), NatMax.set(999) # TODO use the right value for unix (2048) or cygwin (128) max atoms ?
		if FilterSet.get() == "Lipinski-like":
			NatMin.set(0), NatMax.set(999)
		if FilterSet.get() == "DrugLikeness":
			NatMin.set(20), NatMax.set(70)
		if FilterSet.get() == "DrugLikeness (frag)":
			NatMin.set(6), NatMax.set(45)

	if param == "TORSDOF":
		if FilterSet.get() == "Default":
			TORSDOFmin.set(0), TORSDOFmax.set(max_tors)
		if FilterSet.get() == "Lipinski-like":
			TORSDOFmin.set(0), TORSDOFmax.set(max_tors)
		if FilterSet.get() == "DrugLikeness":
			TORSDOFmin.set(0), TORSDOFmax.set(max_tors)
		if FilterSet.get() == "DrugLikeness (frag)":
			TORSDOFmin.set(0), TORSDOFmax.set(max_tors)

	# set the Raccoon defaults
	if not param or param == "Default":
		HbDmin.set(0), HbDmax.set(99)
		HbAmin.set(0), HbAmax.set(99)
		MWmin.set(0), MWmax.set(9999)
		NatMin.set(0), NatMax.set(999)
		TORSDOFmin.set(0), TORSDOFmax.set(max_tors)
		DoRejectATypes.set(True)
	
	# http://en.wikipedia.org/wiki/Lipinski%27s_Rule_of_Five
	if param == "Lipinski-like":
		HbDmin.set(0), HbDmax.set(5)
		HbAmin.set(0), HbAmax.set(10)
		MWmin.set(0), MWmax.set(500)
		NatMin.set(0), NatMax.set(999)
		TORSDOFmin.set(0), TORSDOFmax.set(max_tors)
		DoRejectATypes.set(True)

	# http://en.wikipedia.org/wiki/Lipinski%27s_Rule_of_Five#cite_note-2
	if param == "DrugLikeness":
		HbDmin.set(0), HbDmax.set(5)
		HbAmin.set(0), HbAmax.set(10)
		MWmin.set(160), MWmax.set(480)
		NatMin.set(20), NatMax.set(70)
		TORSDOFmin.set(0), TORSDOFmax.set(max_tors)
		DoRejectATypes.set(True)

	# Values from Fattori's paper
	if param == "DrugLikeness (frag)":
		HbDmin.set(0), HbDmax.set(3)
		HbAmin.set(0), HbAmax.set(6)
		MWmin.set(160), MWmax.set(250)
		NatMin.set(6), NatMax.set(45)
		TORSDOFmin.set(0), TORSDOFmax.set(max_tors)
		DoRejectATypes.set(True)


def FilterLigands(seriously):
	accepted_ligands = []
	rejected_ligands = []

	verbose = False
	
	# VALIDATE INPUT
	if CheckLigFilterOptions():
		for lig in LigandDictionary.keys():
			lig_hba = LigandDictionary[lig]["HbA"]
			lig_hbd = LigandDictionary[lig]["HbD"]
			lig_tors = LigandDictionary[lig]["TORSDOF"]
			lig_mw = LigandDictionary[lig]["MW"]
			lig_nat = LigandDictionary[lig]["Nat"]
			lig_notstdat = LigandDictionary[lig]["NotStdAT"]
			if lig_notstdat and DoRejectATypes:
				rejected_ligands.append(lig)
				if verbose or DEBUG: print lig, "rejected by NonSTDatom type", LigandDictionary[lig]["NotStdAT"]
			else:
				if lig_hba >= HbAmin.get() and lig_hba <= HbAmax.get():
					if lig_hbd >= HbDmin.get() and lig_hbd <= HbDmax.get():
						if lig_tors >= TORSDOFmin.get() and lig_tors <= TORSDOFmax.get():
							if lig_mw >= MWmin.get() and lig_mw <= MWmax.get():
								if lig_nat >= NatMin.get() and lig_nat <= NatMax.get():
									accepted_ligands.append(lig)
									if verbose or DEBUG: print "ACCEPTED", lig
								else:
									rejected_ligands.append(lig)
									if verbose or DEBUG: print lig, "rejected number of atoms", lig_nat
							else:
								if verbose or DEBUG: print lig, "rejected molecular weight", lig_mw
								rejected_ligands.append(lig)
						else:
							rejected_ligands.append(lig)
							if verbose or DEBUG: print lig, "rejected torsions", lig_tors
					else:
						rejected_ligands.append(lig)
						if verbose or DEBUG: print lig, "rejected HBD", lig_hbd
				else:
					rejected_ligands.append(lig)
					if verbose or DEBUG: print lig, "rejected HBA", lig_hba
		# summarize the filtering process
		total = len(LigandDictionary.keys())
		rejected = len(rejected_ligands)
		accepted = total - rejected
		msg = "Total number of ligands: %12s" % str(total)
		TotalNumberLigandsMsg.set(msg)
		msg = "Accepted ligands: %12s" % str(accepted)
		TotAcceptedLigandsMsg.set(msg)
		msg = "Rejected ligands: %12s" % str(rejected)
		TotRejectedLigandsMsg.set(msg)
		# this variable is set for make TheCheck function quicker
		TotalAcceptedLigands.set(accepted)
		if seriously:
			for lig in rejected_ligands:
				LigandDictionary[lig]["accepted"] = False
			for lig in accepted_ligands:
				LigandDictionary[lig]["accepted"] = True
			LigandsTag()
			try:
				TheCheck()
			except:
				pass
			countLigands()
			try:
				LigandFilterWin.destroy()
			except:
				return

def LigandsTag():
	# Color ligands basing on their status ACCEPTED/REJECTED
	acc_col = 'black'
	rej_col = 'red'
	for item in range(0, LigandScrolledListBox.size()):
		if not LigandDictionary[LigandScrolledListBox.get(item)]["accepted"]:
			LigandScrolledListBox.itemconfig(item, fg = 'red') #white', bg = '#aa2200')
		else:
			LigandScrolledListBox.itemconfig(item, fg = 'black') #white', bg = '#22aa00') 
	return

#########################################################################################################33
#########################################################################################################33
#########################################################################################################33
#########################################################################################################33
#########################################################################################################33
############################### RECEPTOR STUFF

def countReceptors():
	# it works for RC's only
	if len(receptorFileList) > 0:
		message = "Receptor conformations ("+str(len(receptorFileList))+")"
		TargetPDBQT.set(message)
	else:
		TargetPDBQT.set("Import receptor conformations...")

def openReceptorDir(recDir = None):
	if not recDir:
		recDir = askdirectory()
	if recDir:
		queue_in = []
		queue_out = []
		# PDBQT
		recFiles = glob.glob(os.path.join(recDir, "*.pdbqt"))            
		for item in recFiles:
			queue_out.append(item)
		# PDB/MOL2
		recFiles = glob.glob(os.path.join(recDir, "*.pdb"))
		for item in recFiles:
			queue_in.append(item)
		recFiles = glob.glob(os.path.join(recDir, "*.mol2"))
		for item in recFiles:
			queue_in.append(item)

		if len(queue_in) and not tkMessageBox.askokcancel('Non-PDBQT files found',('The directory contains %d structures to be converted in PDBQT.\nDo you want to proceed?' % len(queue_in))):
			tkMessageBox.showwarning("Import skipped", "No structures have been imported")
			return

		DisableInterface()
		for file in queue_in:
			output_file = file.rsplit(".", 1)[:-1][0]+".pdbqt" # 'Efficient' way to get the stem
			InfoMessage.set( (  "=> Generating PDBQT structure for  %s" % (os.path.basename(file)[-5:]) ))
			root.update()
			genPDBQTrec(file, output_file)
			queue_out.append(output_file)
		for item in checkPDBQTreclist(queue_out):
			if item not in receptorFileList:
				receptorFileList.append(item)
				receptorScrolledListBox.insert('end', item)                
				MultiReceptorSet.set(True)
		countReceptors()
		InfoMessage.set("Receptor structures imported successfully")
		EnableInterface()
		if DoFlex.get() == 1:
			ParseFlexSelection()
		TheCheck()

def openReceptor(filename = None):
	# the input is a list
	if filename:
		recFile = filename
	else:
		recFile = askopenfilename(title = "Select one or more target structures...", filetypes=[("Protein/DNA PDBQT", "*.pdbqt"), ("PDB", "*.pdb"), ("Mol2", "*.mol2")], multiple = 1)
	if recFile:
		queue_in = []
		queue_out = []
		for file in recFile:
			if file[-3:] == "pdb" or file[-4:] == "mol2":
				queue_in.append(file)
			if file[-5:] == "pdbqt":
				queue_out.append(file)
		DisableInterface()
		for file in queue_in:
			output_file = file.rsplit(".", 1)[:-1][0]+".pdbqt" # 'Efficient' way to get the stem
			InfoMessage.set( (  "=> Generating PDBQT structure for  %s" % (os.path.basename(SingleRecFileAsk)[-5:]) ))
			root.update()
			genPDBQTrec(file, output_file)
			queue_out.append(output_file)
		for item in checkPDBQTreclist(queue_out):
			if item not in receptorFileList:
				receptorFileList.append(item)
				receptorScrolledListBox.insert('end', item)                
			MultiReceptorSet.set(True)
		InfoMessage.set(   "Receptor structure imported successfully")
		EnableInterface()
		countReceptors()
		if DoFlex.get() == 1:
			ParseFlexSelection()
		TheCheck()



def removeAllReceptors():
    global receptorFileList
    if len(receptorFileList) > 1 and not tkMessageBox.askokcancel('Delete all the receptors.','Do you really want to\nremove all the receptors\nfrom the list?'):
         return
    del receptorFileList[:]
    receptorScrolledListBox.clear()
    MultiReceptorSet.set(False)
    countReceptors()
    TheCheck()


def openSingleReceptor(filename = None): 
	if filename:
		SingleRecFileAsk = filename
	else:
		SingleRecFileAsk = askopenfilename(filetypes=[("Protein/DNA PDBQT", "*.pdbqt"), ("PDB", "*.pdb"), ("Mol2", "*.mol2")])
	if SingleRecFileAsk:
		# PDBQT structure
		if SingleRecFileAsk[-5:] == "pdbqt":
			if checkPDBQTrec(SingleRecFileAsk):
				singleRecFile = SingleRecFileAsk
				RecFilename.set(SingleRecFileAsk)
				SingleRecFilenameLabel.config(font = ("Helvetica", 10, "bold") ) 
				SingleReceptorSet.set(True)
				ReceptorOptions()
		# PDB/Mol2 receptor
		elif SingleRecFileAsk[-3:] == "pdb" or SingleRecFileAsk[-4:] == "mol2":
			print "PDB/MOL2 receptor"
			output_file = SingleRecFileAsk.rsplit(".", 1)[:-1][0]+".pdbqt" # Efficient way to get the stem
			if genPDBQTrec(SingleRecFileAsk, output_file):
				if checkPDBQTrec(output_file):
					singleRecFile = output_file
					RecFilename.set(output_file)
					SingleRecFilenameLabel.config(font = ("Helvetica", 10, "bold") ) 
					SingleReceptorSet.set(True)
					ReceptorOptions()
	else:
		RecFilename.set('')
		SingleReceptorSet.set(False)
		AutoGridWhen3.config(state = DISABLED)
	TheCheck()	

def genPDBQTrec(infile, outfile):
	# If this file closely resemble the Prepare_receptor4.py, it's normal.
	receptor_filename = infile
	outputfilename = outfile

	repair_set = RecRepairOptionsSet.get()
	if repair_set == 'none':
		repairs = None
	if repair_set == 'rebuild bonds':
		repairs = 'bonds'
	if repair_set == 'add H':
		repairs = 'hydrogens'
	if repair_set == 'add H (if missing)':
		repairs = 'checkhydrogens'
	if repair_set == 'rebuild bonds + add H':
		repairs = 'bonds_hydrogens'
	
	charges_to_add = RecChargeSet.get()

	# preserve_charge_types = a			 # NEGLECTED AS IN THE LIGANDS
	cleanup = RecCleanNPH.get()+RecCleanLP.get()+RecCleanWAT.get()+RecDelAlternate.get()
	delete_single_nonstd_residues  = RecCleanStdRes.get()
	
	verbose = None
	mode = 'automatic'
	preserve_charge_types = None

	mols = Read(receptor_filename)
	if verbose: print 'read ', receptor_filename
	try:
		mol = mols[0]
	except:
		return False
	preserved = {}
	if charges_to_add is not None and preserve_charge_types is not None:
		preserved_types = preserve_charge_types.split(',') 
		if verbose: print "preserved_types=", preserved_types
		for t in preserved_types:
			if verbose: print 'preserving charges on type->', t
			if not len(t): continue
			ats = mol.allAtoms.get(lambda x: x.autodock_element==t)
			if verbose: print "preserving charges on ", ats.name
			for a in ats:
				if a.chargeSet is not None:
					preserved[a] = [a.chargeSet, a.charge]

	if len(mols)>1:
		if verbose: print "more than one molecule in file"
		#use the molecule with the most atoms
		ctr = 1
		for m in mols[1:]:
			ctr += 1
			if len(m.allAtoms)>len(mol.allAtoms):
				mol = m
				if verbose: print "mol set to ", ctr, "th molecule with", len(mol.allAtoms), "atoms"
	mol.buildBondsByDistance()

	RPO = AD4ReceptorPreparation(mol, mode, repairs, charges_to_add, 
						cleanup, outputfilename=outputfilename,
						preserved=preserved, 
						delete_single_nonstd_residues=delete_single_nonstd_residues)	
	if charges_to_add is not None:
		#restore any previous charges
		for atom, chargeList in preserved.items():
			atom._charges[chargeList[0]] = chargeList[1]
			atom.chargeSet = chargeList[0]
	return True


def checkPDBQTrec(filename):
	found_ligand = 0
	found_some_atom = 0
	for line in open(filename, 'r'):
		if line[0:4] == "ROOT":
			found_ligand = 1
		if line[0:4] == "ATOM":
			found_some_atom = 1
	if found_ligand == 0:
		if found_some_atom == 1:
			return True
		else:
			tkMessageBox.showerror("Receptor Error", "The file is not a valid PDBQT.")
			return False
	else:
		tkMessageBox.showerror("Receptor Error", "The selected PDBQT file is a ligand file...")
		return False

def SetFlexibleResidueFile(get_name = None):
	global FlexResFileName, FLEX_SET, ResidueStatus, ResidueStatusLoaded
	if not get_name:
		get_name = askopenfilename(filetypes=[("Flex residue PDBQT", "*.pdbqt")])
	S = ""
	if get_name:
		FlexResFileName.set("")
		ResidueCount = 0
		try:
			file = open(get_name, 'r')
		except:
			tkMessageBox.showerror("Flexibile Residue Error", "Error while opening the flexible residue file:\n"+get_name)
			return False

		for line in file: 
			if line[0:9] == "BEGIN_RES":
				ResidueCount += 1

		if ResidueCount:
			# Chech that torsions are OK in the flex res file
			# update the message bar
			if ResidueCount >1: S = "s"
			FlexResFileName.set(get_name)
			FlexResDefined.set(True)
			FlexTorsionCount()
			ResidueStatusLoaded.set(str(ResidueCount)+" residue"+S+" loaded [ "+str(FlexResTORSDOF.get())+" rotatable bonds ]")
			ResidueStatus.set(ResidueStatusLoaded.get())
		else:
			tkMessageBox.showerror("Flexibile Residue Error", "The loaded PDBQT file is not a flexible residue.")
			ResidueStatus.set("")
	else:
		FlexResTORSDOF.set(0)
		FlexResFileName.set("")
		ResidueStatus.set("")
		FlexTorsionCount()
	TheCheck()

def FlexTorsionCount(force = False):
	"""-checks the number of rotatable bonds of selected/loaded flexible residues """
	verbose = False

	if force:
		FlexResTORSDOF.set(0)
		TORSDOFmax.set(AutoDockMaxTORSDOF.get())
		FilteringDefaults("TORSDOF")
		return

	found_flex_tors = 0

	if FlexResFileName.get() == "" and ListFlexResiduesNames.get() == "":
		return

	# File mode
	if DoFlexFromWhat.get() == 1 and not FlexResFileName.get() == "":
		for line in open(FlexResFileName.get(), 'r'):
			if "active torsions" in line:
				found_flex_tors +=  int(line.split()[1])
	# Selection mode
	if DoFlexFromWhat.get() == 2 and not ListFlexResiduesNames.get() == "":
		list_of_residues = []
		list_of_flex_res_atypes = []
		selection = ListFlexResiduesNames.get()
		selection = selection.replace(' ', '')
		selection = selection.split(',')
		for res in set(selection):
			res = res.split(':')
			res_nam = res[-1][0:3]
			list_of_residues.append(res_nam)
		for res in list_of_residues:
			found_flex_tors += ResidueRotatableBondTable[res][0]
		if verbose or DEBUG: print " adding %s rot's for %s" % ( ResidueRotatableBondTable[res_nam][0], res_nam)
		if verbose or DEBUG: print "FLEX> this is the final count of rotatable bonds included for the flex res count:", found_flex_tors

	# Too many rotatable bonds reached
	if found_flex_tors > AutoDockMaxTORSDOF.get():
		tkMessageBox.showerror("Too many rotatable bonds", ("The imported flex residues have %s rotatable bonds.\n\
The maximum number of rotatable bonds allowed by AutoDock is %s." % (found_flex_tors, AutoDockMaxTORSDOF.get() )))
		FlexResTORSDOF.set(0)
		# Remove the flex res settings
		if DoFlexFromWhat.get() == 1:
				FlexResFileName.set("")
				FlexResDefined.set(False)
				ResidueStatus.set("")
				FlexResTORSDOF.set(0)
				TORSDOFmax.set(AutoDockMaxTORSDOF.get())
				FilteringDefaults("TORSDOF")
				TheCheck()
				return False
		if DoFlexFromWhat.get() == 2:
				ResidueStatus.set("[ none ]") 
				FlexResDefined.set(False)
				FlexResTORSDOF.set(0)
				TORSDOFmax.set(AutoDockMaxTORSDOF.get())
				FilteringDefaults("TORSDOF")
				TheCheck()
				return False

	# Maximum rotatable bonds limit reached
	if found_flex_tors == AutoDockMaxTORSDOF.get():
		tkMessageBox.showwarning("Rotatable bonds limit", ("The imported flex residues have the maximum number of allowed rotatable \
bonds (%s).\n\nOnly rigid ligands will be accepted for the docking!" % (AutoDockMaxTORSDOF.get() )))
	FlexResTORSDOF.set( found_flex_tors )

	if len(LigandDictionary):
		tkMessageBox.showinfo("AutoDock rotatable bonds", ("The imported flex residues have %s rotatable bonds.\n\nThe maximum \
number of rotatable bonds for ligands will be set set to %s and the ligand set will be filtered with this \
value." % (found_flex_tors, AutoDockMaxTORSDOF.get()-found_flex_tors )  ))
	FilteringDefaults("TORSDOF")
	FilterLigands(True)
	if DEBUG:
		print "FLEX> found a total of %s rotatable bonds in the flexible residue" % found_flex_tors
	return True 
		


def EnableFlexFromFile():
	global Single_target_radio, Multi_target_radio, SingleTargetPanel, MultiTargetPanel, group_receptor1
	global group_receptor2, ResidueOrigin, receptorScrolledListBox 
	global SingleRecStatus,  FlexResFile, ImportFlexResPDBQT, FlexResFileNameLabel, FlexResListEntry
	global FlexResStatus, FlexResListSet,  DoFlex, ResidueStatus, ResidueStatusLoaded
	# Activate all buttons to load and display flex res filename
	ImportFlexResPDBQT.config(state=NORMAL)
	FlexResFileNameLabel.config(state=NORMAL)
	# Deactivate all buttons to select flex res filename
	FlexResListEntry.config(state = DISABLED)
	FlexResListSet.config(state = DISABLED)
	# Check if there was a previous filename defined 
	# and test the file again, else undefine 
	# the FlexResDefined (maybe activated from a selection of residues)
	if FlexResFileName.get() == '':
		FlexResDefined.set(False)

	ResidueStatus.set(ResidueStatusLoaded.get())
	try:
		FlexTorsionCount()
	except:
		pass
	try:
		TheCheck()
	except:
		return


def EnableFlexFromSel():
	global Single_target_radio, Multi_target_radio, SingleTargetPanel, MultiTargetPanel, group_receptor1
	global group_receptor2, ResidueOrigin, receptorScrolledListBox, SingleRecStatus,  FlexResFile, ImportFlexResPDBQT
	global FlexResFileNameLabel, FlexResListEntry, FlexResStatus,FlexResListSet,  DoFlex, ResidueStatus
	# Activate all buttons to load and display flex res filename
	ImportFlexResPDBQT.config(state=DISABLED)
	FlexResFileNameLabel.config(state=DISABLED)
	# Deactivate all buttons to select flex res filename
	FlexResListEntry.config(state = NORMAL)
	FlexResListSet.config(state = NORMAL)
	# Check if there was a previous selection defined and
	# test it again, else undefine the FlexResDefined (maybe activated from a filename)
	if not ListFlexResiduesNames.get() == '':
		FlexResDefined.set(False)
	ResidueStatus.set(ResidueStatusSelected.get())
	try:
		ParseFlexSelection()
	except:
		pass
	try:
		TheCheck()
	except:
		return


def ParseFlexSelection():
	verbose = False
	if not DoFlexFromWhat.get() == 2:
		return
	# figure out if the receptor is the single conformation or a multi_snapshot
	if RCstatus.get() == 0 and SingleReceptorSet.get():
		receptor_list = [RecFilename.get()]
	elif RCstatus.get() == 1 and MultiReceptorSet.get():
		receptor_list = receptorScrolledListBox.get('0', END)
	else:
		if RCstatus.get() == 0:
			SingleRecButton.flash()
		if RCstatus.get() == 1:
			AddAReceptorButton.flash()
		return

	found = []
	missing = []
	chain_list = []

	found_flex_tors = 0

	selection = ListFlexResiduesNames.get()
	selection = selection.replace(' ', '')
	selection = selection.split(',')
	# ARG9, B:THR276

	if not selection == ['']: #	empty residue list... don't waste my time, please...
		for receptor in receptor_list:
			# File opening
			if verbose or DEBUG: print "============> Checking receptor", receptor
			file = open(receptor, 'r')
			protein = file.readlines()
			file.close
			del found[:]

			for res in set(selection): # changed from "selection" to "set(selection)" to avoid duplicates
				FOUND = False
				residue = res
				if verbose or DEBUG: print "\nThis would be the residue", res
				res = res.split(':')
				if verbose or DEBUG: print res
				res_nam = res[-1][0:3]
				if verbose or DEBUG: print "residue name  =>", res_nam
				res_num = res[-1][3:]
				if verbose or DEBUG: print "residue numb  =>", res_num
				if res_num == '':
					if verbose or DEBUG: print "NO NUMBER SPECIFIED!"
					tkMessageBox.showwarning("Wrong residue(s) specification", "Residues must be specified using\
the following syntax.\nFor example, 'threonine 276' can be either:\n\n\tTHR276\n\t\
( any )\n\n\tB:THR276\n\t       ( chain B only )\n\nMultiple residues can be specified\
by separating them with a comma (',') as:\n\n\tTHR276, HIS229\n\n\tB:THR276, B:HIS229")
					FlexResDefined.set(False)
					TheCheck()
					return False
				if len(res) > 1: # there is a chain specification
					chain = res[-2]
					if verbose or DEBUG: print "chain         =>", chain
				else:
					chain = ''
				for line in protein:
					if line[0:4] == 'ATOM' or line[0:6] == 'HETATM':
						if res_nam == line[17:20].split()[0]:
							if res_num == line[22:26].split()[0]:
								if chain in line[21]:
									FOUND = True
									if verbose or DEBUG: print line # useful for debugging, do not remove!
									if line[21] not in chain_list:
										chain_list.append(line[21])
				if FOUND:
					if verbose or DEBUG: print "FOUND THE RESIDUE %s in %s" % (res, receptor)
					found.append([residue, ( len(chain_list) )])
					del chain_list[:]
				else:
					missing.append(residue)
					if verbose or DEBUG: print "XXXX this res is missing: ", res
					if verbose or DEBUG:	print "this is a window with an error of residue"
			if len(missing) > 0:
				if verbose or DEBUG: print "XXXX some residues are missing"
				if verbose or DEBUG: print "this is a window with an error of residue"
				if verbose or DEBUG: print missing
				msg_missing = '\n'
				for item in missing:
					msg_missing = msg_missing+"\t-> "+item+"\n"
				tkMessageBox.showwarning("Unable to find residue(s)", ("The following residue(s) \
are missing:\n"+msg_missing+"\n\n - Check the syntax (i.e. \'THR276', 'B:THR276' or 'B:THR276,B:HIS229')\n\n - Specify different residues.\n"))
				ResidueStatus.set("[ none ]") 
				FlexResDefined.set(False)
				TheCheck()
				return False
		if len(selection) == len(found):
			total = 0
			for i in range(len(found)):
				total = total + found[i][1]
			# The selection is copied into the variable used at the end
			FlexResSelected.set(ListFlexResiduesNames.get())
			# here goes the check torsions
			if not FlexTorsionCount():
				return False
			ResidueStatusSelected.set(( str(total)+" residue(s) selected [ "+ str(FlexResTORSDOF.get())+" rotatable bonds ]"))

			#EnableFlexFromSel() # TODO Possibly useless here...
			ResidueStatus.set(ResidueStatusSelected.get())
			FlexResDefined.set(True)

			TheCheck()
			return True
		else:
			FlexResDefined.set(False)
			ResidueStatusSelected.set("[ none ]")
			TheCheck()
			return False
	else: # empty the residue definition if no argument is present in the entry	
		if DEBUG: print "no residues"
		ResidueStatusSelected.set("[ none ]")
		ResidueStatus.set("[ none ]") 
		FlexResDefined.set(False)
		TheCheck()
		if DEBUG: print "again, no residues"
		return False



def MakeReceptorMenu():
	global Single_target_radio, Multi_target_radio, SingleTargetPanel, MultiTargetPanel, group_receptor1, group_receptor2, ResidueOrigin, receptorScrolledListBox,  FlexResFile, ImportFlexResPDBQT, FlexResFileName, FlexResFileNameLabel, FlexResList, FlexResListEntry, FlexResStatus, FlexResListSet, DoFlex, ResidueStatus, SingleRecFilenameLabel, SingleRecButton, AddAReceptorButton

	ReceptorRadioChoice = Pmw.Group( p2, tag_pyclass = None)
	ReceptorRadioChoice.pack()

	Single_target_radio = Radiobutton(ReceptorRadioChoice.interior(), text='Single target', value=0, variable=RCstatus, state=ACTIVE, command=ReceptorOptions)
	Multi_target_radio = Radiobutton(ReceptorRadioChoice.interior(), text='Multiple conformations', value=1, variable=RCstatus, command=ReceptorOptions)
	Single_target_radio.pack(anchor=NW, side = LEFT, expand = 0, padx = 5)
	Multi_target_radio.pack(anchor=NW, side = LEFT, expand = 0, padx = 5)

	# Group containing the structure(s) choices ###################################
	group_receptor1 = Pmw.Group(p2, tag_textvariable = TargetPDBQT)

	# Single receptor menu
	SingleTargetPanel = Frame(group_receptor1.interior(), relief=FLAT ) 
	SingleRecFilenameLabel = Label(SingleTargetPanel, textvariable = RecFilename)
	SingleRecFilenameLabel.pack()

	SingleRecButton = Button(SingleTargetPanel, text="Add receptor file...", command = openSingleReceptor)
	SingleRecButton.pack(expand=YES, anchor=CENTER, side=LEFT)
	
	# Multi-receptor menu
	MultiTargetPanel = Frame(group_receptor1.interior(), relief=FLAT)
	receptorScrolledListBox = Pmw.ScrolledListBox(MultiTargetPanel) #, hull_width = 800, hull_height = 200, usehullsize= 1) # THAT's A ugly workaround I should get rid of...
	receptorScrolledListBox.grid(row = 0, column = 0, sticky = N+W+E, columnspan = 10)
	AddAReceptorButton = Button(MultiTargetPanel, text='Add a structure...', command=openReceptor)
	AddAReceptorButton.grid(row = 1, column = 0, padx = 5)
	Button(MultiTargetPanel, text='Add a directory...', command=openReceptorDir).grid(row = 1, column = 1, padx = 5)
	Button(MultiTargetPanel, text='Remove a structure', command=removeReceptor).grid(row = 1, column = 2, padx = 5)
	Button(MultiTargetPanel, text='Remove all', command=removeAllReceptors).grid(row = 1, column = 3, padx = 5)

	group_receptor1.pack(fill = BOTH, expand = 1, padx = 10, pady = 10, anchor = N, side = TOP)


	# Group containing the flexible residues choice #######################################
	group_receptor2 = Pmw.Group(p2, tag_text = 'Flexible residues', tag_pyclass = Tkinter.Checkbutton, tag_variable = DoFlex, tag_command = SetFlexibleMode)
	group_receptor2.pack(fill = 'x', expand = 0, padx = 10, pady = 10, anchor = N, side = TOP)	


	FlexResFile = Radiobutton(group_receptor2.interior(), text='From file', value=1, variable=DoFlexFromWhat, command = EnableFlexFromFile)
	FlexResFile.grid(row = 0, column = 0, sticky = W)
	ImportFlexResPDBQT = Tkinter.Button(group_receptor2.interior(), text="Import PDBQT", command=SetFlexibleResidueFile)
	ImportFlexResPDBQT.grid(row = 0, column = 1, sticky = W)
	FlexResFileNameLabel = Label(group_receptor2.interior(), textvariable=FlexResFileName)
	FlexResFileNameLabel.grid(row = 0, column = 2, sticky = W)

	FlexResList = Radiobutton(group_receptor2.interior(), text='From selection', value=2, variable=DoFlexFromWhat, command = EnableFlexFromSel)
	#FlexResList.config(fg = 'red')
	FlexResList.grid(row = 1, column = 0, sticky = W)
	FlexResListEntry = Tkinter.Entry(group_receptor2.interior(), textvariable=ListFlexResiduesNames)
	FlexResListEntry.grid(row = 1, column = 1, sticky = W)
	FlexResListSet = Button(group_receptor2.interior(), text='Set', command = ParseFlexSelection)
	FlexResListSet.grid(row = 1, column = 2, sticky = W)
	FlexResStatus = Label(group_receptor2.interior(), textvariable = ResidueStatus) 
	FlexResStatus.grid(row = 2, column = 1, sticky = W, columnspan = 3)

	DefaultRec = Tkinter.Button(p2, text="PDBQT generation options", command = ReceptorImportOptions).pack()


def ReceptorImportOptions():

	global RecRepairOptions
	try:
		ReceptorOptionsWin.lift()
	except:
		ReceptorOptionsWin = Toplevel(root)
		ReceptorOptionsWin.title("Receptor PDBQT generation options")
		ReceptorOptionsWin.winfo_toplevel().resizable(NO,NO)
		ChargeFrame = Pmw.Group(ReceptorOptionsWin, tag_text = "Partial charges")
		Radiobutton(ChargeFrame.interior(), text="Add Gasteiger", variable = RecChargeSet, value = "gasteiger").grid(row = 0, column = 0, sticky = W, padx = 5) # Default
		Radiobutton(ChargeFrame.interior(), text="Keep original", variable = RecChargeSet, value = "").grid(row = 0, column = 1, sticky = W, padx = 5)
		ChargeFrame.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = N)

		CleanupFrame = Pmw.Group(ReceptorOptionsWin, tag_text = "Remove")
		Label(CleanupFrame.interior(), text = "yes").grid(row = 0, column = 1, sticky = W, pady = 2)
		Label(CleanupFrame.interior(), text = "no").grid(row = 0, column = 2, sticky = W, pady = 2)
		Label(CleanupFrame.interior(), text = "Non-polar H").grid(row = 1, column = 0, sticky = E, pady = 3)
		Radiobutton(CleanupFrame.interior(), variable = RecCleanNPH, value = "_nphs" ).grid(row = 1 , column = 1, sticky = N, pady = 3) 
		Radiobutton(CleanupFrame.interior(), variable = RecCleanNPH, value = "" ).grid(row = 1 , column = 2, sticky = N, pady = 3)
		Label(CleanupFrame.interior(), text = "Lone pairs").grid(row = 2, column = 0, sticky = E, pady = 3)
		Radiobutton(CleanupFrame.interior(), variable = RecCleanLP, value = "_lps" ).grid(row = 2 , column = 1, sticky = N , pady = 3) 
		Radiobutton(CleanupFrame.interior(), variable = RecCleanLP, value = "" ).grid(row = 2 , column = 2, sticky = N , pady = 3) 
		Label(CleanupFrame.interior(), text = "Water mol's").grid(row = 3, column = 0, sticky = E, pady = 3)
		Radiobutton(CleanupFrame.interior(), variable = RecCleanWAT, value = "_waters" ).grid(row = 3 , column = 1, sticky = N , pady = 3)
		Radiobutton(CleanupFrame.interior(), variable = RecCleanWAT, value = "" ).grid(row = 3 , column = 2, sticky = N , pady = 3)
		Label(CleanupFrame.interior(), text = "Not-standard res").grid(row = 4, column = 0, sticky = E, pady = 3)
		Radiobutton(CleanupFrame.interior(), variable = RecCleanStdRes, value = True ).grid(row = 4 , column = 1, sticky = N , pady = 3)
		Radiobutton(CleanupFrame.interior(), variable = RecCleanStdRes, value = False ).grid(row = 4 , column = 2, sticky = N , pady = 3)
		Label(CleanupFrame.interior(), text = "Alternate chains (B)").grid(row = 5, column = 0, sticky = E, pady = 3)
		Radiobutton(CleanupFrame.interior(), variable = RecDelAlternate, value = "deleteAltB" ).grid(row = 5 , column = 1, sticky = N , pady = 3)
		Radiobutton(CleanupFrame.interior(), variable = RecDelAlternate, value = "" ).grid(row = 5 , column = 2, sticky = N , pady = 3)
		CleanupFrame.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = N)

		RepairFrame = Pmw.Group(ReceptorOptionsWin, tag_text = "Structure repair")
		# label
		RecRepairOptions = OptionMenu(RepairFrame.interior(), RecRepairOptionsSet, "none", "rebuild bonds", "add H", "add H (if missing)", "rebuild bonds + add H")
		RecRepairOptions.grid(row = 4, padx = 10, sticky = N)
		RepairFrame.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = N)

		Tkinter.Button(ReceptorOptionsWin, text="OK", command = ReceptorOptionsWin.destroy, width = 20 ).grid(row = 9, column = 0, sticky = S, columnspan = 2, pady = 10, padx = 10)
		Tkinter.Button(ReceptorOptionsWin, text="Set defaults", command = ReceptorOptionsDefault, width = 10).grid(row = 0, column = 0, columnspan = 3, sticky = S, pady = 10, padx = 10)


def ReceptorOptionsDefault():
	RecChargeSet.set('gasteiger')
	RecCleanNPH.set('_nphs')
	RecCleanLP.set('_lps')
	RecCleanWAT.set('_waters')
	RecCleanStdRes.set(False)
	RecDelAlternate.set('')
	RecRepairOptionsSet.set('add H (if missing)')




def ReceptorOptions():
	verbose = False
	global SingleTargetPanel, MultiTargetPanel, group_receptor1, group_receptor2, RCstatus, FlexResFile, ImportFlexResPDBQT, FlexResFileNameLabel, FlexResList, FlexResListEntry, AutoGridWhen1, AutoGridWhen2, AutoGridWhen3 #, TargetPDBQT

	if RCstatus.get() == 0: # Single Target
		if verbose: print "I'm running the RCstatus with this value:", RCstatus.get()
		MultiTargetPanel.forget()
		SingleTargetPanel.pack(expand = YES, fill = 'x')
		TargetPDBQT.set("Receptor structure")
		if DoFlex.get() == 1:
			FlexResFile.config(state=NORMAL)
			ImportFlexResPDBQT.config(state=NORMAL)
			FlexResFileNameLabel.config(state=NORMAL)
			ParseFlexSelection()
		if AutoGridWhen2:
			if not system == "Windows":
				AutoGridWhen2.config(state = NORMAL)

		if AutoGridWhen3 and TotalAcceptedLigands.get():
			AutoGridWhen3.config(state = NORMAL)
		
	if RCstatus.get() == 1: # Multiple Targets 
		if verbose: print "I'm running the RCstatus with this value:", RCstatus.get()
		SingleTargetPanel.forget()
		FlexResFile.config(state=DISABLED)
		FlexResFileNameLabel.config(state=DISABLED)
		ImportFlexResPDBQT.config(state=DISABLED)
		countReceptors()
		if DoFlex.get() == 1:
			ParseFlexSelection()

		MultiTargetPanel.pack(expand = YES, fill = BOTH)
		if AutoGridWhen3:
			AutoGridWhen3.config(state = DISABLED)
	try:
		TheCheck()
	except:
		return

def SetFlexibleMode():
	global Single_target_radio, Multi_target_radio, SingleTargetPanel, MultiTargetPanel, group_receptor1, group_receptor2, ResidueOrigin, receptorScrolledListBox, SingleRecStatus,  FlexResFile, ImportFlexResPDBQT, FlexResFileNameLabel, FlexResListEntry, FlexResStatus,FlexResListSet,  DoFlex

	# To initialize the default flexible option as "from file"
	if DoFlexFromWhat.get() == -1:
		FlexResFile.invoke()

	if DoFlex.get() == 0:
		FlexResFile.config(state = DISABLED)
		ImportFlexResPDBQT.config(state=DISABLED)
		FlexResFileNameLabel.config(state=DISABLED)
		FlexResList.config(state = DISABLED)
		FlexResListEntry.config(state = DISABLED)
		FlexResListSet.config(state = DISABLED)
		FlexResStatus.config(state = DISABLED)
		FlexResListSet.config(state = DISABLED)
		FlexTorsionCount(force = True)
		try:
			TheCheck()
		except:
			pass
	if DoFlex.get() == 1:
		if RCstatus.get() == 0: # Single receptor mode enable the "From file button"
			FlexResFile.config(state = NORMAL)
			ImportFlexResPDBQT.config(state=NORMAL)
			FlexResFileNameLabel.config(state=NORMAL)
			FlexResListSet.config(state = NORMAL)
		FlexResList.config(state = NORMAL)
		FlexResListEntry.config(state = NORMAL)
		FlexResStatus.config(state = NORMAL)
		FlexResListSet.config(state = NORMAL)
		FlexResListSet.config(state = NORMAL)
		FlexTorsionCount()
		try:
			TheCheck()
		except:
			pass


###### Estetical tricks

def FontSizeInc():
	pass
	# TODO

def FontSizeDec():
	pass
	# TODO

#########################
### GPF RELATED FUNCTIONS

def MakeGPFMenu():
	global CacheMapFrame, GPFframe, CacheMapHandleNow, CacheMapHandle, GPFcontent, GPFedit, GPFsave, GPFFilenameLabel, GPFload, CacheMapDir, CacheMapDirLabel, MapFolderList

	# The GPF management facility is contained here in GPFframe
	# GPF edit group  
	GPFframe = Pmw.Group(p3, tag_text = 'GPF template')
	GPFload = Button(GPFframe.interior(), text='Load GPF template...', command=opengpf)
	GPFload.grid(row = 0, column = 0, sticky = W, columnspan = 1)
	GPFedit = Button(GPFframe.interior(), text='Edit', command=editGPF, state = DISABLED, width = 13)
	GPFedit.grid(row = 2, column = 0, sticky = W)
	GPFsave = Button(GPFframe.interior(), text='Apply changes', command=saveGPFchanges)#, state = DISABLED)
	GPFFilenameLabel = Label(GPFframe.interior(), textvariable=GPFfilename, state = DISABLED)
	GPFFilenameLabel.grid(row = 0, column = 1, sticky = E)
	# GPF Text editor
	GPFcontent = Text(GPFframe.interior(), height=22, width = 100)
	GPFscroll = Scrollbar(GPFframe.interior(), command=GPFcontent.yview)
	GPFscroll.grid(row = 1, column = 3, sticky = N+S)
	GPFcontent.configure(yscrollcommand=GPFscroll.set)
	GPFcontent.grid(row = 1, column = 0, columnspan = 3, sticky = N+S+W+E)
	GPFcontent.config(fg = 'black', font = ("Courier", 11, "normal"))

	CacheMapHandleNow = Pmw.Group(GPFframe.interior(), tag_text="Cached maps")
	CacheMapOptionsNow = OptionMenu(CacheMapHandleNow.interior(), CacheMapPolicy, "Make copies [ use more disk space ]", "Make symbolic links [ save disk space ]")
	CacheMapPolicy.set('Make copies [ use more disk space ]')
	CacheMapOptionsNow.grid(row = 1, column = 3, columnspan = 2)


	# The cached maps management facility is contained here in CacheMapFrame
	# Cached maps group	
	CacheMapFrame = Pmw.Group(p3, tag_text = 'Pre-calculated maps')
	CacheMapDir = Button(CacheMapFrame.interior(), text='Select the cached maps directory', command=opendirMaps) #, state = DISABLED)
	CacheMapDir.grid(row = 0, column = 0)
	CacheMapDirLabel = Label(CacheMapFrame.interior(), textvariable = CacheMapDirName, state = DISABLED)
	CacheMapDirLabel.grid(row = 0, column = 1)
	# Maps folder browser
	MapFolderScroll = Scrollbar(CacheMapFrame.interior())
	MapFolderList = Listbox(CacheMapFrame.interior(), yscrollcommand = MapFolderScroll.set, width = 90)
	MapFolderScroll.config(command = MapFolderList.yview )
	# TODO Add an orizontal scroll list?
	MapFolderScroll.grid(row = 1, column = 3, sticky = N+S)
	MapFolderList.grid(row = 1, column = 0, sticky = W+E, columnspan = 3)
	MapFolderList.insert(END, "[no map directory defined yet... ]")
	MapFolderScroll = Scrollbar(CacheMapFrame.interior(), command = MapFolderList.yview)

	CacheMapHandle = Pmw.Group(CacheMapFrame.interior(), tag_text="Cached maps")
	CacheMapOptions = OptionMenu(CacheMapHandle.interior(), CacheMapPolicy, "Make copies [ use more disk space ]", "Make symbolic links [ save disk space ]")
	CacheMapPolicy.set('Make copies [ use more disk space ]')
	CacheMapOptions.grid(row = 5, column = 1, columnspan = 2)
	CacheMapHandle.grid(row = 2, column = 0, columnspan = 2)

	if system == "Windows":
		CacheMapOptionsNow.config(state = DISABLED)
		CacheMapOptions.config(state = DISABLED)

def MapMenu():
	for item in CacheMapFrame, GPFframe, CacheMapHandle:
		if item:
				item.forget()
		try: 
			if AGoptions:
				AGoptions.forget()
		except:
			pass
		if CacheMapHandleNow:
			CacheMapHandleNow.grid_forget()
	state = MapSource.get()
	if state == 0: # Use the GPF to run AutoGrid in all the jobs
		GPFframe.pack(fill = BOTH, expand = 1, padx = 10, pady = 3, side = TOP, anchor = N)
	if state == 1: # Use the GPF to run AutoGrid now, then cache the maps
		AGoptions.pack()
		GPFframe.pack(fill = BOTH, expand = 1, padx = 10, pady = 10)
		CacheMapHandleNow.grid(row = 2, column = 1, sticky = W, columnspan = 1)
		if not AutoGridBin.get():
			WhichAutoGrid()
	if state == 2: # Use the maps in the cache folder
		CacheMapFrame.pack(fill = BOTH, expand = 1, padx = 10, pady = 10)
	try:
		TheCheck()
	except:
		pass


def setGPFtags(): # Inspired by:  http://effbot.org/tkinterbook/text.htm
	GPFcontent.tag_remove('keyword', '1.0', END)
	GPFcontent.tag_remove('comment', '1.0', END)
	for keyw in GPFkeywords:
		idx = '1.0'
		while 1:
			idx = GPFcontent.search(keyw, idx, stopindex=END)
			if not idx: break
			lastidx = '%s+%dc' % (idx, len(keyw))
			if idx.split('.')[1] == "0":
				GPFcontent.tag_add('keyword', idx, lastidx)
			idx = lastidx
		GPFcontent.tag_config('keyword', font = ("Courier", 11, "bold"), foreground = 'blue')
	idx = '1.0'
	while 1:
		idx = GPFcontent.search("#", idx, stopindex=END)
		if not idx: break
		lastidx = idx.split('.')[0]+".end"
		GPFcontent.tag_add('comment', idx, lastidx)
		idx = lastidx
		GPFcontent.tag_config('comment', foreground = 'gray')

def removeGPFtags(): # Inspired by:  http://effbot.org/tkinterbook/text.htm
	GPFcontent.tag_remove('keyword', '1.0', END)
	GPFcontent.tag_remove('comment', '1.0', END)

def opengpf():
	# Provides:
	#  GPFlines = list of lines contained in the GPF (=> prepare_x scripts)
	#  GPFParameterFile = filename of the parameter file required by the GPF (if found)
	#
	global GPFlines, GPFcontent, GPFedit, GPFsave, GPFFilenameLabel, GPFParameterFile

	GPFcontent.tag_config("npts", foreground="red")
	gpfFile = askopenfilename(filetypes=[("Grid Parameter File", "*.gpf")])
	if DEBUG: print gpfFile
	
	if gpfFile:
		gpftemplate = gpfFile
		ask_for_param_file = 0
		GPFParameterFile.set("")
		GPFcontent.config(state = NORMAL)
		GPFcontent.delete(1.0, END) 
		for line in open(gpfFile, 'r'): # surprisingly, adding the text to the editor worked at the first attempt....
			if line[0:14] == "parameter_file":
				if DEBUG: print "I found a param file in %s!" % gpfFile
				ask_for_param_file = 1
				param_file_name = line.split()[1]
			GPFcontent.insert(END, line)
		GPFlines = GPFcontent.get(1.0, END)
		GPFfilename.set(gpfFile)
		GPFFilenameLabel.config(state = NORMAL)
		if ask_for_param_file == 1:
			tkMessageBox.showwarning("Parameter file required", "A parameter file is required by the GPF:\n => %s \n The filename location must be specified..." % param_file_name)
			askGPFParamFile(param_file_name)
		else:
			GPFcontent.config(state = DISABLED)
			GPFedit.config(state = ACTIVE)
	setGPFtags()
	TheCheck()

def askGPFParamFile(filename):
	# ask the user the location of the ADX.X_xxxx.dat file found in the GPF
	#
	# Provides:
	#  defines the GPFParameterFile
	keepasking = True
	while keepasking == True:
		parameter_filename = askopenfilename(filetypes=[("AutoDock Parameter File", filename)])
		if parameter_filename:
			GPFParameterFile.set(parameter_filename) 
			keepasking = False
			GPFcontent.config(state = DISABLED)
			GPFedit.config(state = ACTIVE)
			return True
		else:
			answer = tkMessageBox.askquestion('Warning', 'The file is required by the GPF.\nDo you want to define it?')
			if answer == "no":
				tkMessageBox.showwarning("Error", "The file is essential for this GPF.\nRe-import the GPF and set the correct parameter file.")
				# empty the GPF buffer and the entry in GPF the editor
				GPFlines = None
				GPFcontent.delete(1.0, END) 
				GPFfilename.set("[ no GPF loaded ]")
				keepasking = False
				GPFcontent.config(state = DISABLED)
				GPFedit.config(state = DISABLED)
				return False

def editGPF():
	GPFcontent.config(state = NORMAL)
	GPFedit.grid_forget()
	GPFload.config(state = DISABLED)
	GPFcontent.config(fg = 'red', font = ("Courier", 11, "bold"))
	GPFsave.config(fg = 'red', width = 13)
	GPFsave.grid(row = 2, column = 0, sticky = W)
	removeGPFtags()

def saveGPFchanges():
	GPFlines = GPFcontent.get(1.0, END)
	GPFload.config(state = NORMAL)
	GPFcontent.config(fg = 'black', font = ("Courier", 11, "normal"))
	GPFcontent.config(state = DISABLED)
	GPFsave.grid_forget()
	setGPFtags() 
	GPFedit.grid(row = 2, column = 0, sticky = W)
	setGPFtags()

def disableGPF(): 
	GPFcontent.config(fg = 'gray', font = ("Courier", 11, "normal"))
	GPFcontent.config(state = DISABLED)
	GPFedit.config(state = DISABLED)
	GPFload.config(state = DISABLED)
	GPFFilenameLabel.config(state = DISABLED)
	if not CacheMapDirName.get() == "[ none ]":
		CacheMapDir.config(state = NORMAL)
	else:
		CacheMapDir.config(state = NORMAL)
		CacheMapDir.flash()

def enableGPF():
	GPFcontent.config(fg = 'black', font = ("Courier", 11, "normal"))
	GPFcontent.config(state = NORMAL)
	GPFedit.config(state = NORMAL)
	GPFload.config(state = NORMAL)
	CacheMapDir.config(state = DISABLED)
	setGPFtags()

def opendirMaps(mapfolder = None): 
	# Check map integrity and presence of all maps for all atom types
	#
	#
	#
	global LIGAND_SET , mapDir 
	FldFound, XyzFound = False, False
	accepted_maps = []
	if not mapfolder:
		mapDir = askdirectory(title = "Select the dir containing the grid maps...")
	else:
		mapDir = mapfolder
	if mapDir:
		MapFolderList.delete(0, END)
		DoCachedMaps.set(False)
		# collect all the atomic maps
		mapFiles = glob.glob(os.path.join(mapDir, "*.map"))
		# add the *.fld and *.xyz maps
		for extra_map in glob.glob(os.path.join(mapDir, "*.maps.*")):
			mapFiles.append(extra_map)
		# Prune possible dirs matching "*map*" pattern
 		for item in mapFiles:
			if os.path.isdir(item):
				del mapFiles[mapFiles.index(item)]

		if len(mapFiles):
			for map in mapFiles:
				if map[-8:] == "maps.fld":
					FldFound = True
				if map[-8:] == "maps.xyz":
					XyzFound = True
		if not FldFound: # manage possible errors
			tkMessageBox.showerror("Map file not found!", "The .fld map is missing.\nSelect another directory.")
		elif not XyzFound:
			tkMessageBox.showerror("Map file not found!", "The .xyz map is missing.\nSelect another directory.")
		# ...then check for necessary atom types if ligands have been set
		if XyzFound and FldFound:
			CheckFolderMap(mapFiles)
		TheCheck()

def CheckFolderMap(MapFileList):
	# Check for mapfiles for all the atom types (+e +d) that
	# are found in the ligands of the Great Book of Ligands
	# and assure that all the maps are consistent
	# (same parameters)
	MissingMaps = []
	FolderIsOk = True
	MapConsistency = True
	del MissingMaps[:]
	missing_files = []
	
	receptor_stem = (os.path.basename(RecFilename.get())).split(".")[0]
	if DEBUG: print "CheckFolderMap> RECEPTOR_STEM", receptor_stem
	# Check for all atom types maps
	for atype in AtypeList:
		if AtypeList[atype][0] > 0:
			missing = 1
			map_file_name = receptor_stem+"."+atype+".map"
			print "MISSING", map_file_name
			for item in MapFileList:
				print "CHECK ITEM", item
				if map_file_name in item:
					missing = 0
					break
			else:
				print "\t %s is not in %s" % (map_file_name, item)
				missing_files.append(map_file_name)
	print MapFileList
	if missing_files:
		miss_text = ""
		for file in missing_files:
			miss_text += "\n\t"+file
		tkMessageBox.showerror("Missing maps", ("The following maps are missing:"+miss_text+"\n\nPlease specify another directory."))
		MapFolderList.delete(0, END)
		DoCachedMaps.set(False)
		CacheMapDirName.set("[ none ]")
		CacheMapDirLabel.config(state = DISABLED)
		InfoMessage.set("Some maps are missing.")
		return False

	#GetAtypes(selection = )
	# Selection mode
	if DoFlexFromWhat.get() == 2 and not ListFlexResiduesNames.get() == "":
		for res_type in ListFlexResiduesNames.get():
			flex_types += ResidueRotatableBondTable[res_type][0]
		for atype in AtypeList:
			if AtypeList[atype][0] > 0:
				missing = 1
				for map in MapFileList:
					if atype == map.split(".")[-2]: 
						missing = 0
				if missing == 1:   
					MissingMaps.append(atype)

	# Check for number of points
	if len(MissingMaps) == 0:
		mapheader = []
		mapheader_checking = []
		try:
			for file in MapFileList:
			    if file[-3:] == "map":
				MAP = open(file, 'r')
				# first map populates the map reference dictionary
				if len(mapheader) == 0:
					line = MAP.next()
					for count in '123456':
						mapheader.append(line)
						line = MAP.next()
					MAP.close()
				else:
					line = MAP.next()
					for count in '123456':
						mapheader_checking.append(line)
						line = MAP.next()
					MAP.close()
					if not mapheader == mapheader_checking:
						MapConsistency == False
					else:
						MapConsistency == True
						del mapheader_checking[:]
		except:
			if DEBUG: print "CheckFolderMap> Houston, we've got a problem in checking maps..."
			MapConsistency = False

		if MapConsistency:
			for item in MapFileList:
				MapFolderList.insert('end', item)
				CacheMapDirName.set(mapDir)
				CacheMapDirLabel.config(state = NORMAL)
			DoCachedMaps.set(True)
			return True
		else:
			tkMessageBox.showwarning("Map files are not coherent!", "The maps doesn't have the same properties\
							(i.e npoints, resolution...). Please check them or select another folder")
			CacheMapDirName.set("[ none ]")
			CacheMapDirLabel.config(state = DISABLED)
			AutoGridWhen1.invoke() # Select the default as "Run AG in each job"
			return False
	else: # One or more maps are missing...
		MapFolderList.delete(0, END)
		DoCachedMaps.set(False)
		message_missing = ""
		for mmap in MissingMaps:
			message_missing = message_missing+"==> "+mmap+"\n"

		CacheMapDirName.set("[ none ]")
		CacheMapDirLabel.config(state = DISABLED)
		tkMessageBox.showwarning("Map file not found!", "The following maps are missing:\n\n%s\nRe-define \
						the directory or use different ligands."% message_missing)
		AutoGridWhen1.invoke() # Select the default as "Run AG in each job"
		return False


def prepareGPF(output_gpf_filename, receptor_filename, ligand_filename = None, atom_types = None , flexres_filename = None):

	# get the vales from the scrollbox
	# parse keyword+values
	# generate keyword="value[,value,value]"
	# 
	# warning, this is limited to the keywords listed below
	# but not others [ to be improved ]
	# parse the GPF for keywords
	# "input" can be either a ligand or a the dictionary of the atom types
	#

	parameters = []

	list_filename = gpf_filename = None
	directory = None
	verbose = None
	center_on_ligand = False
	size_box_to_include_ligand = False

	verbose = False

	parameters = []
	if verbose or DEBUG:
			print "I'm trying to generate the GPF using the following params:"
			print "output gpf", output_gpf_filename
			print "receptor_filename", receptor_filename
			print "ligand_filename", ligand_filename
			print "atom types", atom_types
			print "flexres_filename", flexres_filename

	list_of_atom_types = []

	if atom_types:
		if verbose or DEBUG: print "I'm going to use these atom types to generate the maps...", atom_types
		line = "ligand_types="
		for atype in atom_types:
			if atype not in list_of_atom_types:
				line = line+atype+","
				list_of_atom_types.append(atype)
		line = line.rstrip(',')
		parameters.append(line)
	if verbose: print "This is the command line", line

	# add potential parameter file line
	if not GPFParameterFile.get() == "":
		parameters.append( ( "parameter_file="+GPFParameterFile.get() ) )


	# read the imported GPF and parse the keywords
	gpf_lines = GPFcontent.get(1.0, END)

	if verbose: print "############################################ GPF ####################\n",gpf_lines, "\n###################################"

	for line in gpf_lines.split('\n'):
		if verbose: print "======> PROCESSING: ", line
		if not line.strip(): # get rid of empty lines
			continue
		else:
			clean_line = line.split("#")[0] # get rid of comments
			clean_line = clean_line.split(" ", 1)
			keyword = clean_line[0]
			try:
				argument = clean_line[1]
			except:
				pass
			if verbose: print " keyword = |"+keyword+"|, value = |"+argument+"|"
			# try: ?

			if keyword == "npts":
				value = argument.split()
				line = keyword+"="+value[0]+","+value[1]+","+value[2]
				if verbose: print "=> found npts, generated this xxxx:", line
				parameters.append(line)
				
			if keyword == "parameter_file":
				value = argument.replace(" ", "")
				line = keyword+"="+value
				if verbose: print "=> found parameter file, generated this xxxx:", line

			if keyword == "spacing":
				value = argument.replace(" ", "")
				line = keyword+"="+value
				if verbose: print "=> found spacing, generated this xxxx:", line
				parameters.append(line)

			if keyword == "gridcenter":
				value = argument.split()
				line = keyword+"="+value[0]+" "+value[1]+" "+value[2]
				if verbose: print "=> found gridcenter, generated this xxxx:", line
				parameters.append(line)

			if keyword == "smooth":
				value = argument.replace(" ", "")
				line = keyword+"="+value
				if verbose: print "=> found smooth, generated this xxxx:", line
				parameters.append(line)

			if keyword == "dielectric":
				value = argument.replace(" ", "")
				line = keyword+"='"+value+"'"
				if verbose: print "=> found dielectric, generated this xxxx:", line
				parameters.append(line)
	if verbose: print parameters

	gpfm = GridParameter4FileMaker(size_box_to_include_ligand=False,verbose=False)

	if ligand_filename:
		gpfm.set_ligand(ligand_filename)
	gpfm.set_receptor(receptor_filename)

	if flexres_filename:
		flexmol = Read(flexres_filename)[0]
		flexres_types = flexmol.allAtoms.autodock_element
		lig_types = gpfm.gpo['ligand_types']['value'].split()
		all_types = lig_types
		for t in flexres_types:
			if t not in all_types: 
				all_types.append(t)
		all_types_string = all_types[0]
		if len(all_types)>1:
			for t in all_types[1:]:
				all_types_string = all_types_string + " " + t
		gpfm.gpo['ligand_types']['value'] = all_types_string 
	for p in parameters:
		key,newvalue = string.split(p, '=')
		kw = {key:newvalue}
		apply(gpfm.set_grid_parameters, (), kw)
	gpfm.write_gpf(output_gpf_filename)	
	return True

def docking_setup_interface(event):
	global Info, numGen, EnEval, simple_settings, simple_settings_info, EnEval, OpenDPF, DPF_group, docking_set, CheckTDOF, CheckVOL, complex_gen_info, complex_eval_info, DPF_INFO, InfoFrame, dockMenuSettings
	global DPFcontent, DPFscroll, DPFedit, DPFsave, DPFfilename, DPFFilenameLabel, simple_settings_info
	global DPFgroupTemplate, DPFgroupSimple, DPFgroupComplex, DPFgroupSmart

	if not DPFgroupTemplate:
		DPFgroupTemplate = Pmw.Group(p4, tag_text = 'DPF template')
	if not DPFgroupSimple:
		DPFgroupSimple = Pmw.Group(p4, tag_text = 'DPF simple settings')
	if not DPFgroupComplex:
		DPFgroupComplex = Pmw.Group(p4, tag_text = 'DPF manual settings')
	if not DPFgroupSmart:
		DPFgroupSmart = Pmw.Group(p4, tag_text = 'SmartDPF Settings')
	DPFgroupNone = Pmw.Group(p4, tag_pyclass = None) # UGLY, VERY UGLY WORKAROUND
	DPFgroupTemplate.forget()
	DPFgroupSimple.forget()
	DPFgroupComplex.forget()
	DPFgroupSmart.forget()

	if not dockMenuSettings:
		dockMenuSettings = OptionMenu(p4, docking_set, "From template...", command=docking_setup_interface)
		dockMenuSettings.pack()
	if not docking_set.get(): # == Null:
		docking_set.set("[ select docking setup ]") # default value
	if docking_set.get() == "From template...":
		OpenDPF = Button(DPFgroupTemplate.interior(), text='Load DPF template...', command=opendpf)
		DPFedit = Button(DPFgroupTemplate.interior(), text='Edit', command=editDPF, state = DISABLED, width = 13)
		DPFsave = Button(DPFgroupTemplate.interior(), text='Apply changes', command=saveDPFchanges)
		DPFFilenameLabel = Label(DPFgroupTemplate.interior(), textvariable=DPFfilename, state = DISABLED)

		DPFdefault = Button(DPFgroupTemplate.interior(), text='Generate default DPF', command = MkDefaultDPF)


		# DPF Text editor
		if not DPFcontent:
			DPFcontent = Text(DPFgroupTemplate.interior(), height=22, width = 100)
		DPFscroll = Scrollbar(DPFgroupTemplate.interior(), command=DPFcontent.yview)
		DPFcontent.configure(yscrollcommand=DPFscroll.set)
		DPFcontent.config(fg = 'black', font = ("Courier", 11, "normal"))
		OpenDPF.grid(row = 0, column = 0, sticky = W)
		DPFedit.grid(row = 3, column = 0, sticky = W)
		DPFFilenameLabel.grid(row = 0, column = 1, sticky = E)
		DPFdefault.grid(row = 0, column = 2, sticky = E)

		DPFscroll.grid(row = 2, column = 3, sticky = N+S)
		DPFcontent.grid(row = 2, column = 0, columnspan = 3, sticky = N+S+W+E)
		DPFgroupTemplate.pack()
	DPFgroupNone.pack_forget()


def MkDefaultDPF():
	# Substitute the current content of the DPF editor
	# with the canonical DPF with all default values
	# (as from ADT)
	if len(DPFcontent.get(1.0, END)) > 1:
		if not tkMessageBox.askokcancel("Default DPF", "The default set of parameters will overwrite the current DPF.\n\n\
Are you sure?"):
			return
	DPFcontent.config(state = NORMAL)
	DPFcontent.delete(1.0, END) 
	DPFfilename.set(" AutoDock default ")
	DPFFilenameLabel.config(state = DISABLED)
	DPFcontent.insert(END, default_docking_parameter_file)
	DPFedit.config(state = NORMAL)
	setDPFtags()
	TheCheck()
	return

	

def setDPFtags(): 
	DPFcontent.tag_remove('keyword', '1.0', END)
	DPFcontent.tag_remove('comment', '1.0', END)
	for keyw in DPFkeywords:
		idx = '1.0'
		while 1:
			idx = DPFcontent.search(keyw, idx, stopindex=END)
			if not idx: break
			lastidx = '%s+%dc' % (idx, len(keyw))
			if idx.split('.')[1] == "0":
				DPFcontent.tag_add('keyword', idx, lastidx)
			idx = lastidx
		DPFcontent.tag_config('keyword', font = ("Courier", 11, "bold"), foreground = 'blue')
	idx = '1.0'
	while 1:
		idx = DPFcontent.search("#", idx, stopindex=END)
		if not idx: break
		lastidx = idx.split('.')[0]+".end"
		DPFcontent.tag_add('comment', idx, lastidx)
		idx = lastidx
		DPFcontent.tag_config('comment', foreground = 'gray')

def removeDPFtags(): 
	DPFcontent.tag_remove('keyword', '1.0', END)
	DPFcontent.tag_remove('comment', '1.0', END)

def opendpf():
	# Provides:
	#  GPFlines = list of lines contained in the GPF (=> prepare_x scripts)
	#  GPFParameterFile = filename of the parameter file required by the GPF (if found)
	#
	global DPFlines, DPFcontent, DPFedit, DPFsave, DPFFilenameLabel, DPFParameterFile

	dpfFile = askopenfilename(filetypes=[("Docking Parameter File", "*.dpf")])
	if DEBUG: print dpfFile
	if dpfFile:
		dpftemplate = dpfFile
		ask_for_param_file = 0
		DPFParameterFile.set("")
		DPFcontent.config(state = NORMAL)
		DPFcontent.delete(1.0, END) 
		for line in open(dpfFile, 'r'):
			if line[0:14] == "parameter_file":
				print "I found a param file!"
				ask_for_param_file = 1 
				param_file_name = line.split()[1]
			DPFcontent.insert(END, line)
		DPFlines = DPFcontent.get(1.0, END)
		DPFfilename.set(dpfFile)
		DPFFilenameLabel.config(state = NORMAL)
		if ask_for_param_file == 1:
			tkMessageBox.showwarning("Parameter file required", "A parameter file is required by the DPF:\n => %s \n The filename location must be specified..." % param_file_name)
			askDPFParamFile(param_file_name)
		else:
			DPFcontent.config(state = DISABLED)
			DPFedit.config(state = NORMAL)
	setDPFtags()
	TheCheck()

def editDPF():
	DPFcontent.config(state = NORMAL)
	DPFedit.grid_forget()
	DPFcontent.config(fg = 'red', font = ("Courier", 11, "bold"))
	OpenDPF.config(state = DISABLED)
	DPFsave.config(fg = 'red', width = 13)
	DPFsave.grid(row = 3, column = 0, sticky = W)
	removeDPFtags()

def saveDPFchanges():
	DPFlines = DPFcontent.get(1.0, END)
	DPFcontent.config(fg = 'black', font = ("Courier", 11, "normal"))
	DPFcontent.config(state = DISABLED)
	OpenDPF.config(state = NORMAL)
	DPFsave.grid_forget()
	DPFedit.grid(row = 3, column = 0, sticky = W)
	setDPFtags()


def askDPFParamFile(filename):
	# ask the user the location of the ADX.X_xxxx.dat file found in the DPF
	#
	# Provides:
	#  defines the GPFParameterFile
	keepasking = True
	while keepasking == True:
		parameter_filename = askopenfilename(filetypes=[("AutoDock Parameter File", filename)])
		if parameter_filename:
			DPFParameterFile.set(parameter_filename)
			keepasking = False
			DPFcontent.config(state = DISABLED)
			DPFedit.config(state = NORMAL)
			break
		else:
			answer = tkMessageBox.askquestion('Warning', 'The file is required by the DPF.\nDo you want to define it?')
			if answer == "no":
				tkMessageBox.showwarning("Error", "The file is essential for this DPF.\nRe-import the DPF and set the correct parameter file.")
				# empty the GPF buffer and the entry in GPF the editor
				DPFlines = None
		    		DPFcontent.delete(1.0, END) 
				DPFfilename.set("[ no DPF loaded ]")
				DPFFilenameLabel.config(state = DISABLED)
				DPFedit.config(state = DISABLED)
				keepasking = False

##################################### DPF CLASS

class DockingParameter42FileMaker:
	"""Accept a <ligand>.pdbqt and <receptor>.pdbqt and create
	<ligand>_<receptor>42.dpf
	"""

	def __init__(self, verbose = None):
		self.verbose = verbose
		self.dpo = DockingParameters()


	def getTypes(self, molecule):
		if not len(molecule.allAtoms.bonds[0]):
			molecule.buildBondsByDistance()
		ad4_typer = AutoDock4_AtomTyper(verbose=self.verbose)
		ad4_typer.setAutoDockElements(molecule)
		dict = {}
		for a in molecule.allAtoms:
			dict[a.autodock_element] = 1
		d_types = dict.keys()
		d_types.sort()
		mol_types = d_types[0]
		for t in d_types[1:]:
			mol_types = mol_types + " " + t
		if self.verbose: print "end of getTypes: types=", mol_types, ' class=', mol_types.__class__
		return mol_types


	def set_write_all(self, value):
		verbose = self.verbose
		self.dpo['write_all_flag']['value'] = True
		if verbose: print "set write_all_flag to", self.dpo['write_all_flag']['value']


	def set_ligand(self, ligand_filename): 
		verbose = self.verbose
		self.ligand_filename = os.path.basename(ligand_filename)
		if verbose: print "set ligand_filename to", self.ligand_filename
		self.dpo.set_ligand(ligand_filename)
		#expect a filename like ind.out.pdbq: get 'ind' from it
		self.ligand_stem = string.split(self.ligand_filename,'.')[0]
		if verbose: print "set ligand_stem to", self.ligand_stem
		self.ligand = Read(ligand_filename)[0]
		if self.ligand==None:
			print 'ERROR reading: ', ligand_filename
			return 
		if verbose: print "read ", self.ligand.name
		#set dpo:
		#move
		self.dpo['move']['value'] = self.ligand_filename
		if verbose: print "set move to ", self.dpo['move']['value']
		#ndihe
		#assumes ligand has torTree
		self.dpo['ndihe']['value'] = self.ligand.parser.keys.count("BRANCH")
		#self.dpo['ndihe']['value'] = len(self.ligand.torTree.torsionMap)
		if verbose: print "set ndihe to ", self.dpo['ndihe']['value']
		#torsdof
		#caution dpo['torsdof4']['value'] is a list [ndihe, 0.274]
		try:
			self.dpo['torsdof4']['value'][0] = self.ligand.TORSDOF
		except:
			print 'setting torsdof to ligand.ndihe=', self.ligand.ndihe
			self.dpo['torsdof4']['value'][0] = self.ligand.ndihe
		if verbose: print "set torsdof4 to ", self.dpo['torsdof4']['value']
		#types
		self.ligand.types = self.getTypes(self.ligand)
		self.dpo['ligand_types']['value'] = self.ligand.types
		if verbose: print "set types to ", self.dpo['ligand_types']['value']
		#about
		self.ligand.getCenter() 
		cen = self.ligand.center
		self.dpo['about']['value'] =  [round(cen[0],4), round(cen[1],4),\
										round(cen[2],4)]
		if verbose: print "set about to ", self.dpo['about']['value']
		

	def set_receptor(self, receptor_filename):
		self.receptor_filename = os.path.basename(receptor_filename)
		self.receptor_stem = string.split(self.receptor_filename, '.')[0]
		self.dpo.set_receptor(receptor_filename)


	def set_flexres(self, flexres_filename):
		flexmol = Read(flexres_filename)[0]
		flexres_filename = os.path.basename(flexres_filename)
		self.dpo['flexres_flag']['value'] = True
		self.dpo['flexres']['value'] = flexres_filename
		#make sure each atom type in flexres molecule is in ligand_types
		d = {}
		current_types = self.dpo['ligand_types']['value'].split()
		for t in current_types:
			d[t] = 1
		for a in flexmol.allAtoms:
			d[a.autodock_element] = 1
		self.dpo['ligand_types']['value'] = string.join(d.keys())


	def set_docking_parameters(self, **kw):
		"""Any docking parameters should be set here
		"""
		# like this: 
		# newdict = {'ga_num_evals':1750000, 'ga_pop_size':150,
		#			'ga_run':20, 'rmstol':2.0}
		# self.mv.dpo['<parameter>']['value'] = <new value>
		for parm, newvalue in kw.items():
			self.dpo[parm]['value'] = newvalue
			if parm=='set_sw1':
				self.dpo['set_psw1']['value'] = not newvalue
			if parm=='set_psw1':
				self.dpo['set_sw1']['value'] = not newvalue
			if parm=='flexres':
				self.set_flexres(newvalue) 
			if parm=='write_all':
				self.set_write_all(newvalue) 


	def write_dpf(self, dpf_filename,
			  parm_list = genetic_algorithm_local_search_list4_2, 
			  pop_seed = False):
		if not dpf_filename:
			dpf_filename = "%s%s%s%s" % \
						   (self.ligand_stem, "_",
							self.receptor_stem, ".dpf")
		# now that we have a filename...
		# set initial conformation
		if pop_seed:
			self.dpo['tran0']['value'] = self.dpo['about']['value']
			self.dpo['quat0']['value'] = '1.0 0. 0. 0.'
			dihe0 = '0. '*self.dpo['ndihe']['value']
			dihe0.rstrip()
			self.dpo['dihe0']['value'] = dihe0 
		if self.verbose:
			print "writing ", dpf_filename
		self.dpo.write42(dpf_filename, parm_list)

 
 ########################################################



def prepareDPF(dpf_filename, receptor_filename, ligand_filename, flexres_filename = None, search_algorithm = "GA", parameters = None):

	# implement the possibility to define explicit params for the SmartVS?

	if search_algorithm == "GA": # GA-only supported keywords
		parameter_list = genetic_algorithm_local_search_list4_2
	if search_algorithm == "LS":
		parameter_list = local_search_list4_2 # not explicitly supported
	if search_algorithm == "SA":
		parameter_list = simulated_annealing_list4_2 # not explicitly supported
	
	pop_seed = False
	verbose = False
	template = None

	# parameter parser
	dpf_lines = DPFcontent.get(1.0, END)

	if not parameters:
		parameters = []
	
		for line in dpf_lines.split('\n'):
			if not line.strip(): # get rid of empty lines
				continue
			else:
				clean_line = line.split("#")[0] # get rid of comments
				clean_line = clean_line.split(" ", 1)
				keyword = clean_line[0]
				try:
					argument = clean_line[1]
				except:
					argument = ""
	
				if keyword == "autodock_parameter_version":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found autodock_param_vers", value[0]
					parameters.append(par_line)
					
				if keyword == "parameter_file":
					value = argument#.replace(" ", "")
					par_line = keyword+"="+value
					parameters.append(par_line)
					#print "=> found parameter file, generated this xxxx:", value
	
				if keyword == "outlev":
					value = argument#.replace(" ", "")
					par_line = keyword+"="+value
					#print "=> found outlev, generated this xxxx:", par_line
					parameters.append(par_line)
	
				if keyword == "seed": 
					value = argument.split()
					par_line = keyword+"="+value[0]+" "+value[1]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
	
				if keyword == "tran0":
					value = argument.replace(" ", "")
					par_line = keyword+"="+value
					#print "=> found smooth, generated this xxxx:", par_line
					parameters.append(par_line)
				if keyword == "axisangle0":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "dihe":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "tstep":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "qstep":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "dstep":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "unbound":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "rmstol":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "extnrg":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "e0max":
					value = argument.split()
					par_line = keyword+"="+value[0]+" "+value[1]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_pop_size":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_num_evals":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_num_generations":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_elitism":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_mutation_rate":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_crossover_rate":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_window_size":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_cauchy_alpha":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_cauchy_beta":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "set_ga":
					#value = argument.split()
					par_line = keyword+"= "#+value[0]+"'"
					#print "=> found %s, generated this " % (par_line)
					parameters.append(par_line)
				if keyword == "sw_max_its":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "sw_max_succ":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "sw_max_fail":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "sw_rho":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "sw_lb_rho":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ls_search_freq":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "set_psw1":
					par_line = keyword+"= "
					#par_line = "set_psw1_flag"
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "set_sw1":
					par_line = keyword+"= "
					#par_line = "set_sw1_flag"
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "unbound_model":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "ga_run":
					value = argument.split()
					par_line = keyword+"="+value[0]
					#print "=> found %s, generated this : %s" % (keyword, par_line)
					parameters.append(par_line)
				if keyword == "analysis":
					#value = argument.split()
					par_line = keyword+"= "#+value[0]+"'"
					#print "=> found %s, generated this : " % (par_line)
					parameters.append(par_line)
	if verbose: print "###\n", parameters, "###\n"

	dm = DockingParameter42FileMaker(verbose=None)
	dm.set_ligand(ligand_filename)
	dm.set_receptor(receptor_filename)
	if flexres_filename is not None:
		flexmol = Read(flexres_filename)[0]
		flexres_types = flexmol.allAtoms.autodock_element
		lig_types = dm.dpo['ligand_types']['value'].split()
		all_types = lig_types
		for t in flexres_types:
			if t not in all_types: 
				all_types.append(t)
		all_types_string = all_types[0]
		if len(all_types)>1:
			for t in all_types[1:]:
				all_types_string = all_types_string + " " + t
		dm.dpo['ligand_types']['value'] = all_types_string 
		dm.dpo['flexres']['value'] = os.path.basename(flexres_filename)
		dm.dpo['flexres_flag']['value'] = True
	for p in parameters:
		key,newvalue = string.split(p, '=')
		if newvalue[0]=='[':
			nv = []
			for item in newvalue[1:-1].split(','):
				nv.append(float(item))
			newvalue = nv
		elif 'flag' in key:
			if newvalue in ['1','0']:
				newvalue = int(newvalue)
			if newvalue =='False':
				newvalue = False
			if newvalue =='True':
				newvalue = True
		kw = {key:newvalue}
		apply(dm.set_docking_parameters, (), kw)
		if key not in parameter_list:
			#special hack for output_pop_file
			if key=='output_pop_file':
				parameter_list.insert(parameter_list.index('set_ga'), key)
			else:
				parameter_list.append(key) 
	dm.write_dpf(dpf_filename, parameter_list, pop_seed)


########################## INFO ###################################


def RMBhelp(aboutwhat = None):
	# TODO 
	pass

def GetOSoption():
	global TargetOS, LinuxOptionsPanel, PBSOptionsPanel, WinOptionsPanel
	
	LinMasterBash, LinSingleBash, LinTarGz, LinRunAfter = BooleanVar(),BooleanVar(),BooleanVar(), BooleanVar()
	PBScputime = StringVar()

	for panel in LinuxOptionsPanel, PBSOptionsPanel, WinOptionsPanel:
		panel.grid_forget()
	if not TargetOS.get():
		print "this is the first time the TargetOS is called"
		TargetOS.set('lin')

	if TargetOS.get() == "lin":
		# Linux/Mac
		panel = LinuxOptionsPanel
		if system == "Windows":
			CygwinOption = Tkinter.Checkbutton(panel.interior(), text = 'Use Cygwin', variable = cygwin)
			CygwinOption.grid(row = 0, column = 0, sticky = W)
		Label(panel.interior(), text="Script generation ").grid(row = 1, column = 0, sticky = E)
		LinuxScriptOption = OptionMenu(panel.interior(), LinuxScriptLevel, "master script for starting the VS",\
						"single scripts for each ligand", "[disabled]").grid(row = 1, column = 1, sticky = W)
		CheckMakeTarGZ = Tkinter.Label(panel.interior(), text = 'Create a VS package file ').grid(row = 2,\
						column = 0, columnspan = 1, sticky = E)
		TarCompressionOptions = OptionMenu(panel.interior(), TarFile, "Tar (Bz2 compression)", "Tar (Gzip compression)",\
						"Tar (uncompressed)", "Zip compressed", "[disabled]")
		TarCompressionOptions.grid(row = 2, column = 1, sticky = W)

	if TargetOS.get() == "pbs":
		# PBS
		panel = PBSOptionsPanel 
		Label(panel.interior(), text="Script generation ").grid(row = 1, column = 0, sticky = E)
		LinuxScriptOption = OptionMenu(panel.interior(), LinuxScriptLevel, "master script for starting the VS",\
						"single scripts for each ligand", "[disabled]").grid(row = 1, column = 1, sticky = W, columnspan = 3)
		CheckMakeTarGZ = Tkinter.Label(panel.interior(), text = 'Create a VS package file ').grid(row = 2, column = 0, columnspan = 1, sticky = E)
		TarCompressionOptions = OptionMenu(panel.interior(), TarFile, "Tar (Bz2 compression)", "Tar (Gzip compression)",\
						"Tar (uncompressed)", "[disabled]")
		TarCompressionOptions.grid(row = 2, column = 1, sticky = W)
		PBSOptionCPUTime = Label(panel.interior(), text='CPU time per job ')
		PBSOptionCPUTime.grid(row = 3, column = 0, sticky = E)
		PBSOptionCPUTimeEntry = Tkinter.Entry(panel.interior(), textvariable=PBStime, width = 8)
		PBSOptionCPUTimeEntry.grid(row = 3, column =1, sticky = W)
		PBSOptionCPUset = Button(panel.interior(), text ="Set", command = SetPBStime)
		PBSOptionCPUset.grid(row = 3, column =2, sticky = W, columnspan = 1)
		Label(panel.interior(), text = "Number of DLG's to run per ligand ").grid(row = 4, column = 0, sticky = E)
		Entry(panel.interior(), textvariable = PBShowmanyruns, width = 4).grid(row = 4, column = 1, sticky = W)
		PBSOptionCPUset = Button(panel.interior(), text ="Set", command = SetPBShowmanyruns).grid(row = 4, column = 2, sticky = W)
		SetPBStime
		SetPBShowmanyruns
		

	if TargetOS.get() == "win":
		# Win (God bless you)
		CheckMasterScript = Tkinter.Checkbutton(panel.interior(), text = 'Generate a master batch script for the VS job')
		CheckMasterScript.grid(row = 3, column = 0, sticky = W, columnspan = 3)
		CheckMakeTarGZ = Tkinter.Checkbutton(panel.interior(), text = 'Create a compressed file of the VS (.zip)') 
		CheckMakeTarGZ.grid(row = 4, column = 0, sticky = W, columnspan = 3)
	panel.grid(row = 3, column = 0, columnspan = 2)

def SetPBShowmanyruns():
	wrong = False
	try:
		howmany = PBShowmanyruns.get()
		if howmany == "":
			wrong = True
		if howmany <= 0:
			wrong = True
	except:
		wrong = True
	if wrong:
		nb.tab('VS Generation').invoke()
		tkMessageBox.showerror("PBS runs error!", ("The value of runs must be a number bigger than 0 (and smaller than infinite).\n\nReset to default."))
		PBShowmanyruns.set(1)
		return False
	else:
		if howmany > 255:
			tkMessageBox.showwarning("Warning", ("The number of runs is very high."))
		return True

def SetPBStime():
	if DEBUG: print "CHECKING TIME FOR PBS", PBStime
	time = PBStime.get()
	try:
		time = time.split(':')
	except:
		nb.tab('VS Generation').invoke()
		tkMessageBox.showerror("PBS time error!", ("The time format must be :\n\n   hh:mm:ss\n\n Reset to default."))
		PBStime.set("24:00:00")
		return False

	wrong = False
	if len(time) < 3 or len(time) > 3:
		nb.tab('VS Generation').focus_set()
		nb.tab('VS Generation').invoke()
		tkMessageBox.showerror("PBS time error!", ("The time format must be :\n\n   hh:mm:ss\n\n Reset to default."))
		PBStime.set("24:00:00")
		return False
	try:
		if int(time[0]) < 0:
			wrong = True
		if int(time[1]) > 59 or int(time[1]) < 0:
			wrong = True
		if int(time[2]) > 59 or int(time[2]) < 0:
			wrong = True
		if not int(time[0]) > 0:
			if not int(time[1]) > 0:
				if not int(time[2]) > 0:
					wrong = True
	except:
		wrong = True
	if wrong:	
		nb.tab('VS Generation').focus_set()
		nb.tab('VS Generation').invoke()
		tkMessageBox.showerror("PBS time error!", ("The time format must be :\n\n   hh:mm:ss\n\n Reset to default."))
		PBStime.set("24:00:00")
		return False
	else:
		return True


### CORE FUNCTIONS

def TheCheck():
	# Perform the checking for all the
	# necessary settings for activating
	# the GENERATE button
	LIGANDS = False
	RECEPTORS = False
	MAPS = False
	DOCKING = False
	FLEXIBLE = False
	DESTINATION = False

	if DEBUG: print "======= PERFORMING THE CHECK ============"

	# Check for ligands
	if TotalAcceptedLigands.get() > 0:
		LIGANDS = True
		count_ligands = TotalAcceptedLigands.get()
		LigandSummary.set(( str(count_ligands)+" accepted" ))
		LigSummaryLabel.config(fg = '#11bb11')
	else:
		LigandSummary.set(( " [ none ] "))
		LigSummaryLabel.config(fg = "red")

	if DEBUG : print "- ligands", TotalAcceptedLigands.get()


	# Check for the receptors
	if RCstatus.get() == 0:
		if SingleReceptorSet.get():
			receptor_message = (RecFilename.get())
			RECEPTORS = True
			count_receptors = 1
	if RCstatus.get() == 1:
		if MultiReceptorSet.get():
			count_receptors = len(receptorScrolledListBox.get('0' , END))
			if count_receptors > 0:
				receptor_message = (  str(count_receptors)+" structures" )
				RECEPTORS = True
	# potential flexible residues
	#
	#
	if RECEPTORS:
		if DoFlex.get():
			if DoFlexFromWhat.get() == 1:
				if not FlexResFileName.get() == "":
					FLEXIBLE = True
			if DoFlexFromWhat.get() == 2:
				if FlexResDefined.get():
					FLEXIBLE = True
			if FLEXIBLE:
				if DEBUG: print "THE_CHECK> we're going flexible..."
				receptor_message = ("\n"+receptor_message+"\n[ flex: "+ResidueStatus.get()+" ]" )
		RecSummaryLabel.config(fg = '#11bb11')
		ReceptorSummary.set(receptor_message)
	else:
		ReceptorSummary.set( " [ none ] " )
		RecSummaryLabel.config(fg = 'red')


	# Check for maps
	if MapSource.get() <= 1:
		if len(GPFcontent.get('1.0', END)) > 3:
			if MapSource.get() == 0:
				MapsSummary.set(("\ncalculated in each job\n[ "+GPFfilename.get()+" ]"))
				MAPS = True
			if MapSource.get() == 1 and AutoGridBin.get():
				MAPS = True
				if CacheMapPolicy.get() == "Make copies [ use more disk space ]":
					MapsSummary.set(("\n\ncalculated now and copied\n  [ Template: "+GPFfilename.get()+" ]\n  [ AutoGrid bin: "+AutoGridBin.get()+" ]"))
				if CacheMapPolicy.get() == "Make symbolic links [ save disk space ]":
					MapsSummary.set(("\n\ncalculated now and linked\n  [ "+GPFfilename.get()+" ]\n  [ AutoGrid bin: "+AutoGridBin.get()+" ]"))
	if MapSource.get() == 2:
		if DoCachedMaps.get():
			MAPS = True
			if CacheMapPolicy.get() == "Make copies [ use more disk space ]":
				MapsSummary.set(("\nalready calculated and copied in each ligand directory from:\n[ "+CacheMapDirName.get()+" ]" ))
			if CacheMapPolicy.get() == "Make symbolic links [ save disk space ]":
				MapsSummary.set(("\nalready calculated and linked in each ligand directory from:\n[ "+CacheMapDirName.get()+" ]" ))
			if DEBUG: MapsSummary.set(("\nusing pre-calculated\n\t[ "+CacheMapDirName.get()+" ]"))
	


	if MAPS:
		MapsSummaryLabel.config(fg = '#11bb11')
	else:
		MapsSummary.set((" [ none ] "))
		MapsSummaryLabel.config(fg = 'red')

	# Check for DPF
	if docking_set.get() == "From template...":
		if len(DPFcontent.get('1.0', END)) > 3: # three lines arbitrary value
			docking_message = ("\nusing DPF template\n[ "+DPFfilename.get()+" ]" )
			DOCKING = True
	
	if DOCKING:
		DockingSummary.set(docking_message)
		DockSummaryLabel.config(fg = '#11bb11')
	else:
		DockingSummary.set(" [ none ] ")
		DockSummaryLabel.config(fg = "red")

	# implement with some feedback
	if TargetOS.get() == "pbs":
		if SetPBStime():
			if SetPBShowmanyruns():
				pass
		else:
			return False

	#Check for the output directory
	if not JobDirectory.get() == "":
		DESTINATION = True
		SetOutDirButton.config(fg = 'black')
		OutputDirLabel.config(fg = '#11bb11')
		OutputDirLabel.config(fg = '#11bb11')
	else:
		SetOutDirButton.config(fg = 'red')
		OutputDirLabel.config(fg = 'red')


	if LIGANDS and RECEPTORS and MAPS and DOCKING:
		# that's why we're here...
		JobsSummary.set(("\t"+str(count_receptors * count_ligands)+" jobs will be generated" ))
		if DESTINATION:
			TheButton.config(state = NORMAL, text = "G E N E R A T E", command = TheFunction)
			TheButton.flash()
	else:
		TheButton.config(state = DISABLED)
		JobsSummary.set((""))
	


def DisableInterface(Tab = None):
	if Tab:
		nb.tab(Tab).configure(state = 'disabled')
	else:
		nb.tab('Ligand(s)').configure(state = 'disabled')
		nb.tab('Receptor(s)').configure(state = 'disabled')
		nb.tab('Maps').configure(state = 'disabled')
		nb.tab('Docking').configure(state = 'disabled')
		nb.tab('VS Generation').configure(state = 'disabled')
		AddLigandsButton.config(state = DISABLED)
		AddLigandsDirButton.config(state = DISABLED)
		AddLigandsDirRecursiveButton.config(state = DISABLED)
		RemoveLigandsButton.config(state = DISABLED)
		RemoveAllLigandsButton.config(state = DISABLED)
		FilterButton.config(state = DISABLED)
		LigandPDBQTOptButton.config(state = DISABLED)
		SetOutDirButton.config(state = DISABLED)

def EnableInterface(Tab = None):
	if Tab:
		nb.tab(Tab).configure(state = 'normal')
	else:
		nb.tab('Ligand(s)').configure(state = 'normal')
		nb.tab('Receptor(s)').configure(state = 'normal')
		nb.tab('Maps').configure(state = 'normal')
		nb.tab('Docking').configure(state = 'normal')
		nb.tab('VS Generation').configure(state = 'normal')
		AddLigandsButton.config(state = NORMAL)
		AddLigandsDirButton.config(state = NORMAL)
		AddLigandsDirRecursiveButton.config(state = NORMAL)
		RemoveLigandsButton.config(state = NORMAL)
		RemoveAllLigandsButton.config(state = NORMAL)
		FilterButton.config(state = NORMAL)
		LigandPDBQTOptButton.config(state = NORMAL)
		SetOutDirButton.config(state = NORMAL)

def HandBrake():
	TheButton.config(state = DISABLED, text = " [ Generation process is paused... ]")
	if tkMessageBox.askquestion('Warning', 'Do you really want to interrupt the generation process?') == "yes":
		StopImmediately.set(True)
		return
	else:
		TheButton.config(state = NORMAL,text = "> STOPPED <")
		return


def TheFunction():
	path = JobDirectory.get()
	if DEBUG: print "TheFunction> starting the vs creation in ", path

	StopImmediately.set(False)

	DisableInterface()
	EnableInterface('VS Generation')

	TheButton.config(state = NORMAL, text = " [ Stop the generation... ]", command = HandBrake)
	if DEBUG:
		print "\n========================================\n"
		print "===== STARTING THE GENERATION ==========\n"
		print "========================================\n"

	# Initialize the log
	log_file = InitializeLog(path)
	if not log_file:
		if DEBUG: print "[gen+log] => we start very well... :S no logging available!"
		EnableInterface()
		return False

	
	header = "\n\n     ======================================================================================================\n"
	header += "     ======================================================================================================\n\n"
	header += "                              G E N E R A T I O N    S T A R T E D\n\n"

	print >> log_file, header


	# Define the target(s)
	if RCstatus.get() == 0:
		if DEBUG: print "[gen] => single receptor NAME = ", 
		receptor_list = [ RecFilename.get() ]
		if DEBUG: print RecFilename.get()
	else:
		if DEBUG: print "[gen] => multiple receptors", 
		receptor_list = receptorScrolledListBox.get('0', END)
	
	if DEBUG: print "[ I'm going to use %d receptors ]" % len(receptor_list)

	# Get the filtered ligands
	ligand_list = []
	atomtypes_set = [] #atom types present in the accepted ligands set
	for ligand in LigandDictionary.keys():
		if LigandDictionary[ligand]["accepted"]:
			ligand_list.append(ligand)
			for atom in LigandDictionary[ligand]["Atypes"]:
				if atom not in atomtypes_set: atomtypes_set.append(atom)
	# counters are initialized here
	rec_count = len(receptor_list)
	lig_count = len(ligand_list) 
	jobs_todo = rec_count * lig_count
	jobs_done = 1
	# the Main loop
	for receptor in receptor_list:
		rec_name = os.path.basename(receptor).rsplit('.', 1)[:-1][0]
		current_path = path+os.sep+rec_name
		# Flush the list of dir per ligands (this is generated on a per-receptor base)
		del DirJournal[:]
		# create the directory RECEPTOR/[ligands]
		if not os.path.exists(current_path):
			try:
				os.makedirs(current_path, 0755)
			except:
				tkMessageBox.showerror("Error!", ("Impossible to create the directory:\n%s\n GIVING UP..." % current_path))
				print >> log_file, ("\n\n\n#### ERROR ###\n\nThere was a problem in creating the directory:\n%s\n\n VS generation aborted.\n\n####      ####" % current_path) # End of receptor loop
				TheButton.config(state = DISABLED, text = "E R R O R")
				EnableInterface()
				return False

		## Preliminary stuff to do before the ligands get involved
		#
		#
		## 1. define or generate flexible residue files
		#
		flex_res = None
		if DoFlex.get(): # 
			if FlexResDefined.get(): # 
				if DEBUG: print "soo.... we want flexible,right?\n\nPREPARING"
				if DoFlexFromWhat.get() == 1:
					if FlexResFileName.get(): # TODO in theory it shouldn't be necessary
						if DEBUG: print "\tcopying the flexible residue in the right place"
						if DEBUG: print "\tcp flex.pdbqt working_dir"
						flex_res = FlexResFileName.get()
				if DoFlexFromWhat.get() == 2:
					if FlexResSelected.get(): # TODO in theory it shouldn't be necessary
						if DEBUG: print "\tgenerate the flexible residue from the receptor"
						if DEBUG: print "\tprepare_flex_receptor blablabla "
						InfoMessage.set( (  "[ Generating flex residues for %s... ]" % rec_name )) 
						receptor, flex_res = genFlex(receptor)
				flex_types = GetAtypes(flex_res)
				for atom in flex_types:
					if atom not in atomtypes_set: atomtypes_set.append(atom)

		if DEBUG:
			print "[GEN] I've got the flex_res filename", flex_res
			print "[GEN] Now the receptor is", receptor
		#
		## 2. calculate or copy maps now if necessary
		#
		#  create the cached maps folder (for "now" and "already")
		CachedMapsDir = None

		CacheMapOptions = OptionMenu(CacheMapHandle.interior(), CacheMapPolicy, "Make copies [ use more disk space ]", "Make symbolic links [ save disk space ]")
		if CacheMapPolicy.get() == "Make copies [ use more disk space ]":
			symlink = False
		if CacheMapPolicy.get() == "Make symbolic links [ save disk space ]":
			symlink = True

		if MapSource.get() >= 1: 
			CachedMapsDir = current_path+os.sep+"maps"
			if not os.path.exists(CachedMapsDir):
				try:
					os.makedirs(CachedMapsDir, 0755)
				except:
					tkMessageBox.showerror("Error!", ("Impossible to create the directory:\n%s\n GIVING UP..." % CachedMapsDir))
					print >> log_file, ("\n\n\n#### ERROR ###\n\nThere was a problem in creating the directory:\n%s\n\n VS generation aborted.\n\n####      ####" % CachedMapsDir) 
					EnableInterface()
					return False
		if MapSource.get() == 1: # populate the dir with AutoGrid
			InfoMessage.set( (  "[ Running AutoGrid on %s... ]" % rec_name )) 
			if not CalcCacheMaps(CachedMapsDir, receptor, flex_res): 
				tkMessageBox.showerror("Error!", ("Impossible to calculate the cached maps here:\n%s\n GIVING UP..." % CachedMapsDir))
				EnableInterface()
				return False

		if MapSource.get() == 2: # populate the dir by copying the files from the cache
			InfoMessage.set( (  "[ Copying cached maps for %s... ]" % rec_name )) 
			if not CopyMapDir(atomtypes_set, None, CachedMapsDir, symlink = False): # no matter if maps will be eventually copied or linked, now it must be false
				tkMessageBox.showerror("Error!", ("Impossible to copy the maps in the VS job master directory \n%s\n GIVING UP..." % CachedMapsDir))
				EnableInterface()
				return False

		# Ligands loop #############################################################################################
		for ligand in ligand_list:

			if StopImmediately.get():
				InfoMessage.set( "Generation process aborted by the user...")
				print >> log_file, ("\n\n\n#### ABORT ###\n\nThe generation process was interrupted by the user.\n\n") 
				TheButton.config(state = DISABLED, text = " [ Generation aborted ]")
				EnableInterface()
				return False

			InfoMessage.set( (  "=> Processing %s | %s \t[ %d | %d ]" % (os.path.basename(receptor), os.path.basename(ligand), jobs_done, jobs_todo )   ))
			nb.tab('VS Generation').focus_set()
			root.update()
			current_atom_types = []
			ligand_name = os.path.basename(ligand).rsplit('.', 1)[:-1][0]
			# create ligand dir
			ligand_dir = MkJobDir(ligand, rec_name, current_path)
			if not ligand_dir:
				tkMessageBox.showerror("Error!", ("Impossible to create the directory:\n%s\n GIVING UP..." % ligand_dir))
				print >> log_file, ("\n\n\n#### ERROR ###\n\nThere was a problem in creating the directory:\n%s\n\n VS generation aborted.\n\n####      ####" % ligand_dir) 
				EnableInterface()
				return False

			# copy the ligand in place
			if not os.path.dirname(ligand) == ligand_dir:
				try:
					shutil.copy2(ligand, ligand_dir)
				except:
					tkMessageBox.showerror("Error!", ("Impossible to copy the ligand:\n%s\n\tto\n%s\n\nGIVING UP..." % (ligand, ligand_dir)))
					EnableInterface()
					return False
			else:
				if DEBUG: print "TheFunction> skipped the source/dest ligand copy because they are identical..."
			
			# copy flexres if necessary
			if DoFlex.get(): # 
				if FlexResDefined.get():
					if not os.path.dirname(flex_res) == ligand_dir:
						try:
							shutil.copy2( flex_res, ligand_dir)
						except:
							tkMessageBox.showerror("Error!", ("Impossible to copy the flex res file:\n%s\n\tto\n%s\n\nGIVING UP..." % (flex_res, ligand_dir)))
							EnableInterface()
							return False
					else:
						if DEBUG: print "TheFunction> skipped the source/dest flex_res copy because they are identical..."


			# maps management
			#
			# a. generate GPF
			gpf_file = None
			if MapSource.get() == 0 : # being in the for loop cached maps will be referred to the receptor
				# generate the gpf
				gpf_file = ligand_dir+os.sep+rec_name+".gpf"
				try:
					prepareGPF(gpf_file, receptor, ligand_filename = ligand, atom_types = None, flexres_filename = flex_res)
				except:
					tkMessageBox.showerror("Error!", ("Impossible to create the gpf file:\n%s\n GIVING UP..." % gpf_file))
					EnableInterface()
					return False
					
				if not os.path.exists(gpf_file):
					tkMessageBox.showerror("Error!", ("Impossible to create the gpf file:\n%s\n GIVING UP..." % gpf_file))
					print >> log_file, ("\n\n\n#### ERROR ###\n\nThere was a problem in creating the GPF:\n%s\n\n VS generation aborted.\n\n####      ####" % gpf_file) 
					EnableInterface()
					# error message window
					return False

				# copy potential parameter files
				if not GPFParameterFile.get() == "":
					if not os.path.dirname(GPFParameterFile.get()) == ligand_dir:
						try:
							shutil.copy2( GPFParameterFile.get(), ligand_dir)
						except:
							tkMessageBox.showerror("Error!", ("Impossible to copy the parameter file required by the\
GPF:\n%s\n\tto\n%s\n\nGIVING UP..." % (GPFParameterFile.get(), ligand_dir)))
							EnableInterface()
							return False
					else:
						if DEBUG: print "TheFunction> skipped the source/dest GPFparamfile copy because they are identical..."


				# copy the receptor
				if not os.path.dirname(receptor) == ligand_dir:
					try:
						shutil.copy2(receptor, ligand_dir)
					except:
						tkMessageBox.showerror("Error!", ("Impossible to copy the receptor\n%s\n\tto\n%s\n\nGIVING UP..." % (receptor, ligand_dir)))
						EnableInterface()
						return False
				else:
					if DEBUG: print "TheFunction> skipped the source/dest receptor copy because they are identical..."



			# b. use cached maps
			elif MapSource.get() >= 1:
				current_atom_types = GetAtypes(ligand)
				# include flex res atoms
				if FlexResDefined.get():
					for atom in flex_types:
						if atom not in current_atom_types: current_atom_types.append(atom)
				CopyMapDir(current_atom_types, CachedMapsDir, ligand_dir, symlink = symlink)

			# Prepare the DPF
			if docking_set.get() == "From template...":
				dpf_file = ligand_dir+os.sep+ligand_name+"_"+rec_name+".dpf"
				prepareDPF(dpf_file, receptor, ligand, flex_res)
				if not os.path.exists(dpf_file):
					tkMessageBox.showerror("Error!", ("Impossible to create the DPF file:\n%s\n GIVING UP..." % dpf_file))
					print >> log_file, ("\n\n\n#### ERROR ###\n\nThere was a problem in creating the DPF:\n%s\n\n VS generation aborted.\n\n####      ####" % dpf_file) 
					EnableInterface()
					return False	
				# copy potential parameter files
				if not DPFParameterFile.get() == "":
					if not os.path.dirname(DPFParameterFile.get()) == ligand_dir:
						try:
							shutil.copy2( DPFParameterFile.get(), ligand_dir)
						except:
							tkMessageBox.showerror("Error!", ("Impossible to copy the parameter file required by the\
DPF:\n%s\n\tto\n%s\n\nGIVING UP..." % (DPFParameterFile.get(), ligand_dir)))
							EnableInterface()
							return False
					else:
						if DEBUG: print "TheFunction> skipped the source/dest DPFparamfile copy because they are identical..."
			jobs_done += 1

			if not TargetOS.get() == "win":
				if not LinuxScriptLevel.get() == "[disabled]":
					MakeJobScript(ligand_dir, dpf_file, gpf_file)
			log_file.flush()
			
	
		if TargetOS.get() == "pbs" or TargetOS.get() == "lin":
			if DEBUG: print "Making the master script"
			if LinuxScriptLevel.get() == "master script for starting the VS":
				MakeMasterJobScript(current_path)

	if DEBUG: print "\n\n\n	[ GENERATION DONE ]"
	if not TarFile.get() == "[disabled]":
		InfoMessage.set( (  "[ writing the compressed file... ]")   ) 
		TheButton.config(state = DISABLED, text = "...creating the VS package...")
		root.update()
		# vs pack filename
		pack_filename = path+os.sep+"VSpack_"+os.path.basename(path)
		if DEBUG:
			print "TheFunction> creating the package file", pack_filename, "in ", path

		# Zip file format
		if TarFile.get() == "Zip compressed":
			if not MakeZip(path, pack_filename):
				root.update()
				return False
		# ...anything else
		else:
			if not MakeTar(path, pack_filename):
				root.update()
				return False

	InfoMessage.set( (  "[ generation completed successfully ]")   ) 
	tkMessageBox.showinfo(title="VS generation terminated", message=("%d docking jobs have been successfully \
generated in:\n\n%s\n" % (len(receptor_list) * len(ligand_list), path ) ))
	EnableInterface()
	# Success! update the log with all the ligands, and close the file
	print >> log_file, "\n\t\t\t process completed successfully.\n\n"
	print >> log_file, "\n\n\n[DONE]" # End of receptor loop. This line is used in the load function to recognize a successfull VSgeneration when loading it back.
	log_file.close()
	TheButton.config(state = DISABLED, text = "D O N E")


def CopyMapDir(atomtypes_to_copy, source_dir, destination_dir, symlink = False):
	# copy or make symbolic links of map files
	#
	#
	if source_dir == destination_dir:
		if DEBUG: print "CopyMapDir> skipping copy/symlink because the directories are the same"
		return True
	if MapSource.get() == 2:
		map_files = MapFolderList.get('0', END)
	if MapSource.get() == 1:
		map_files = glob.glob(os.path.join(source_dir, "*.map"))
		map_files.append(glob.glob(os.path.join(source_dir, "*.xyz"))[0])
		map_files.append(glob.glob(os.path.join(source_dir, "*.fld"))[0])

	counter = 0
	atomtypes_to_copy.append('e')
	atomtypes_to_copy.append('d')
	atomtypes_to_copy.append('maps')
	for atype in atomtypes_to_copy:
		for map in map_files:
			if atype == map.split(".")[-2]:
				try:
					if DEBUG: print "CopyMapDir> going to process this file ==>", map
					if symlink:
						if DEBUG: print "     doing symlinking", map, destination_dir
						map_filename = os.path.basename(map)
						map_dir = os.path.basename(source_dir)
						SRC = "../"+map_dir+os.sep+map_filename
						DEST = destination_dir+os.sep+map_filename
						os.symlink(SRC, DEST)
					else:
						shutil.copy2( map, destination_dir)
					counter = counter + 1 # +1 to account for the two maps.* files
				except:
					tkMessageBox.showerror(title="Cached maps error", message=(("Some problem occurred when copying or linking the file %s") % map ))
					return False
	if len(atomtypes_to_copy)+1 == counter:
		return True
	else:
		return False

def GetAtypes(filename = None, selection = None):
	# The selection works with selected
	# flex residues only
	#
	if not filename and not selection:
		return

	atypes = []
	if filename:
		f = open(filename, 'r')
		for line in f.readlines():
			if line[0:6] == 'HETATM' or line[0:4] == 'ATOM':
				atom = line.split()[-1]
				if atom not in atypes:
					atypes.append(atom)
		f.close()
	if selection:
		pass
	
	return atypes

def CalcCacheMaps(output_dir, receptor, flexible_residues = None):
	# get the atom types for the accepted ligands
	atom_types = []
	for ligand in LigandDictionary.keys():
		if LigandDictionary[ligand]["accepted"]:
			for atom in LigandDictionary[ligand]["Atypes"]:
				if atom not in atom_types:
					atom_types.append(atom)
	if not os.path.dirname(receptor) == output_dir:
		try:
			shutil.copy2( receptor, output_dir)
		except:
			tkMessageBox.showerror(title="Error", message=(("Impossible to copy the receptor in the target directory for caching the maps.")))
		gpf_name = output_dir+os.sep+os.path.basename(receptor).rsplit('.', 1)[:-1][0]+"_all_maps.gpf"
	else:
		if DEBUG: print "CalcCacheMaps> skipping the receptor copy, because files are identical"

	try:
		prepareGPF(gpf_name, receptor, atom_types = atom_types , flexres_filename = flexible_residues)
	except:
		return False
	if RunAutoGrid(output_dir, gpf_name):
		return True
	else:
		return False


def RunAutoGrid(working_dir, gpf):
	# define AutoGrid
	#
	if not AutoGridBin.get():
		return False
	else:
		AutoGrid = AutoGridBin.get()

	glg = gpf.rsplit('.', 1)[:-1][0]+".glg"
	try:
		nb.tab('VS Generation').focus_set()
		root.update()
		#print "Look, mom! I'm running Autogrid from inside Python!!!!"
		os.system(("cd %s; %s -p %s -l %s" % (working_dir, AutoGrid, gpf, glg )))
		
		# Check if the calculation succeded
		GridLog = open(glg, 'r')
		log = GridLog.readlines()
		GridLog.close()
		if DEBUG: print log[-2]
		if "Successful Completion" in log[-2]:
			return True
		else:
			error = ""
			for line in log[-7:]:
				error += line
			tkMessageBox.showerror("AutoGrid error!", ("Maps calculation failed with the following message:\n %s" % error))
			return False
	except:
		return False

def WhichAutoGrid(program = 'autogrid4'):
	# Try to check the file path....
	def is_exe(fpath):
		return os.path.exists(fpath) and os.access(fpath, os.X_OK)
	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			if CheckExe(program):
				AutoGridBin.set(program)
				AutoGridExecButton.config(text = "Change the AutoGrid executable", fg = 'black')
				TheCheck()
				return True
	else:
	# walks thru the path...
		for path in os.environ["PATH"].split(os.pathsep):
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				if CheckExe(exe_file):
					AutoGridBin.set(exe_file)
					AutoGridExecButton.config(text = "Change the AutoGrid executable", fg = 'black')
					TheCheck()
					return True
	# If the function gets here, AG was not found...
	AutoGridExecButton.config(text = "Set the AutoGrid executable", fg = 'red')
	
def GetAutoGrid(filename = None):
	keepasking = True
	while keepasking == True:
		if filename:
			AutoGrid = filename
		else:
			AutoGrid = askopenfilename(title = "Specify the AutoGrid binary file...", filetypes =[("Any file...", '*')])
		if AutoGrid:
			if CheckExe(AutoGrid):
				keepasking = False
				AutoGridBin.set(AutoGrid)
				AutoGridExecButton.config(text = "Change the AutoGrid executable", fg = 'black')
				TheCheck()
				return True
			else:
				tkMessageBox.showwarning("AutoGrid", "The specified file is not an executable.")
				AutoGridExecButton.config(text = "Set the AutoGrid executable", fg = 'red')
				return False
		else:
			if not AutoGridBin.get():
				answer = tkMessageBox.askquestion('Warning', 'The AutoGrid binary file is required for pre-caching maps.\nDo you want to define it?')
				if answer == "no":
					tkMessageBox.showwarning("Pre-caching aborted", "The calculations of maps has been aborted by the user.")
					keepasking = False		
					GPFframe.forget()
					AutoGridWhen1.invoke() # Select the default as "Run AG in each job"
					AutoGridExecButton.config(text = "Set the AutoGrid executable", fg = 'red')
					return False
			else:
				keepasking = False
				TheCheck()
				return True

def CheckExe(file):
	# not working 
	return True

def genFlex(receptor_filename):
	verbose = False
	name = os.path.splitext(receptor_filename)[0]
	rigid_filename=name+"_rigid.pdbqt"
	flexres_filename=name+"_flex.pdbqt"
	if verbose or DEBUG: print "[genFlex] rigid = ", rigid_filename
	if verbose or DEBUG: print "[genFlex] flexres = ", flexres_filename

	residue_selected = ListFlexResiduesNames.get()
	residue_selected = residue_selected.replace(" ","")
	if verbose or DEBUG: print "[genFlex] gen from ", residue_selected

	residue_to_move = residue_selected.replace(',','_')
	if verbose or DEBUG: print "These are residues to move", residue_to_move

	disallow = ""
	disallowed_pairs = ""
	r = Read(receptor_filename)[0]
	r.buildBondsByDistance()
	all_res = ResidueSet()
	res_names = residue_to_move.split('_')
	res_names = residue_selected.split(',')
	
	if verbose or DEBUG: print "res_names will be", res_names

	for n in res_names:
		res = r.chains.residues.get(lambda x: x.name==n)
		all_res += res

	d = {}
	for res in all_res: d[res] = 1
	all_res = d.keys()
	all_res = ResidueSet(all_res)
	all_bnds = BondSet()
	bnd_pairs = disallowed_pairs.split(':')
	for pair in bnd_pairs:
		names = pair.split('_')
		bnds = all_res.atoms.bonds[0].get(lambda x: x.atom1.name in names and x.atom2.name in names)
		all_bnds += bnds
	fdp = AD4FlexibleReceptorPreparation(r, residues=all_res, rigid_filename=rigid_filename, 
											flexres_filename=flexres_filename,
											non_rotatable_bonds=all_bnds)
	return rigid_filename, flexres_filename

def update_status(status_message):
	status = Label(p1, text=status_message, bd=1, relief=SUNKEN, anchor=S)
	status.pack(side=BOTTOM, fill=X)

def confirm():
	if tkMessageBox.askokcancel("Close Raccoon", "\nAre you sure you want to quit?\n\n(all unsaved data will be lost)\n"):
		root.destroy()

def MkJobDir(ligand_filename, receptor_stem, output_dir):
	global DirJournal
	LigNAME = os.path.basename(ligand_filename).rsplit('.', 1)[:-1][0]
	RecNAME = receptor_stem
	JobDir = output_dir+os.sep+LigNAME+"_"+RecNAME
	if JobDir in DirJournal: # to manage homonimy (same ligand filename from different directories)
		DirJournal.append(JobDir)
		JobDir = JobDir+"_"+str(DirJournal.count(JobDir))
	else:
		DirJournal.append(JobDir)
	try:
		if not os.path.exists(JobDir):
			os.makedirs(JobDir, 0755)
		else:
			return
		return JobDir
	except:
		return False

def MakeJobScript(ligand_dir, dpf_file, gpf_file):
	# generate run.sh in the ligand_dir
	if TargetOS.get() == "lin":
		if system == "Windows" and not cygwin.get():
			script_file = ligand_dir+os.sep+"run.bat"
			line = "@echo off"
			line = "REM Generated by AutoDock Raccoon"
			if gpf_file:
				gpf = os.path.basename(gpf_file)
				glg = gpf[:-3]+"glg"
				line += ("\necho Running AutoGrid...\nautogrid4.exe -p %s -l %s" % (gpf, glg) )
			dpf = os.path.basename(dpf_file)
			dlg = dpf[:-3]+"dlg"
			line += ("\necho Running AutoDock...\nautodock4.exe -p %s -l %s\n" % (dpf, dlg) )
		else:
			script_file = ligand_dir+os.sep+"run.sh"
			line = "#!/bin/bash\n# Generated by AutoDock Raccoon\n#\n#"
			line += "\n# Specify here the paths for the binaries, if necessary"
			if gpf_file:
				line += "\n"+"# autogrid = ''"
				line += "\n"+"# autodock = ''"
			else:
				line += "\n"+"# autodock = ''"
			if gpf_file:
				gpf = os.path.basename(gpf_file)
				glg = gpf[:-3]+"glg"
				line += ("\necho Running AutoGrid...\nautogrid4 -p %s -l %s" % (gpf, glg) )
			dpf = os.path.basename(dpf_file)
			dlg = dpf[:-3]+"dlg"
			line += ("\necho Running AutoDock...\nautodock4 -p %s -l %s\n" % (dpf, dlg) )
		script = open( script_file, 'w')
		script.writelines(line)
		script.close()
		if not system == "Windows": os.system("chmod +x %s" % (script_file))
		return True

def MakeMasterJobScript(path):
	header = """      ________________________________________________________________
__________//___________________________/////___________________/____________
_________/__/__________________________/____/__________________/____________
________/____/___________/_____________/_____/_________________/____________
________/____/__/_____/_/////___/////__/_____/__/////___/////__/___/________
_______/______/_/_____/__/_____/_____/_/_____/_/_____/_/_____/_/_//_________
_______////////_/_____/__/_____/_____/_/_____/_/_____/_/_______//_/_________
_______/______/_/____//__/___/_/_____/_/____/__/_____/_/_____/_/___/________
_______/______/__////_/___///___/////__/////____/////___/////__/____/_______
      ________________________________________________________________
                                 ______ 
                                /      \\ 
                               /        \\ 
                              /          \\   Raccoon
                              \\    /\\    /    Virtual 
                               \\  /  \\  /      Screening 
                                \\/ /\\ \\/        Generation      
                                 /\\  \\ 
                               /\\  \\__\\    version %s
                              /  \\__\\ 
                             /____\\ """ % version
	


	if TargetOS.get() == "lin":
		if system == "Windows" and not cygwin.get():
			line = "@echo off\nREM Generated by AutoDock Raccoon\necho.\n"
			command = "call run.bat"
			master_script_name = path+os.sep+"RunVS.bat"
			spacer = ""
			Q = ""
		else:
			line = "### Generated by AutoDock Raccoon\n"
			command = "./run.sh"
			master_script_name = path+os.sep+"RunVS.sh"
			Q = "'"
			spacer = "  "

		for i in header.split("\n"): # acrobatic moves for making a unified generator...
			line += "echo %s%s%s%s\n" % (Q, spacer, i, Q)

		if system == "Windows" and not cygwin.get():
			line += "echo.\necho                  == Press ENTER to start the calculation ==\n"
			line += "pause > NUL\n"
		else:
			line += "\necho -e \"\\n                 == Press ENTER to start the calculation ==\"\n"
			line += "read X\n"
			

		for DIR in DirJournal:
			dir = os.path.basename(DIR)
			line += ("echo %sDocking %s%s\n"% (Q, dir, Q)  )
			line += ("cd %s\n%s\ncd ..\n\n" % (dir, command))


		line += "echo %sCalculation completed.%s\n" % (Q,Q)
		if system == "Windows" and not cygwin.get():
			line += "pause > NUL\n"
		else:
			line += "read X\n"

		try:
			master_script = open(master_script_name, 'w')
			master_script.writelines(line)
			master_script.close()
		except:
			tkMessageBox.showerror("Master script generation.", ("An error occurred when trying to generate the jobs list file."))
			return False

		if not system == "Windows":
			os.system("chmod +x %s" % (master_script_name))

	if TargetOS.get() == "pbs":
		# create the list of job dirs in which to go
		# for submitting the calculation
		try:
			file = open(path+os.sep+'jobs_list', 'w')
			for DIR in DirJournal:
				dir = os.path.basename(DIR)
				print >> file, dir+"\n" 
			file.close()
		except:
			tkMessageBox.showerror("PBS script generation.", ("An error occurred when trying to generate the jobs list file."))
			return False
		CreateSmuggler(path)
		return True

def CreateSmuggler(path):
	# this function is called only for
	# PBS jobs
	if DEBUG: print "Creating the smuggler..."
	filename = "vs_submit.sh"
	end = PBShowmanyruns.get()
	line = "#!/bin/bash\n"
	line += "#\n# Generated with Raccoon | AutoDockVS\n#\n\n"

	line += "#### PBS jobs parameters"
	line += "CPUT=\"%s\"\n" % PBStime.get()
	line += "WALLT=\"%s\"\n" % PBStime.get()
	line += "#\n# There should be no reason\n"
	line += "# for changing the following values\n"
	line += "NODES=1\n"
	line += "PPN=1\n"
	line += "MEM=512mb\n\n\n"

	line += "### CUSTOM VARIABLES\n"
	line += "#\n"
	line += "# use the following line to set special options (e.g. specific queues)\n"
	line += "#OPT=\"-q MyPriorQueue\"\n"
	line += "OPT=\"\"\n\n\n"

	line += "# Paths for executables on the cluster \n"
	line += "# Modify them to specify custom executables to be used\n"
	line += "QSUB=\"qsub\"\n"
	line += "AUTODOCK=\"autodock4\"\n\n"
	# Set Autogrid if necessary"
	if MapSource.get() == 0:
		line += "AUTOGRID=\"autogrid4\"\n\n"

	line += "# Special path to move into before running\n"
	line += "# the screening. This is very system-specific,\n"
	line += "# so unless you're know what are you doing,\n"
	line += "# leave it as it is\n"
	line += "WORKING_PATH=`pwd`\n\n"

	line += "\n\n##################################################################################################\n"
	line += "##################################################################################################\n"
	line += "####### There should be no need to modify anything below this line ###############################\n"
	line += "##################################################################################################\n"
	line += "##################################################################################################\n\n\n"
	line += "#\n#\n\n"

	line += "type $AUTODOCK &> /dev/null || {\n"
	line += "        echo -e \"\\nError: the file [$AUTODOCK] doesn't exist or is not executable\\n\";\n"
	line += "        echo -e \"Try to specify the full path to the executable of the AutoDock binary in the script\";\n"
	line += "        echo -e \"( i.e. AUTODOCK=/usr/bin/autodock4 )\\n\\n\";\n"
	line += "        echo -e \" [ virtuals screening submission aborted]\\n\"\n"
	line += "        exit 1; }\n\n"
	line += ""

	if MapSource.get() == 0:
		line += "type $AUTOGRID &> /dev/null || {\n"
		line += "        echo -e \"\\nError: the file [$AUTOGRID] doesn't exist or is not executable\\n\";\n"
		line += "        echo -e \"Try to specify the full path to the executable of the AutoGrid binary in the script\";\n"
		line += "        echo -e \"( i.e. AUTOGRID=/usr/bin/autogrid4 )\\n\\n\";\n"
		line += "        echo -e \" [ virtuals screening submission aborted]\\n\"\n"
		line += "        exit 1; }\n\n"

	line += "type $QSUB &> /dev/null || {\n"
	line += "        echo -e \"\\nError: the file [$QSUB] doesn't exist or is not executable\\n\";\n"
	line += "        echo -e \"Try to specify the full path to the executable of the Qsub command binary in the script\";\n"
	line += "        echo -e \"( i.e. QSUB=/usr/bin/qsub )\\n\\n\";\n"
	line += "        echo -e \" [ virtuals screening submission aborted]\\n\"\n"
	line += "        exit 1; }\n\n"

	line += "echo Starting submission...\n"
	line += "for NAME in `cat jobs_list`\n"
	line += "    do\n"
	line += "        cd $NAME\n"
	# Set the extra loop for multiple DLG per ligand
	# and specify the name convention: ligand_protein.#.job
	if end > 1:
		line += "        for i in `seq 1 %s`\n" % str(end)
		line += "            do\n"
		job_name = "$NAME.$i.job"
		tab = "    "
	else:
		tab = ""
		job_name = "$NAME.job"

	line += "%s        echo \"#!/bin/bash\" > %s\n" % (tab, job_name)
	line += "%s        echo \"cd $WORKING_PATH/$NAME\" >> %s \n" % (tab, job_name)
	if MapSource.get() == 0:
		line += "%s        echo \"$AUTOGRID -p *.gpf -l grid_out.glg\" >> %s\n" % (tab, job_name)
	if end > 1:
		line += "%s        echo \"$AUTODOCK -p $NAME.dpf -l $NAME.$i.dlg\" >> %s\n" % (tab, job_name)
	else:
		line += "%s        echo \"$AUTODOCK -p $NAME.dpf -l $NAME.dlg\" >> %s\n" % (tab, job_name)

	line += "%s        chmod +x %s\n" % (tab, job_name)
	line += "%s        echo -n \"Submitting $NAME : \"\n" % tab
	line += "%s        $QSUB $OPT -l cput=$CPUT -l nodes=1:ppn=1 -l walltime=$WALLT -l mem=$MEM %s\n" % (tab, job_name) # remove the echo for making it active
	if end > 1:
		line += "        done\n"	
	line += "        cd ..\n"
	line += "done\n"
	try:
		output = open(path+os.sep+filename, 'w')
		output.writelines(line)
		output.close()
		if not system == "Windows":
			os.system("chmod +x %s" % (path+os.sep+filename))
		return True
	except:
		tkMessageBox.showerror("PBS script generation.", ("An error occurred when trying to generate the %s file." % filename))
		return False

def InitializeLog(outdir = None, filename = None):
	if not outdir and not filename:
		return False
	if not outdir:
		outdir = ""
	#global LogFile, first_time
	if system == "Windows":
		os.environ.get("USERNAME")
	else:
		user = os.environ["USER"]
	machine = system_info[1]
	operative_system = system_info[0]
	
	if TargetOS.get() == "lin":
		target_machine = "Workstation"
	if TargetOS.get() == "pbs":
		target_machine = "Linux clusters"
	if TargetOS.get() == "win":
		target_machine = "Windows"

	# take a look at the clock
	date = datetime.datetime.now()
	year = str(date.year)
	month = str(date.month)
	day = str(date.day)
	hour = str(date.hour)
	minute = str(date.minute)
	second = str(date.second) 			# too much?
	microsecond = str(date.microsecond)	# waaay to much!

	# VSgen-2009.7.26.log
	if not filename:
		log_name = outdir+os.sep+"raccoonVS-"+year+"."+month+"."+day+".log"
	else:
		log_name = filename
	
	full_date = date.strftime("%Y-%B-%d %H:%M")


	if RCstatus.get() == 0:
		receptor_count = 1	
	else:
		receptor_count = len(receptorScrolledListBox.get('0', END))

	ligand_count = str(TotalAcceptedLigands.get())

	tot_number_jobs = str( (TotalAcceptedLigands.get() * receptor_count  ) )

	header = """
 	      ________________________________________________________________
	
	__________//___________________________/////___________________/____________
	_________/__/__________________________/____/__________________/____________
	________/____/___________/_____________/_____/_________________/____________
	________/____/__/_____/_/////___/////__/_____/__/////___/////__/___/________
	_______/______/_/_____/__/_____/_____/_/_____/_/_____/_/_____/_/_//_________
	_______////////_/_____/__/_____/_____/_/_____/_/_____/_/_______//_/_________
	_______/______/_/____//__/___/_/_____/_/____/__/_____/_/_____/_/___/________
	_______/______/__////_/___///___/////__/////____/////___/////__/____/_______
	
	      ________________________________________________________________
	                                 ______ 
	                                /      \\ 
	                               /        \\ 
	                              /          \\   Raccoon
	                              \\    /\\    /    Virtual 
	                               \\  /  \\  /      Screening 
	                                \\/ /\\ \\/        Generation      
	                                 /\\  \\ 
	                               /\\  \\__\\    version %s
	                              /  \\__\\ 
	                             /____\\
		
		
                  date :\t%s
      output directory :\t%s
    total docking jobs :\t%s
      operative system :\t%s [ %s ]
   generating jobs for :\t%s


      ===================================== Ligand filters =========================================
	
                       Filtering criteria
                       ------------------
                                   MIN      MAX
                    Hb donors :   %4s  -  %4s
                 Hb acceptors :   %4s  -  %4s
             Molecular weight :   %4s  -  %4s
        Total number of atoms :   %4s  -  %4s
              Rotatable bonds :   %4s  -  %4s
		Reject non-AD atypes  :   %s
	
	
		Ligands accepted for the virtual-screening: %s


""" % ( version, full_date, outdir, tot_number_jobs, operative_system, machine, target_machine , str(HbDmin.get()), str(HbDmax.get()), str(HbAmin.get()), str(HbAmax.get()), str(MWmin.get()), str(MWmax.get()), str(NatMin.get()), str(NatMax.get()), str(TORSDOFmin.get()), str(TORSDOFmax.get()), str(DoRejectATypes.get()), ligand_count)   
	

	# receptor
	if RCstatus.get() == 0:
		receptor_log = "\n      ============================= Single target receptor ==========================================\n"
		receptor_log = receptor_log+"\n   Target structure:\nTARGET>\t"+ RecFilename.get()

	else:
		receptor_log = "\n      =========================== Multiple target receptors =========================================\n"
		receptor_log = receptor_log+"\n   Total target structures :" + str(receptor_count)+"\n"
		# append the list of receptor structures
		for rec in receptorScrolledListBox.get('0', END):
			receptor_log = receptor_log+"\nTARGET>\t"+rec
	header = header + receptor_log

	# flexible residues
	if DoFlex.get():
		if FlexResDefined.get():
			flex_log = "\n\n      ------------------------------- Flexible residues -----------------------------------\n\n"
			if DoFlexFromWhat.get() == 1:
				if FlexResFileName.get(): # TODO in theory it shouldn't be necessary
					flex_log = flex_log + "FLEX> Flexible residues from the file :\t"+FlexResFileName.get()
				else:
					if DEBUG : print "RETURNING A SHAMEFUL FALSE: problems in logging the flex residues [FlexResFileName.get() = ", FlexResFileName.get(), "]"
					return False
			if DoFlexFromWhat.get() == 2:
				if FlexResSelected.get(): # TODO in theory it shouldn't be necessary
					flex_log = flex_log + "FLEX> Flexible residues generated from the selection : "+ FlexResSelected.get()
				else:
					if DEBUG :print "RETURNING A SHAMEFUL FALSE: problems in logging the flex residues [FlexResSelected.get() = ", FlexResSelected.get(), "]"
					return False
			header = header + flex_log + "\n"


	
	# Maps
	maps_log = "\n\n      ===================================== Maps ====================================================\n"

	if MapSource.get() <= 1:
		if MapSource.get() == 0:
			maps_log = maps_log + "\n   Grid mode : calculated in each job.\n"
			maps_log = maps_log + "   Grid param file template :\n\n"
	
		if MapSource.get() == 1:
			if CacheMapPolicy.get() == "Make copies [ use more disk space ]":
				maps_log = maps_log + "\n   Grid mode : calculated now and >copied< in each ligand job directory.\n"
				maps_log = maps_log + "   Grid param file template :\n\n"
			if CacheMapPolicy.get() == "Make symbolic links [ save disk space ]":
				maps_log = maps_log + "\n   Grid mode : calculated now and >linked< in each ligand job directory.\n"
				maps_log = maps_log + "   Grid param file template :\n\n"
			maps_log = maps_log+("\t [ AutoGrid binary file used : |%s| ]" % AutoGridBin.get())

		# add the gpf lines to the log
		for line in GPFcontent.get('1.0', END).split('\n'):
			if not line.strip(): # get rid of empty lines
				continue
			else:
				maps_log = maps_log+"\nGPF>\t"+line#"\n"
		if GPFParameterFile.get():
			maps_log = maps_log+(" [ the parameter file |%s| has been copied ]\n\n" % GPFParameterFile.get())

	if MapSource.get() == 2:
		if CacheMapPolicy.get() == "Make copies [ use more disk space ]":
			cache_policy = " >copied< "
		if CacheMapPolicy.get() == "Make symbolic links [ save disk space ]":
			cache_policy = " >linked< "
		maps_log = maps_log + "\n   Grid mode : use pre-calculated"+cache_policy+"in each ligand job directory.\n"
		maps_log = maps_log + "   Grid cache dir : "+CacheMapDirName.get()

	header = header + maps_log


	docking_log = "\n\n     ==================================  Docking parameters ========================================\n"

	if docking_set.get() == "From template...":
		docking_log = docking_log+"\n   Docking mode : docking parameters will be >generated from template< for each ligand.\n"
		docking_log = docking_log+"   Docking param file template :\n\n"
		for line in DPFcontent.get(1.0, END).split('\n'):
			if not line.strip(): # get rid of empty lines
				continue
			else:
				docking_log = docking_log+"\nDPF>\t"+line
		if DPFParameterFile.get():
			docking_log = docking_log+("\n\n[ the parameter file %s has been copied ]" % DPFParameterFile.get())
	header = header + docking_log

	ligands_log = "\n\n     ======================================  Ligands list ============================================\n\n"
	for ligand in LigandDictionary.keys():
		if LigandDictionary[ligand]["accepted"]:
			ligands_log += "\nLIGAND> "+ligand
	header += ligands_log
	try:
		LOG = open(log_name, 'w')
	except:
		if DEBUG: print "problems in opening the log file"
		InfoMessage.set('Problems in opening the log file... generation aborted...')
		return False
	print >> LOG, header
	return LOG

def MakeTar(source_dir, tarfilename):

	if DEBUG:
		print "MakeTar> creating the tar from the source =>", source_dir
		print "MakeTar> The filename is	=>", tarfilename

	if TarFile.get() == "[disabled]":
		return True
	if TarFile.get() == "Tar (uncompressed)":
		filemode = "w"
		ext = ".tar"
	if TarFile.get() == "Tar (Bz2 compression)":
		filemode = "w:bz2"
		ext = ".tar.bz2"
	if TarFile.get() == "Tar (Gzip compression)":
		filemode = "w:gz"
		ext = ".tar.gz"

	tarfilename += ext
	InfoMessage.set('Writing the VS package...(this could take a while)')
	root.update()
	short_name = os.path.basename(source_dir)
	try:
		if DEBUG: print "Trying to generate the tar file", tarfilename
		vs_tar = tarfile.open(name = tarfilename, mode = filemode)
		root.update()
		vs_tar.add(source_dir, arcname = short_name)
		root.update()
		vs_tar.close()
		return True
	except:
		InfoMessage.set('Error in writing the VS package...')
		tkMessageBox.showwarning("Tar file error", "Unable to perform the operation.") 
		if DEBUG: print "problems in creating the tar file"
		return False


def MakeZip(source_dir, zipfilename):
	# compression level
	compression = zipfile.ZIP_DEFLATED

	zipfilename += ".zip"
	prefix = os.path.basename(source_dir)
	file_list = []
	InfoMessage.set('Creating the zip file...')
	root.update()
	try:
		output = zipfile.ZipFile(zipfilename, mode = 'w')
	except:
		InfoMessage.set('Zip file creation error!')
		root.update()
		return False
	for ROOT, SUBFOLDERS, FILES in os.walk(source_dir):
		if DEBUG:
			print "=================\nMAKEZIP > "
			print "ROOT", ROOT
			print "\tSUBFOLDS", SUBFOLDERS
			print "\t\tFILES", FILES
		for item in FILES:
			file_list.append(os.path.join(ROOT,item))

	for item in file_list:
		if DEBUG: print "Adding |%s| to %s" % (item, zipfilename)
		if not zipfilename in item: # to avoid a nice infinite, disk-hungry loop
			try:
				tmp = item
				shortname = tmp.replace(source_dir, prefix)
				output.write(item, arcname = shortname, compress_type = compression)
				InfoMessage.set('Adding files to the Zip file...(this could take a while)')
				root.update()
			except:
				InfoMessage.set('Error adding files to the Zip archive!')
				root.update()
				return False
	return True


def ImportLigList(filename = None):
	if not filename:
		filename = askopenfilename(title = "Select a ligand list file......", filetypes =[("Any file...", '*')])
		if not filename:
			return False
	try:
		file = open(filename, 'r')
		list = file.readlines()
		file.close()
	except:
		tkMessageBox.showwarning("Ligand list", "Warning: unable to open the selected file.") 
		return False
	if len(list)>0:
		before = len(LigandDictionary) # this remove spurious counts if there are duplicates in the file
		missing = []
		found = []
		for item in list:
			if not item[0] == "#":
				item = item.rstrip()
				if os.path.isfile(item):
					found.append(item)
				else:
					missing.append(item)
		if len(found) == 0:
			tkMessageBox.showwarning("Ligand list", "No ligands loaded!\nCheck the list content...\n(maybe it's not a list)")
			return False
		if len(missing) > 0 and tkMessageBox.askyesno("Ligands imported", "%d ligands have not been found.\n\nDo you want to inspect the list of rejected ligands?" % len(missing)):
			RejectedWindow = Toplevel()
			RejectedWindow.title("List of discarded ligands")
			scrollbar = Scrollbar(RejectedWindow)
			ListOfRejected = Listbox(RejectedWindow)
			CloseButton = Button(RejectedWindow, text = "Close", command = RejectedWindow.destroy)
			ListOfRejected.grid(column = 0, sticky = W+N+S+E)
			RejectedWindow.grid_rowconfigure(0, minsize = 300, weight = 1)
			RejectedWindow.grid_columnconfigure(0, minsize = 330, weight = 1)
			scrollbar.grid(row = 0, column = 1, sticky = S+N)
			scrollbar.config(command = ListOfRejected.yview)
			ListOfRejected.config(yscrollcommand=scrollbar.set)
			for item in missing:
				ListOfRejected.insert(END, item)
			CloseButton.grid(row = 2, columnspan = 2, sticky = W+E)
			return True
		else:
			openLigand(found)
			after = len(LigandDictionary) # this remove spurious counts if there are duplicates in the file
			tkMessageBox.showinfo("Ligand list", ("%d new ligands imported." % (after - before)))
			return True
	else:
		tkMessageBox.showwarning("Ligand list", "Empty file... apparently.") 
		return False

def ExportLigList():
	SaveLig = StringVar()
	SaveLig.set("all")
	header  = "# Ligand list saved by Raccoon"
	header += "# "

	def ExportDone(filename = None):
		ExportLigWin.destroy()

		list = []
		if SaveLig.get() == "all":
			for ligand in LigandDictionary:
				list.append(ligand)
		if SaveLig.get() == "accepted":
			for ligand in LigandDictionary:
				if LigandDictionary[ligand]["accepted"]: list.append(ligand)
		if SaveLig.get() == "rejected":
			for ligand in LigandDictionary:
				if not LigandDictionary[ligand]["accepted"]: list.append(ligand)
		if len(list):
			if not filename:
				filename = asksaveasfilename(title = "Select a ligand list file......", filetypes = [('Raccoon log file', '*.log'), ("Any file...", "*")] , defaultextension =[("Any file...", '*')])
			if not filename:
				EnableInterface()
				return
			file = open(filename, 'w')
			for item in list:
				print >> file, item
			file.close()
		EnableInterface()
		return

	def	ExportAbort():
		ExportLigWin.destroy()
		EnableInterface()	

	if not len(LigandDictionary):
		return
	try:
		ExportLigWin.lift()
	except:
		DisableInterface()	

		rejected = 0
		total = len(LigandDictionary.keys())
		for item in LigandDictionary.keys():
			if not LigandDictionary[item]["accepted"]:
				rejected += 1
		accepted = total - rejected

		all_msg      = "All ligands    [ %d ]" % total
		accepted_msg = "Accepted [ %d ]" % accepted
		rejected_msg = "Rejected  [ %d ]" % rejected

		ExportLigWin = Toplevel(root)
		ExportLigWin.title("Export list")
		ExportLigWin.winfo_toplevel().resizable(NO,NO)
		SelectionLevel = Pmw.Group(ExportLigWin, tag_text = "Select a set...")
		SaveLigDefault = Radiobutton(SelectionLevel.interior(), text=all_msg, variable = SaveLig, value = "all" )
		SaveLigDefault.grid(row = 0, column = 0, sticky = W) # Default
		Radiobutton(SelectionLevel.interior(), text=accepted_msg, variable = SaveLig, value = "accepted").grid(row = 1, column = 0, sticky = W, padx = 15)
		Radiobutton(SelectionLevel.interior(), text=rejected_msg, variable = SaveLig, value = "rejected").grid(row = 2, column = 0, sticky = W, padx = 15)
		SelectionLevel.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = W, columnspan = 2)
		SaveLigDefault.invoke()

		Button(ExportLigWin, text = "Save", command = ExportDone).grid(row = 10, column = 0, columnspan = 1, padx = 3, pady= 10)
		Button(ExportLigWin, text = "Cancel", command = ExportAbort).grid(row = 10, column = 1, padx = 3, pady= 10)
		#EnableInterface()

# Ligand page ############### p1 ################################
LigandButtonsGroup = Frame(p1, relief = FLAT)
AddLigandsButton = Button(LigandButtonsGroup, text='[ + ] Add ligands...', command = openLigand)
AddLigandsButton.pack(expand=YES, anchor=CENTER, side=LEFT)
AddLigandsDirButton = Button(LigandButtonsGroup, text='[ ++ ] Add a directory...', command = openLigandDir)
AddLigandsDirButton.pack(expand=YES, anchor=CENTER, side=LEFT)
AddLigandsDirRecursiveButton = Button(LigandButtonsGroup, text='[ +++ ] Add recursively...', command = openLigandDirRecursive)
AddLigandsDirRecursiveButton.pack(expand=YES, anchor=CENTER, side=LEFT)

LigandButtonsGroup.pack(fill = 'both', expand = 0, padx = 5, pady = 5, anchor = S)
Ligand_group = Pmw.Group(p1, tag_textvariable = LigandListLabel)
LigandScrolledListBox = Listbox(Ligand_group.interior(), selectmode=EXTENDED)
LigandScroll = Scrollbar(Ligand_group.interior(), command=LigandScrolledListBox.yview)
LigandScroll.pack(anchor = N, side = RIGHT, fill = 'y')
LigandScrolledListBox.configure(yscrollcommand=LigandScroll.set)
LigandScrolledListBox.grid(row = 1, column = 0, columnspan = 3, sticky = N+S+W+E)
LigandScrolledListBox.config(fg = 'black', font = ("Helvetica", 11, "bold"))
LigandScrolledListBox.pack(fill = BOTH, expand = 1)
Ligand_group.pack(fill = BOTH, expand = 1, padx = 10, pady = 10, side = TOP , anchor = N)

LigandPDBQTOptButton = Button(p1, text = "PDBQT generation options", command = LigandImportOptions)
LigandPDBQTOptButton.pack(expand = NO, anchor = W, side = LEFT)
FilterButton = Button(p1, text = "Filter ligand list...", command = LigandFilterOptions)
FilterButton.pack(expand = NO, anchor = W, side = LEFT)

RemoveLigandsButton = Button(LigandButtonsGroup, text='[ - ] Remove selected', command=removeLigand)
RemoveLigandsButton.pack(expand=YES, anchor=E, side=LEFT)
RemoveAllLigandsButton = Button(LigandButtonsGroup, text='[ --- ] Remove all', command=removeAllLigands)
RemoveAllLigandsButton.pack(expand=YES, anchor=E, side=LEFT)

# Receptor page ############### p2 ##################################
RCstatus.set(0)
MakeReceptorMenu()
# set defaults
Single_target_radio.invoke()
DoFlex.set(0)
SetFlexibleMode()

# Maps page ################### p3 ##################################
# AutoGrid options
AutoGridMenu = Pmw.Group(p3, tag_text="Run AutoGrid...") 
AutoGridWhen1 = Radiobutton(AutoGridMenu.interior(), text='at each job', value=0, variable=MapSource, command = MapMenu)
AutoGridWhen1.grid(row = 1, column = 0, ipadx = 5, ipady = 5)
AutoGridWhen2 = Radiobutton(AutoGridMenu.interior(), text='now (and cache the maps)', value=1, variable=MapSource, command = MapMenu)
AutoGridWhen2.grid(row = 1, column = 1)
AutoGridWhen3 = Radiobutton(AutoGridMenu.interior(), text='never (maps are already calculated)', value=2, variable=MapSource, command = MapMenu)
AutoGridWhen3.grid(row = 1, column = 2)
AutoGridMenu.pack(expand = 1, anchor = NW, padx = 10)

AGoptions = Pmw.Group(p3, tag_pyclass = None)
AutoGridExecButton = Button(AGoptions.interior(), text ="Set the AutoGrid executable", command = GetAutoGrid)
AutoGridExecLabel = Label(AGoptions.interior(),textvariable = AutoGridBin)
AutoGridExecButton.pack(side = TOP, padx = 10)
AutoGridExecLabel.pack(side = TOP, padx = 10)
AGoptions.pack(side = TOP, padx = 10)

MakeGPFMenu()

# set defaults
MapSource.set(0)
AutoGridWhen3.config(state = DISABLED)
AutoGridWhen1.invoke() # Select the default as "Run AG in each job"

# Docking page ########################## p4 ##############################

docking_set = StringVar()
docking_setup_interface("")

# Summary page  #################### p5 ###################################

# Create the "Toolbar" contents of the page.

Summary_group = Pmw.Group(p5, tag_text = 'Summary')
Label(Summary_group.interior(), text = "Ligands : ").grid(row = 1, column = 1, padx = 5, sticky = E)
Label(Summary_group.interior(), text = "Receptor(s) : ").grid(row = 2, column = 1, padx = 5, sticky = E)
Label(Summary_group.interior(), text = "Maps : ").grid(row = 3, column = 1, padx = 5, sticky = E)
Label(Summary_group.interior(), text = "Docking : ").grid(row = 4, column = 1, padx = 5, sticky = E)
SetOutDirButton = Button(Summary_group.interior(), text ="Set directory...", command = SetJobDirectory, fg = 'red', justify = LEFT)
SetOutDirButton.grid(row = 5, column = 1, padx = 5, sticky = E)

LigSummaryLabel = Label(Summary_group.interior(), textvariable = LigandSummary, justify = LEFT)
LigSummaryLabel.grid(row = 1, column = 2, padx = 5, sticky = W)

RecSummaryLabel = Label(Summary_group.interior(), textvariable = ReceptorSummary, justify = LEFT)
RecSummaryLabel.grid(row = 2, column = 2, padx = 5, sticky = W)

MapsSummaryLabel = Label(Summary_group.interior(), textvariable = MapsSummary, justify = LEFT)
MapsSummaryLabel.grid(row = 3, column = 2, padx = 5, sticky = W)

DockSummaryLabel = Label(Summary_group.interior(), textvariable = DockingSummary, justify = LEFT)
DockSummaryLabel.grid(row = 4, column = 2, padx = 5, sticky = W)

OutputDirLabel = Label(Summary_group.interior(), textvariable = JobDirectory, justify = LEFT)
OutputDirLabel.grid(row = 5, column = 2, padx = 5, sticky = W)
OutputDirLabelInfo = Label(Summary_group.interior(), textvariable = JobDirectoryInfo)
OutputDirLabelInfo.grid(row = 6, column = 1, columnspan = 3, padx = 5, sticky = S) #, columnspan = 2)

JobsSummaryLabel = Label(Summary_group.interior(), textvariable = JobsSummary)
JobsSummaryLabel.grid(row = 7, column = 1, columnspan = 2, padx = 5, sticky = S)
Summary_group.pack(anchor = N, side = TOP, fill = 'both', expand = 1, padx = 10, pady = 10)#

LigSummaryLabel.config(fg = 'red')
RecSummaryLabel.config(fg = 'red')
MapsSummaryLabel.config(fg = 'red')
DockSummaryLabel.config(fg = 'red')

# OS specific options
Summary_group2 = Pmw.Group(p5, tag_text = 'OS Options')
LinuxOptionsPanel = Pmw.Group(Summary_group2.interior(), tag_pyclass = None)
PBSOptionsPanel = Pmw.Group(Summary_group2.interior(), tag_pyclass = None)
WinOptionsPanel = Pmw.Group(Summary_group2.interior(), tag_pyclass = None)
SystemButton1 = Radiobutton(Summary_group2.interior(), text='Workstation', value='lin', variable=TargetOS, command = GetOSoption)
SystemButton1.grid(row = 1, column = 0, sticky = W)
SystemButton2 = Radiobutton(Summary_group2.interior(), text='Linux cluster', value='pbs', variable=TargetOS, command = GetOSoption)
SystemButton2.grid(row = 1, column = 1, sticky = W)


if system == "Linux" or system == "Darwin":
	SystemButton1.invoke()
if system == "Windows":
	SystemButton1.invoke()

Summary_group2.pack(anchor = S, side = TOP, fill = 'both', expand = 1, padx = 10, pady = 10)#

# AutoDock Logo
Logo = Canvas(root, width =360, height=73)
logo = Tkinter.PhotoImage(master=root, data=LOGO_BASE64)
Logo.create_image(170,35, image=logo, anchor=CENTER)
Logo.pack(anchor=CENTER, side = BOTTOM)

InfoInit() # Generate the info bar

# Line for avoiding the destruction of the window
root.protocol("WM_DELETE_WINDOW", confirm)

# FINAL GENERATE BUTTON
TheButton = Button(p5, text='G E N E R A T E', fg='black', state = DISABLED, command = TheFunction, height = 3 )
TheButton.pack(pady=2, fill = 'both', padx = 10)
#nb.setnaturalsize() # Resize automatically the window ORIGINAL
makemenu(root)
#root.geometry("800x600")
root.mainloop()

if DEBUG: print "KTHXBY"

