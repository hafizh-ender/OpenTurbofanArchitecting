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

Simple turbojet example based on pycycle.example_cycles.simple_turbojet
"""


from open_turb_arch.architecting import *
from open_turb_arch.architecting.metrics import *
from open_turb_arch.architecting.turbofan import *
from open_turb_arch.evaluation.analysis import *

import numpy as np

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
                init_turbine_pr=8,
                init_mass_flow=80,
                init_extraction_bleed_frac=0.02),
        ),
        evaluate_conditions=[
            # EvaluateCondition(
            #     name_='Cruise',
            #     mach=0.78,  # Mach number [-]
            #     alt=10668 * 3.28084,  # Altitude [ft]
            #     thrust=20400,  # Thrust [N]
            #     balancer=OffDesignBalancer(
            #         init_bpr=3.8,
            #         init_shaft_rpm=7500.,
            #         init_mass_flow=100.,
            #         init_far=.025,
            #         init_extraction_bleed_frac=0.01
            #     ),
            #     d_temp=0.,  # Temperature difference to standard atmosphere [K]
            #     bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
            #     power_offtake=50000,  # Power offtake [W]
            # ),
            # EvaluateCondition(
            #     name_='MCL1',
            #     mach=0.71,  # Mach number [-]
            #     alt=9449 * 3.28084,  # Altitude [ft]
            #     thrust=27200,  # Thrust [N]
            #     balancer=OffDesignBalancer(
            #         init_bpr=3.8,
            #         init_shaft_rpm=7500.,
            #         init_mass_flow=100.,
            #         init_far=.025,
            #         init_extraction_bleed_frac=0.01
            #     ),
            #     d_temp=0.,  # Temperature difference to standard atmosphere [K]
            #     bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
            #     power_offtake=50000,  # Power offtake [W]
            # ),
            # EvaluateCondition(
            #     name_='MCL0',
            #     mach=0.45,  # Mach number [-]
            #     alt=3048 * 3.28084,  # Altitude [ft]
            #     thrust=58000,  # Thrust [N]
            #     balancer=OffDesignBalancer(
            #         init_bpr=3.8,
            #         init_shaft_rpm=7500.,
            #         init_mass_flow=100.,
            #         init_far=.025,
            #         init_extraction_bleed_frac=0.01
            #     ),
            #     d_temp=0.,  # Temperature difference to standard atmosphere [K]
            #     bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
            #     power_offtake=50000,  # Power offtake [W]
            # ),
            # EvaluateCondition(
            #     name_='TakeOff',
            #     mach=0.25,  # Mach number [-]
            #     alt=1e-6,  # Altitude [ft]
            #     thrust=105000,  # Thrust [N]
            #     balancer=OffDesignBalancer(
            #         init_bpr=8.5,
            #         init_shaft_rpm=8000.,
            #         init_mass_flow=200.,
            #         init_far=.025,
            #         init_extraction_bleed_frac=0.01
            #     ),
            #     d_temp=0.,  # Temperature difference to standard atmosphere [K]
            #     bleed_offtake=0.,  # Extraction bleed offtake [kg/s]
            #     power_offtake=50000,  # Power offtake [W]
            # ),
        ]
    )

    return ArchitectingProblem(
        analysis_problem=analysis_problem,
        choices=[
            # FanChoice(fix_include_fan=True, fan_eff=0.8948), 
            FanChoice(fix_include_fan=True), 
            CRTFChoice(fix_include_crtf=False),
            ShaftChoice(
                fixed_number_shafts=2,          
                # comp_hp_eff=0.8707,
                # comp_ip_eff=0.9243,
                # turb_hp_eff=0.8888,
                # turb_ip_eff=0.8996
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
    print(architecting_problem._an_problem.__dict__)
    
    architecting_problem.print_results = True
    architecting_problem.verbose = True
    architecting_problem._max_iter = 30
    
    print("There are %d design variables: " % len(architecting_problem.opt_des_vars))
    # for i, des_var in enumerate(architecting_problem.opt_des_vars):
    #     print('  %d: %s. is fixed: %s' % (i, des_var.name, des_var.is_fixed))
    full_dv_names = [des_var.name for des_var in architecting_problem.opt_des_vars]
    print('Design variable names: %r' % full_dv_names)
    
    print("")
    
    free_dv_names = [des_var.name for des_var in architecting_problem.free_opt_des_vars]
    print('Free design variable names: %r' % free_dv_names)
    
    active_dv_names = ['bpr',
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
    x_arr = [2.8333333333333335, 3.2, 40.0, 0.1, 20000.0, 7000.0]
    x_dict = {name: value for name, value in zip(active_dv_names, x_arr)}
    
    # dv = [0] * len(architecting_problem.free_opt_des_vars)
    dv = [
        3.11309372,     # BPR
        3.35042243,     # FPR
        82.93060324,    # OPR
        0.123528576533,             # % of IPC PR
        0.,              # % of LPC PR
        10000,          # HP Shaft RPM
        5000,           # IP Shaft RPM
        0,              # LP Shaft RPM
        0,              # Gear Ratio
        0,              # Afterburner FAR
        0,              # Inter Turbine Burner FAR
        0.15,           # Inter-bleed HPC-burner total cooling bleed portion
        0,              # Inter-bleed HPC-burner cooling bleed portion of the IPT as target
        0,          # Inter-bleed HPC-burner cooling bleed portion of the LPT as target
        0,          # Inter-bleed IPC-HPC total cooling bleed portion
        0,          # Inter-bleed IPC-HPC cooling bleed portion of the IPT as target
        0,          # Inter-bleed IPC-HPC cooling bleed portion of the LPT as target
        0,          # Inter-bleed LPC-IPC total cooling bleed portion
        0,          # Inter-bleed LPC-IPC cooling bleed portion of the IPT as target
        0,          # Inter-bleed LPC-IPC cooling bleed portion of the LPT as target
        0.01,       # HPC intra-bleed total cooling bleed portion
        1,          # HPC intra-bleed cooling bleed portion of the IPT as target
        0,          # HPC intra-bleed cooling bleed portion of the LPT as target
        0,          # IPC intra-bleed total cooling bleed portion
        0,          # IPC intra-bleed cooling bleed portion of the IPT as target
        0,          # IPC intra-bleed cooling bleed portion of the LPT as target
        0,          # LPC intra-bleed total cooling bleed portion
        0,          # LPC intra-bleed cooling bleed portion of the IPT as target
        0,          # LPC intra-bleed cooling bleed portion of the LPT as target
        0,          # Intercooler location
        0,          # Intercooler radius
        0,          # Intercooler length
        0,          # Number of intercooler pipes
    ]
    # dv = [
    #             x_dict['bpr'],     # BPR
    #             x_dict['fpr'],     # FPR
    #             x_dict['opr'],    # OPR
    #             x_dict['pr_compressor_ip'],             # % of IPC PR
    #             0,              # % of LPC PR
    #             x_dict['rpm_shaft_hp'],          # HP Shaft RPM
    #             x_dict['rpm_shaft_ip'],          # IP Shaft RPM
    #             # x_dict['rpm_shaft_ip_frac'] * x_dict['rpm_shaft_hp'],          # IP Shaft RPM
                
    #             0,              # LP Shaft RPM
    #             0,              # Gear Ratio
    #             0,              # Afterburner FAR
    #             0,              # Inter Turbine Burner FAR
    #             x_dict['eb_hb_total'],           # Inter-bleed HPC-burner total cooling bleed portion
    #             x_dict['eb_hbi_frac_w'],              # Inter-bleed HPC-burner cooling bleed portion of the IPT as target
    #             0,          # Inter-bleed HPC-burner cooling bleed portion of the LPT as target
    #             x_dict['eb_ih_total'],          # Inter-bleed IPC-HPC total cooling bleed portion
    #             x_dict['eb_ihi_frac_w'],          # Inter-bleed IPC-HPC cooling bleed portion of the IPT as target
    #             0,          # Inter-bleed IPC-HPC cooling bleed portion of the LPT as target
    #             0,          # Inter-bleed LPC-IPC total cooling bleed portion
    #             0,          # Inter-bleed LPC-IPC cooling bleed portion of the IPT as target
    #             0,          # Inter-bleed LPC-IPC cooling bleed portion of the LPT as target
    #             x_dict['ab_hpc_total'],       # HPC intra-bleed total cooling bleed portion
    #             x_dict['ab_hi_frac_w'],          # HPC intra-bleed cooling bleed portion of the IPT as target
    #             0,          # HPC intra-bleed cooling bleed portion of the LPT as target
    #             x_dict['ab_ipc_total'],          # IPC intra-bleed total cooling bleed portion
    #             x_dict['ab_ii_frac_w'],          # IPC intra-bleed cooling bleed portion of the IPT as target
    #             0,          # IPC intra-bleed cooling bleed portion of the LPT as target
    #             0,          # LPC intra-bleed total cooling bleed portion
    #             0,          # LPC intra-bleed cooling bleed portion of the IPT as target
    #             0,          # LPC intra-bleed cooling bleed portion of the LPT as target
    #             0,          # Intercooler location
    #             0,          # Intercooler radius
    #             0,          # Intercooler length
    #             0,          # Number of intercooler pipes
    #         ]
    
    dv = [
                x_dict['bpr'],     # BPR
                x_dict['fpr'],     # FPR
                x_dict['opr'],    # OPR
                x_dict['pr_compressor_ip'],             # % of IPC PR
                0,              # % of LPC PR
                x_dict['rpm_shaft_hp'],          # HP Shaft RPM
                x_dict['rpm_shaft_ip'],          # IP Shaft RPM
                # x_dict['rpm_shaft_ip_frac'] * x_dict['rpm_shaft_hp'],          # IP Shaft RPM
                
                0,              # LP Shaft RPM
                0,              # Gear Ratio
                0,              # Afterburner FAR
                0,              # Inter Turbine Burner FAR
                0,# x_dict['eb_hb_total'],           # Inter-bleed HPC-burner total cooling bleed portion
                0,# x_dict['eb_hbi_frac_w'],              # Inter-bleed HPC-burner cooling bleed portion of the IPT as target
                0,          # Inter-bleed HPC-burner cooling bleed portion of the LPT as target
                0,# x_dict['eb_ih_total'],          # Inter-bleed IPC-HPC total cooling bleed portion
                0,# x_dict['eb_ihi_frac_w'],          # Inter-bleed IPC-HPC cooling bleed portion of the IPT as target
                0,          # Inter-bleed IPC-HPC cooling bleed portion of the LPT as target
                0,          # Inter-bleed LPC-IPC total cooling bleed portion
                0,          # Inter-bleed LPC-IPC cooling bleed portion of the IPT as target
                0,          # Inter-bleed LPC-IPC cooling bleed portion of the LPT as target
                0,# x_dict['ab_hpc_total'],       # HPC intra-bleed total cooling bleed portion
                0,# x_dict['ab_hi_frac_w'],          # HPC intra-bleed cooling bleed portion of the IPT as target
                0,          # HPC intra-bleed cooling bleed portion of the LPT as target
                0,# x_dict['ab_ipc_total'],          # IPC intra-bleed total cooling bleed portion
                0,# x_dict['ab_ii_frac_w'],          # IPC intra-bleed cooling bleed portion of the IPT as target
                0,          # IPC intra-bleed cooling bleed portion of the LPT as target
                0,          # LPC intra-bleed total cooling bleed portion
                0,          # LPC intra-bleed cooling bleed portion of the IPT as target
                0,          # LPC intra-bleed cooling bleed portion of the LPT as target
                0,          # Intercooler location
                0,          # Intercooler radius
                0,          # Intercooler length
                0,          # Number of intercooler pipes
            ]
    # architecting_problem.analysis_problem.design_condition.balancer._init_turbine_pr = (x_dict['opr']/x_dict['fpr'])**(0.5)
    # architecting_problem.analysis_problem.design_condition.balancer._init_mass_flow = 20 * x_dict['bpr']
    architecting_problem.analysis_problem.design_condition.balancer._init_turbine_pr = 10
    architecting_problem.analysis_problem.design_condition.balancer._init_mass_flow = 66
    
    
    # dv = [
    #     11,     # BPR
    #     1.6,     # FPR
    #     40*1.6,    # OPR
    #     0.15,             # % of IPC PR
    #     0.,              # % of LPC PR
    #     16645,          # HP Shaft RPM
    #     3894,           # IP Shaft RPM
    #     0,              # LP Shaft RPM
    #     0,              # Gear Ratio
    #     0,              # Afterburner FAR
    #     0,              # Inter Turbine Burner FAR
    #     0.15,           # Inter-bleed HPC-burner total cooling bleed portion
    #     0,              # Inter-bleed HPC-burner cooling bleed portion of the IPT as target
    #     0,          # Inter-bleed HPC-burner cooling bleed portion of the LPT as target
    #     0,          # Inter-bleed IPC-HPC total cooling bleed portion
    #     0,          # Inter-bleed IPC-HPC cooling bleed portion of the IPT as target
    #     0,          # Inter-bleed IPC-HPC cooling bleed portion of the LPT as target
    #     0,          # Inter-bleed LPC-IPC total cooling bleed portion
    #     0,          # Inter-bleed LPC-IPC cooling bleed portion of the IPT as target
    #     0,          # Inter-bleed LPC-IPC cooling bleed portion of the LPT as target
    #     0.01,       # HPC intra-bleed total cooling bleed portion
    #     1,          # HPC intra-bleed cooling bleed portion of the IPT as target
    #     0,          # HPC intra-bleed cooling bleed portion of the LPT as target
    #     0,          # IPC intra-bleed total cooling bleed portion
    #     0,          # IPC intra-bleed cooling bleed portion of the IPT as target
    #     0,          # IPC intra-bleed cooling bleed portion of the LPT as target
    #     0,          # LPC intra-bleed total cooling bleed portion
    #     0,          # LPC intra-bleed cooling bleed portion of the IPT as target
    #     0,          # LPC intra-bleed cooling bleed portion of the LPT as target
    #     0,          # Intercooler location
    #     0,          # Intercooler radius
    #     0,          # Intercooler length
    #     0,          # Number of intercooler pipes
    # ]
    # dv = [
    #     3.56565721,     # BPR
    #     2.90493411,     # FPR
    #     72.06388615,    # OPR
    #     0.0821501967,             # % of IPC PR
    #     0.,             # % of LPC PR
    #     10000,          # HP Shaft RPM
    #     5000,           # IP Shaft RPM
    #     0,              # LP Shaft RPM
    # ]
    # dv = [12.383723156909081, 1.481683726116061, 58.93829717456455, 0.21901465412816748, 0.1, 7067.649861383017, 1773.1628722840915, 10500.0, 3.0, 0.025, 0.025, 0.014797623414826336, 0.0, 0.0, 0.09749230568381187, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01679292542356151, 0.0, 0.0, 0.06939559703482323, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.030000000000000002, 0.255, 0]
    
    # print(len(free_dv_names))
    # print(len(dv))
    architecture, imputed_dv = architecting_problem.generate_architecture(dv)
    
    from open_turb_arch.evaluation.architecture.turbomachinery import Compressor, Turbine, Shaft
    
    print("")
    
    print('Architecture elements:')
    
    print("")
    
    print("All elements:")
    for el in architecture.elements:
        print("- %s: %s" % (el.name, type(el)))
        if hasattr(el, 'target'):
            if el.target is not None:
                # If target is list
                if isinstance(el.target, list):
                    for target in el.target:
                        if hasattr(target, 'name'):
                            print("   Target: %s" % target.name)
                        else:
                            print("   Target: %s" % target)
                else:
                    if hasattr(el.target, 'name'):
                        print("   Target: %s" % el.target.name)
                    else:
                        print("   Target: %s" % el.target)
        
    print("")
        
    print("Compressors:")
    for compressor in architecture.get_elements_by_type(Compressor):
        print(compressor.name)
        
    print("")
    
    print("Turbines:")
    for turbine in architecture.get_elements_by_type(Turbine):
        print(turbine.name)
    
    print("")
    
    print("Shafts:")    
    for shaft in architecture.get_elements_by_type(Shaft):
        print(shaft.name)
        print("  Connected elements")
        for el in shaft.connections:
            print("    %s" % el.name)
    
    print("")
    
    # from open_turb_arch.evaluation.architecture.visualization import ArchitectureVisualizer
    # visualizer = ArchitectureVisualizer()
    # visualizer.export_svg(architecture, 'simple_turbojet_architecture.svg')
    
    imputed_dv_dict = {des_var: value for des_var, value in zip(free_dv_names, imputed_dv)}
    
    print('Imputed design vector: %r' % imputed_dv_dict)
    
    design_vector, objectives, constraints, metrics = architecting_problem.evaluate(imputed_dv)

    print('Design vector: %r' % design_vector)
    print('Objectives: %r' % objectives)
    print('Constraints: %r' % constraints)
    print('Metrics: %r' % metrics)