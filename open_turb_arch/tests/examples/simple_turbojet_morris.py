import json
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

import numpy as np

from SALib.sample import morris as morris_sample
from SALib.analyze import morris as morris_analyze

def get_architecting_problem():
    analysis_problem = AnalysisProblem(
        design_condition=DesignCondition(
            # mach=0.78,  # Mach number [-]
            # alt=10668 * 3.28084,  # Altitude [ft]
            # thrust=24900,  # Thrust [N]
            # d_temp=10.0,  # Temperature difference to standard atmosphere [K]
            # turbine_in_temp=1800 - 273.15,  # Turbine inlet temperature [C]
            # bleed_offtake=0,  # Extraction bleed offtake [kg/s]
            # power_offtake=0,  # Power offtake [W]
            # balancer=DesignBalancer(),
            
            # mach=0.8,  # Mach number [-]
            # alt=35000,  # Altitude [ft]
            # thrust=22500,  # Thrust [N]
            # d_temp=0.,  # Temperature difference to standard atmosphere [K]
            # turbine_in_temp=1600 - 273.15,  # Turbine inlet temperature [C]
            # bleed_offtake=0.98,  # Extraction bleed offtake [kg/s]
            # power_offtake=52000,  # Power offtake [W]
            # balancer=DesignBalancer(),
            
            mach=0.78,  # Mach number [-]
            alt=10668 * 3.28084,  # Altitude [ft]
            thrust=24900,  # Thrust [N]
            d_temp=0.,  # Temperature difference to standard atmosphere [K]
            turbine_in_temp=1800 - 273.15,  # Turbine inlet temperature [C]
            bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
            power_offtake=50000,  # Power offtake [W]
            balancer=DesignBalancer(
                init_turbine_pr=10,
                init_mass_flow=90,
                init_extraction_bleed_frac=0.02),
        ),
        evaluate_conditions=[
        #     EvaluateCondition(
        #         name_='Cruise',
        #         mach=0.78,  # Mach number [-]
        #         alt=10668 * 3.28084,  # Altitude [ft]
        #         thrust=20400,  # Thrust [N]
        #         balancer=OffDesignBalancer(
        #             init_bpr=3.8,
        #             init_shaft_rpm=7500.,
        #             init_mass_flow=100.,
        #             init_far=.025,
        #             init_extraction_bleed_frac=0.01
        #         ),
        #         d_temp=0.,  # Temperature difference to standard atmosphere [K]
        #         bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
        #         power_offtake=50000,  # Power offtake [W]
        #     ),
        #     EvaluateCondition(
        #         name_='MCL1',
        #         mach=0.71,  # Mach number [-]
        #         alt=9449 * 3.28084,  # Altitude [ft]
        #         thrust=27200,  # Thrust [N]
        #         balancer=OffDesignBalancer(
        #             init_bpr=3.8,
        #             init_shaft_rpm=7500.,
        #             init_mass_flow=100.,
        #             init_far=.025,
        #             init_extraction_bleed_frac=0.01
        #         ),
        #         d_temp=0.,  # Temperature difference to standard atmosphere [K]
        #         bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
        #         power_offtake=50000,  # Power offtake [W]
        #     ),
        #     # EvaluateCondition(
        #     #     name_='MCL0',
        #     #     mach=0.45,  # Mach number [-]
        #     #     alt=3048 * 3.28084,  # Altitude [ft]
        #     #     thrust=58000,  # Thrust [N]
        #     #     balancer=OffDesignBalancer(
        #     #         init_bpr=3.8,
        #     #         init_shaft_rpm=7500.,
        #     #         init_mass_flow=100.,
        #     #         init_far=.025,
        #     #         init_extraction_bleed_frac=0.01
        #     #     ),
        #     #     d_temp=0.,  # Temperature difference to standard atmosphere [K]
        #     #     bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
        #     #     power_offtake=50000,  # Power offtake [W]
        #     # ),
        #     # EvaluateCondition(
        #     #     name_='TakeOff',
        #     #     mach=0.25,  # Mach number [-]
        #     #     alt=1e-6,  # Altitude [ft]
        #     #     thrust=105000,  # Thrust [N]
        #     #     balancer=OffDesignBalancer(
        #     #         init_bpr=8.5,
        #     #         init_shaft_rpm=8000.,
        #     #         init_mass_flow=200.,
        #     #         init_far=.025,
        #     #         init_extraction_bleed_frac=0.01
        #     #     ),
        #     #     d_temp=0.,  # Temperature difference to standard atmosphere [K]
        #     #     bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
        #     #     power_offtake=50000,  # Power offtake [W]
        #     # ),
        ]
    )

    return ArchitectingProblem(
        analysis_problem=analysis_problem,
        choices=[
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
        constraints=[],
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


if __name__ == '__main__':

    architecting_problem = get_architecting_problem()
    architecting_problem.verbose = False
    architecting_problem._max_iter = 30
    
    save_folder = 'results_latest_morris_15'
    save_filename = 'morris_results.txt'
    # save_filename_combined = 'morris_results_combined.pkl'
    save_filename_combined = 'morris_results_combined.json'
    
    os.makedirs(save_folder, exist_ok=True)

    free_dv_names = [des_var.name for des_var in architecting_problem.free_opt_des_vars]
    print('Free design variable names: %r' % free_dv_names)
    
    active_dv_names = [
              'bpr',
              'fpr',
              'opr',
              'pr_compressor_ip',
              
            #   'pr_compressor_lp',
            
              'rpm_shaft_hp',
              'rpm_shaft_ip',
              
            #   'rpm_shaft_ip_frac',   # 'rpm_shaft_ip' / 'rpm_shaft_hp'
            
            #   'rpm_shaft_lp',
            #   'gear_ratio',
            #   'far_ab',
            #   'far_itb',
            
            #   'eb_hb_total',
            #   'eb_hbi_frac_w',
              
            #   'eb_hbl_frac_w',
            
            #   'eb_ih_total',
            #   'eb_ihi_frac_w',
              
            #   'eb_ihl_frac_w',
            #   'eb_li_total',
            #   'eb_lii_frac_w',
            #   'eb_lil_frac_w',
            
            #   'ab_hpc_total',
            #   'ab_hi_frac_w',
              
            #   'ab_hl_frac_w',
            
            #   'ab_ipc_total',
            #   'ab_ii_frac_w',
              
            #   'ab_il_frac_w',
            #   'ab_lpc_total',
            #   'ab_li_frac_w',
            #   'ab_ll_frac_w',
            #   'ic_location',
            #   'radius',
            #   'length',
            #   'number'
              ]

    active_dv_ranges = [
            [4.5, 12.], # bpr
            [1.2, 1.6], # fpr
            [20., 80.], # opr
            [0.05, 0.20], # pr_compressor_ip
            
            # [0.1, 0.9], # pr_compressor_lp
            
            [9000., 20000.], # rpm_shaft_hp
            [3000., 7000.], # rpm_shaft_ip 
            ## [0.2, 0.8], # rpm_shaft_ip_frac                  
            
            # [1000., 10000.], # rpm_shaft_lp
            # [1., 5.], # gear_ratio
            # [0., 0.05], # far_ab
            # [0., 0.05], # far_itb
            
            # [0., 0.15], # eb_hb_total
            # [0., 1.], # eb_hbi_frac_w
            
            # [0., 1.], # eb_hbl_frac_w
            
            # [0., 0.15], # eb_ih_total
            # [0., 1.], # eb_ihi_frac_w
            
            # [0., 1.], # eb_ihl_frac_w
            # [0., 0.1], # eb_li_total
            # [0., 1.], # eb_lii_frac_w
            # [0., 1.], # eb_lil_frac_w
            
            # [0., 0.15], # ab_hpc_total
            # [0., 1.], # ab_hi_frac_w
            
            # [0., 1.], # ab_hl_frac_w
            
            # [0., 0.15], # ab_ipc_total
            # [0., 1.], # ab_ii_frac_w
            
            # [0., 1.], # ab_il_frac_w
            # [0., 0.1], # ab_lpc_total
            # [0., 1.], # ab_li_frac_w
            # [0., 1.], # ab_ll_frac_w
            # [0, 2],   # ic_location (categorical: 0: none, 1: HPC-ITB, 2: IPC-ITB, 3: LPC-ITB)
            # [0.01, 0.05],   # radius (m)
            # [0.01, 0.05],   # length (m)
            # [1, 251]    # number (integer)
        ]

    # Check if length of active_dv_names and active_dv_ranges match
    assert len(active_dv_names) == len(active_dv_ranges), "It's not the same"
    
    # 1. Define the design space (your inputs)
    problem = {
        'num_vars': len(active_dv_names),
        'names': active_dv_names,
        'bounds': active_dv_ranges
    }

    # 2. Generate the samples (trajectories)
    # N = Number of trajectories. 
    # Total model evaluations = N * (num_vars + 1)
    # For Morris, N is typically between 10 and 1000.
    # X_samples = morris_sample.sample(problem, N=1000, num_levels=4, optimal_trajectories=100)
    X_samples = morris_sample.sample(problem, N=100, num_levels=4, optimal_trajectories=None)

    print(f"X_samples shape: {X_samples.shape}")
    print(f"Total model evaluations required: {X_samples.shape[0]}")

    # 3. Define or wrap your model/metric evaluation
    # If using OpenMDAO/pyCycle, you would loop through X_samples, 
    # set the inputs in your model, run the model, and record the output.
    def save_results(**kwargs):
        with open(os.path.join(save_folder, save_filename), 'a') as f:
            f.write(str(kwargs) + '\n')
    
    def run_my_model(X):
        # Initialize Y as an empty list of (architecting_problem.metrics.shape * len(X))
        Y = np.zeros((X.shape[0], len(architecting_problem.metrics)))

        for i, x in enumerate(X):
            
            
            # Change x to dict
            x_dict = {name: value for name, value in zip(active_dv_names, x)}
            
            print(f"Running model for sample {i+1}/{X.shape[0]} with design variables: {x_dict}")
            
            # Change init turbine pr
            architecting_problem.analysis_problem.design_condition.balancer._init_turbine_pr = (x_dict['opr']/x_dict['fpr'])**(0.5)
            architecting_problem.analysis_problem.design_condition.balancer._init_mass_flow = 20 * x_dict['bpr']
            
            print(f"Initial turbine PR set to: {architecting_problem.analysis_problem.design_condition.balancer._init_turbine_pr}")
            print(f"Initial mass flow set to: {architecting_problem.analysis_problem.design_condition.balancer._init_mass_flow} kg/s")

            dv = [
                x_dict['bpr'],     # BPR
                x_dict['fpr'],     # FPR
                x_dict['opr'],    # OPR
                x_dict['pr_compressor_ip'],             # % of IPC PR
                
                0,              # % of LPC PR
                x_dict['rpm_shaft_hp'],          # HP Shaft RPM
                x_dict['rpm_shaft_ip'],          # IP Shaft RPM
                # 0,# x_dict['rpm_shaft_ip_frac'] * x_dict['rpm_shaft_hp'],          # IP Shaft RPM
                
                0,              # LP Shaft RPM
                0,              # Gear Ratio
                0,              # Afterburner FAR
                0,              # Inter Turbine Burner FAR
                0,#x_dict['eb_hb_total'],           # Inter-bleed HPC-burner total cooling bleed portion
                0,#x_dict['eb_hbi_frac_w'],              # Inter-bleed HPC-burner cooling bleed portion of the IPT as target
                0,          # Inter-bleed HPC-burner cooling bleed portion of the LPT as target
                0,#x_dict['eb_ih_total'],          # Inter-bleed IPC-HPC total cooling bleed portion
                0,#x_dict['eb_ihi_frac_w'],          # Inter-bleed IPC-HPC cooling bleed portion of the IPT as target
                0,          # Inter-bleed IPC-HPC cooling bleed portion of the LPT as target
                0,          # Inter-bleed LPC-IPC total cooling bleed portion
                0,          # Inter-bleed LPC-IPC cooling bleed portion of the IPT as target
                0,          # Inter-bleed LPC-IPC cooling bleed portion of the LPT as target
                0,#x_dict['ab_hpc_total'],       # HPC intra-bleed total cooling bleed portion
                0,#x_dict['ab_hi_frac_w'],          # HPC intra-bleed cooling bleed portion of the IPT as target
                0,          # HPC intra-bleed cooling bleed portion of the LPT as target
                0,#x_dict['ab_ipc_total'],          # IPC intra-bleed total cooling bleed portion
                0,#x_dict['ab_ii_frac_w'],          # IPC intra-bleed cooling bleed portion of the IPT as target
                0,          # IPC intra-bleed cooling bleed portion of the LPT as target
                0,          # LPC intra-bleed total cooling bleed portion
                0,          # LPC intra-bleed cooling bleed portion of the IPT as target
                0,          # LPC intra-bleed cooling bleed portion of the LPT as target
                0,          # Intercooler location
                0,          # Intercooler radius
                0,          # Intercooler length
                0,          # Number of intercooler pipes
            ]
            
            _, imputed_dv = architecting_problem.generate_architecture(dv)
            _, _, _, metrics = architecting_problem.evaluate(imputed_dv)
            
            # If result contain nan, replace with "NaN" so that it can be saved in json
            metrics = [metric if not np.isnan(metric) else "NaN" for metric in metrics]
            
            if 'NaN' in metrics:
                print(f"Sample {i+1} has NaN in results. Retry with larger initial mass flow rate.")
                
                architecting_problem.analysis_problem.design_condition.balancer._init_turbine_pr = (82.93060324)**(0.45)
                architecting_problem.analysis_problem.design_condition.balancer._init_mass_flow = 20 * 3.11309372
                print(f"Retrying Sample {i+1} with initial mass flow set to: {architecting_problem.analysis_problem.design_condition.balancer._init_mass_flow} kg/s")
                
                _, imputed_dv = architecting_problem.generate_architecture(dv)
                _, _, _, metrics = architecting_problem.evaluate(imputed_dv)
                metrics = [metric if not np.isnan(metric) else "NaN" for metric in metrics]
                    
            # Save the results in Y
            Y[i, :] = metrics
            print(f"Sample {i+1} results: {metrics}")
            
            # Save the results into a file after each evaluation (optional, for large runs)
            save_results(
                sample_index=i,
                x=x.tolist() if isinstance(x, np.ndarray) else x,
                y=metrics
            )
            
        return Y

    Y_samples = run_my_model(X_samples)
    
    # Save X_samples and Y_samples together in a combined file as json
    combined_results = {
        'X_samples': X_samples.tolist() if isinstance(X_samples, np.ndarray) else X_samples,
        'Y_samples': Y_samples.tolist() if isinstance(Y_samples, np.ndarray) else Y_samples,
    }
    
    # with open(os.path.join(save_folder, save_filename_combined), 'wb') as f:
    #     pickle.dump(combined_results, f)
    
    with open(os.path.join(save_folder, save_filename_combined), 'w') as f:
        json.dump(combined_results, f, indent=4)