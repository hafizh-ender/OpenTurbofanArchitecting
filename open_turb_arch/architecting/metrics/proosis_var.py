from typing import *
from dataclasses import dataclass
from open_turb_arch.architecting.metric import *
from open_turb_arch.evaluation.analysis.disciplines import *
from open_turb_arch.evaluation.architecture import *

import open_turb_arch.evaluation.architecture.units as units

__all__ = ['BurnerInletTemperatureMetric', 'P17Q7Metric', 'DHQT41Metric', 'DHQT46Metric', 'WRQAE2AMetric', 'TurbineInletTemperatureMetric']

@dataclass(frozen=False)
class BurnerInletTemperatureMetric(ArchitectingMetric):
    """Representing the burner inlet temperature as design goal or constraint."""

    max_t_burner_inlet: float = 1500  # [K], if used as a constraint

    # Specify the operating condition to extract from, otherwise will take the design condition
    condition: OperatingCondition = None

    def get_opt_objectives(self, choices: List[ArchitectingChoice]) -> List[Objective]:
        return [Objective('t_burner_inlet_obj', ObjectiveDirection.MINIMIZE)]

    def get_opt_constraints(self, choices: List[ArchitectingChoice]) -> List[Constraint]:
        return [Constraint('t_burner_inlet_con', ConstraintDirection.LOWER_EQUAL_THAN, limit_value=self.max_t_burner_inlet)]

    def get_opt_metrics(self, choices: List[ArchitectingChoice]) -> List[OutputMetric]:
        return [OutputMetric('t_burner_inlet_met')]

    def extract_met(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap, architecture: TurbofanArchitecture) -> Sequence[float]:
        return [self._get_t_burner_inlet(analysis_problem, result)]

    def _get_t_burner_inlet(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap):
        ops_metrics = result[analysis_problem.design_condition] if self.condition is None else result[self.condition]
        
        output = ops_metrics.t_burner_in
        
        if units.TEMPERATURE == 'degC':
            output += 273.15  # convert from degC to K if needed
        
        return output  # get main burner inlet temperature as metric


class P17Q7Metric(ArchitectingMetric):
    """Representing the bypass flow total pressure (Pt17) over turbine outlet/nozzle inlet total pressure (Pt7) as design goal or constraint."""

    max_p17qpt7: float = 1.5  # [-], if used as a constraint

    # Specify the operating condition to extract from, otherwise will take the design condition
    condition: OperatingCondition = None

    def get_opt_objectives(self, choices: List[ArchitectingChoice]) -> List[Objective]:
        return [Objective('p17qpt7_obj', ObjectiveDirection.MINIMIZE)]

    def get_opt_constraints(self, choices: List[ArchitectingChoice]) -> List[Constraint]:
        return [Constraint('p17qpt7_con', ConstraintDirection.LOWER_EQUAL_THAN, limit_value=self.max_p17qpt7)]

    def get_opt_metrics(self, choices: List[ArchitectingChoice]) -> List[OutputMetric]:
        return [OutputMetric('p17qpt7_met')]

    def extract_met(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap, architecture: TurbofanArchitecture) -> Sequence[float]:
        return [self._get_p17qpt7(analysis_problem, result)]

    def _get_p17qpt7(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap):
        ops_metrics = result[analysis_problem.design_condition] if self.condition is None else result[self.condition]
        return ops_metrics.p17qpt7  # get bypass flow total pressure (Pt17) over turbine outlet/nozzle inlet total pressure (Pt7) as metric

class DHQT41Metric(ArchitectingMetric):
    """Representing the enthalpy drop across the high-pressure turbine (HPT) divided by the total temperature at the HPT inlet as design goal or constraint."""

    max_dh4qtt4: float = 0.5  # [-], if used as a constraint

    # Specify the operating condition to extract from, otherwise will take the design condition
    condition: OperatingCondition = None

    def get_opt_objectives(self, choices: List[ArchitectingChoice]) -> List[Objective]:
        return [Objective('dh4qtt4_obj', ObjectiveDirection.MINIMIZE)]

    def get_opt_constraints(self, choices: List[ArchitectingChoice]) -> List[Constraint]:
        return [Constraint('dh4qtt4_con', ConstraintDirection.LOWER_EQUAL_THAN, limit_value=self.max_dh4qtt4)]

    def get_opt_metrics(self, choices: List[ArchitectingChoice]) -> List[OutputMetric]:
        return [OutputMetric('dh4qtt4_met')]

    def extract_met(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap, architecture: TurbofanArchitecture) -> Sequence[float]:
        return [self._get_dh4qtt4(analysis_problem, result)]

    def _get_dh4qtt4(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap):
        ops_metrics = result[analysis_problem.design_condition] if self.condition is None else result[self.condition]
        return ops_metrics.dh4qtt4  # get enthalpy drop across the high-pressure turbine (HPT) divided by the total temperature at the HPT inlet as metric

class DHQT46Metric(ArchitectingMetric):
    """Representing the enthalpy drop across the IP turbine (if present) divided by the total temperature at the IP turbine inlet (if present) as design goal or constraint."""

    max_dh46qtt46: float = 0.5  # [-], if used as a constraint

    # Specify the operating condition to extract from, otherwise will take the design condition
    condition: OperatingCondition = None

    def get_opt_objectives(self, choices: List[ArchitectingChoice]) -> List[Objective]:
        return [Objective('dh46qtt46_obj', ObjectiveDirection.MINIMIZE)]

    def get_opt_constraints(self, choices: List[ArchitectingChoice]) -> List[Constraint]:
        return [Constraint('dh46qtt46_con', ConstraintDirection.LOWER_EQUAL_THAN, limit_value=self.max_dh46qtt46)]

    def get_opt_metrics(self, choices: List[ArchitectingChoice]) -> List[OutputMetric]:
        return [OutputMetric('dh46qtt46_met')]

    def extract_met(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap, architecture: TurbofanArchitecture) -> Sequence[float]:
        return [self._get_dh46qtt46(analysis_problem, result)]

    def _get_dh46qtt46(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap):
        ops_metrics = result[analysis_problem.design_condition] if self.condition is None else result[self.condition]
        return ops_metrics.dh46qtt46  # get enthalpy drop across the IP turbine (if present) divided by the total temperature at the IP turbine inlet (if present) as metric

class WRQAE2AMetric(ArchitectingMetric):
    """Representing the fan reduced mass flow divided by fan area as design goal or constraint."""

    max_wrqae2a: float = 0.5  # [-], if used as a constraint

    # Specify the operating condition to extract from, otherwise will take the design condition
    condition: OperatingCondition = None

    def get_opt_objectives(self, choices: List[ArchitectingChoice]) -> List[Objective]:
        return [Objective('wrqae2a_obj', ObjectiveDirection.MINIMIZE)]

    def get_opt_constraints(self, choices: List[ArchitectingChoice]) -> List[Constraint]:
        return [Constraint('wrqae2a_con', ConstraintDirection.LOWER_EQUAL_THAN, limit_value=self.max_wrqae2a)]

    def get_opt_metrics(self, choices: List[ArchitectingChoice]) -> List[OutputMetric]:
        return [OutputMetric('wrqae2a_met')]

    def extract_met(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap, architecture: TurbofanArchitecture) -> Sequence[float]:
        return [self._get_wrqae2a(analysis_problem, result)]

    def _get_wrqae2a(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap):
        ops_metrics = result[analysis_problem.design_condition] if self.condition is None else result[self.condition]
        return ops_metrics.wrqae2a  # get fan reduced mass flow divided by fan area as metric

class TurbineInletTemperatureMetric(ArchitectingMetric):
    """Representing the turbine inlet temperature as design goal or constraint."""

    max_t_turbine_inlet: float = 1500  # [K], if used as a constraint

    # Specify the operating condition to extract from, otherwise will take the design condition
    condition: OperatingCondition = None

    def get_opt_objectives(self, choices: List[ArchitectingChoice]) -> List[Objective]:
        return [Objective('t_turbine_inlet_obj', ObjectiveDirection.MINIMIZE)]

    def get_opt_constraints(self, choices: List[ArchitectingChoice]) -> List[Constraint]:
        return [Constraint('t_turbine_inlet_con', ConstraintDirection.LOWER_EQUAL_THAN, limit_value=self.max_t_turbine_inlet)]

    def get_opt_metrics(self, choices: List[ArchitectingChoice]) -> List[OutputMetric]:
        return [OutputMetric('t_turbine_inlet_met')]

    def extract_met(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap, architecture: TurbofanArchitecture) -> Sequence[float]:
        return [self._get_t_turbine_inlet(analysis_problem, result)]

    def _get_t_turbine_inlet(self, analysis_problem: AnalysisProblem, result: OperatingMetricsMap):
        ops_metrics = result[analysis_problem.design_condition] if self.condition is None else result[self.condition]
        
        output = ops_metrics.t_turb_in  # get turbine inlet temperature as metric
        
        if units.TEMPERATURE == 'degC':
            output += 273.15  # convert to K if the temperature is in degC
        
        return output