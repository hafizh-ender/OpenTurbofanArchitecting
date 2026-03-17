"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Copyright: (c) 2020, Deutsches Zentrum fuer Luft- und Raumfahrt e.V.
Contact: jasper.bussemaker@dlr.de

Simple architecting problem: only contains existing engine architectures,
1 objective (TSFC) and no constraints.
"""


import os
import time
import pickle
import multiprocessing

os.environ['OPENMDAO_REQUIRE_MPI'] = 'false'  # Suppress OpenMDAO MPI import warnings

from open_turb_arch.architecting import *
from open_turb_arch.architecting.metrics import *
from open_turb_arch.architecting.turbofan import *
from open_turb_arch.evaluation.analysis import *

from open_turb_arch.architecting.pymoo import *
from pymoo.optimize import minimize
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.operators.sampling.latin_hypercube_sampling import LatinHypercubeSampling


def get_architecting_problem():
    analysis_problem = AnalysisProblem(
        design_condition=DesignCondition(
            # mach=1e-6,  # Mach number [-]
            # alt=0,  # Altitude [ft]
            # thrust=150e3,  # Thrust [N]
            # turbine_in_temp=1450,  # Turbine inlet temperature [C]
            # bleed_offtake=0.5,  # Extraction bleed offtake [kg/s]
            # power_offtake=37.5e3,  # Power offtake [W]
            balancer=DesignBalancer(init_turbine_pr=10, init_mass_flow=400, init_extraction_bleed_frac=0.02),
            
            # mach=0.78,  # Mach number [-]
            # alt=10668 * 3.28084,  # Altitude [ft]
            # thrust=24900,  # Thrust [N]
            # d_temp=10.0,  # Temperature difference to standard atmosphere [K]
            # turbine_in_temp=1800 - 273.15,  # Turbine inlet temperature [C]
            # bleed_offtake=0,  # Extraction bleed offtake [kg/s]
            # power_offtake=50000,  # Power offtake [W]
            
            mach=0.78,  # Mach number [-]
            alt=10668 * 3.28084,  # Altitude [ft]
            thrust=24900,  # Thrust [N]
            d_temp=0.,  # Temperature difference to standard atmosphere [K]
            turbine_in_temp=1800 - 273.15,  # Turbine inlet temperature [C]
            bleed_offtake=0,  # Extraction bleed offtake [kg/s]
            power_offtake=50000,  # Power offtake [W]
        )
    )

    return ArchitectingProblem(
        analysis_problem=analysis_problem,
        choices=[
            # FanChoice(),
            # ShaftChoice(),
            # GearboxChoice(),
            # NozzleMixingChoice(),
            # OfftakesChoice(),
            
            FanChoice(fix_include_fan=True), 
            CRTFChoice(fix_include_crtf=False),
            ShaftChoice(
                fixed_number_shafts=2,    
                ),
            GearboxChoice(fix_include_gear=False),
            AfterburnerChoice(fix_include_afterburner=False),
            ITBChoice(fix_include_itb=False),     
            CoolingBleedChoice(
                # Detail: 
                # recirculating: inter-bleed HPC-burner to LPC:                         0%
                # handling bleed: inter-bleed HPC-LPC (extraction bleed)                0%
                # overboard bleed: intra-bleed HPC (extraction bleed)                   0.5%
                # LPT cooling: intra-bleed HPC to LPT                                   2%
                # HP leakage (a): inter-bleed HPC-burner (extraction bleed)             0%
                # NGV cooling (b): inter-bleed HPC-burner to HPT (stator part)          5%
                # HPT cooling (c): inter-bleed HPC-burner to HPT (rotor part)           5%
                # HP leak to LPT exit: inter-bleed HPC-burner to LPT                    0%
                # Translation: LPC to IPC
                
                # # Inter-bleed HPC-burner
                # fix_eb_hb_total = 0.10,  # Fix the total cooling bleed portion of the inter-bleed between the HPC and burner
                # fix_eb_hbi_frac_w = 0,  # Fix the cooling bleed portion of the IPT as target of the inter-bleed between the HPC and burner
                # fix_eb_hbl_frac_w = 0,  # Fix the cooling bleed portion of the LPT as target of the inter-bleed between the HPC and burner

                # # Inter-bleed IPC-HPC
                # fix_eb_ih_total = 0,  # Fix the total cooling bleed portion of the inter-bleed between the IPC and HPC
                # fix_eb_ihi_frac_w = 0,  # Fix the cooling bleed portion of the IPT as target of the inter-bleed between the IPC and HPC
                # fix_eb_ihl_frac_w = 0,  # Fix the cooling bleed portion of the LPT as target of the inter-bleed between the IPC and HPC

                # # Inter-bleed LPC-IPC
                # fix_eb_li_total = 0,  # Fix the total cooling bleed portion of the inter-bleed between the LPC and IPC
                # fix_eb_lii_frac_w = 0,  # Fix the cooling bleed portion of the IPT as target of the inter-bleed between the LPC and IPC
                # fix_eb_lil_frac_w = 0,  # Fix the cooling bleed portion of the LPT as target of the inter-bleed between the LPC and IPC

                # # Intra-bleed HPC
                # fix_ab_hpc_total = 0.02,  # Fix the total cooling bleed portion of the HPC intra-bleed
                # fix_ab_hi_frac_w = 1,  # Fix the cooling bleed portion of the IPT as target of the HPC intra-bleed
                # fix_ab_hl_frac_w = 0,  # Fix the cooling bleed portion of the LPT as target of the HPC intra-bleed

                # # Intra-bleed IPC
                # fix_ab_ipc_total = 0,  # Fix the total cooling bleed portion of the IPC intra-bleed
                # fix_ab_ii_frac_w = 0,  # Fix the cooling bleed portion of the IPT as target of the IPC intra-bleed
                # fix_ab_il_frac_w = 0,  # Fix the cooling bleed portion of the LPT as target of the IPC intra-bleed

                # # Intra-bleed LPC
                # fix_ab_lpc_total = 0,  # Fix the total cooling bleed portion of the LPC intra-bleed
                # fix_ab_li_frac_w = 0,  # Fix the cooling bleed portion of the IPT as target of the LPC intra-bleed
                # fix_ab_ll_frac_w = 0,  # Fix the cooling bleed portion of the LPT as target of the LPC intra-bleed
            ),
            NozzleMixingChoice(fix_include_mixing=False),       # no nozzle mixing
            IntercoolerChoice(fix_include_ic=False),        # no intercooler   
            OfftakesChoice(
                fix_power_offtake_location=1, # 1: HPC, 2: IPC, 3: LPC
                fix_bleed_offtake_location=1, # 1: HPC, 2: IPC, 3: LPC
            ), 
        ],
        objectives=[
            TSFCMetric(),
            WeightMetric(),
            NoiseMetric(),
        ],
        constraints=[
            # JetMachMetric(max_jet_mn=1.),
        ],
        metrics=[
            TSFCMetric(),
            WeightMetric(),
            LengthMetric(),
            DiameterMetric(),
            NOxMetric(),
            NoiseMetric(),
            JetMachMetric(),
            BurnerInletTemperatureMetric(),
            TurbineInletTemperatureMetric(),
            P17Q7Metric(),
            WRQAE2AMetric(),
            DHQT41Metric(),
            DHQT46Metric(),
        ],
    )


def get_pymoo_architecting_problem():
    return PymooArchitectingProblem(get_architecting_problem())


if __name__ == '__main__':
    architecting_problem = get_architecting_problem()

    architecting_problem.print_results = True
    architecting_problem.verbose = True
    architecting_problem._max_iter = 30
    architecting_problem.save_results_folder = 'results_latest_multi2'  # Insert folder name to save results
    architecting_problem.save_results_combined = True

    # The number of processes to be used
    # with multiprocessing.Pool(2) as pool:
    t = time.time()
    problem = PymooArchitectingProblem(architecting_problem)
    # problem.parallelization = ('starmap', pool.starmap)

    algorithm = NSGA2(
        pop_size=66,
        sampling=LatinHypercubeSampling()
    )
    result = minimize(problem, algorithm, termination=('n_eval', 66*20), verbose=True, save_history=True)
    elapsed = time.time() - t

    architecting_problem.finalize()
    with open(architecting_problem.save_results_folder+'/pymoo_algo_results.pkl', 'wb') as fp:
        pickle.dump(result, fp)
        
    hour, minute, second = elapsed//3600, (elapsed%3600)//60, elapsed%60
    print('Elapsed time: %.2f hours, %.2f minutes, %.2f seconds' % (hour, minute, second))
