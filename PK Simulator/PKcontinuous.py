import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint

class Patient:
    ''' Class designed to hold all relevent patient parameters '''
    
    def __init__(self, k_slope, k_int, cl_cr, v_slope, bw):
        ''' Creates Patient object
        
            k_slope: Patient's Kslope as a numeric value
            k_int: Patient's nonrenal elimination constant as a numeric value
            cl_cr: Patient's creatinine clearance rate as a numeric value
            v_slope: Patient's Vslope as a numeric value
            bw: Patient's bodyweight
        '''
        
        self.k_slope = k_slope
        self.k_int = k_int
        self.cl_cr = cl_cr
        
        self.v_slope = v_slope
        self.bw = bw
        
        self.k_el = k_int + k_slope * cl_cr
        self.v_d = v_slope * bw
        
class Prior:
    ''' Class designed to hold weights for discrete prior '''
    
    def __init__(self, k_slopes, v_slopes, patient):
        ''' Creates Prior object
        
            k_slopes: Each Kslope to be used in discrete prior as a list of numeric values
            v_slopes: Each Vslope to be used in discrete prior as a list of numeric values
            patient: 
        '''
        
        self.k_slopes = k_slopes
        self.v_slopes = v_slopes
        self.patient = patient
        self.weights = self.initialize_weights()
        self.state = self.initialize_state()
        
    def initialize_weights(self):
        ''' Initializes the discrete prior used in the simulation
        
            Returns: 2-dimensional list of 3-tuples where
                     the first element of the tuple is the weight
                     the second element of the tuple is the patient with distinct parameters
        '''
        
        weights = [[]]
        weight = (len(self.k_slopes) * len(self.v_slopes))**(-1)
        
        for k_slope in self.k_slopes:
            for v_slope in self.v_slopes:
                k_int = self.patient.k_int
                cl_cr = self.patient.cl_cr
                bw = self.patient.bw
                
                patient = Patient(k_slope, k_int, cl_cr, v_slope, bw)
                
                weights[-1].append((weight, patient))
                
            weights.append([])
            
        return weights
    
    def initialize_state(self):
        
        state = [[]]
        for i in range(len(self.k_slopes)):
            for j in range(len(self.v_slopes)):
                x_hat = 0
                P = 1
                
                state[-1].append((x_hat, P))
                
            state.append([])
                
        return state
    
    def kalman_filter(self, a, b, dose, dose_fn, error, y):
        total = 0
        
        for i in range(len(self.k_slopes)):
            for j in range(len(self.v_slopes)):
                weight, patient = self.weights[i][j]
                
                x_next, P = self.state[i][j]
                
                x_prev = np.exp(-patient.k_el*(b-a))*x_next + dose*dose_fn(a, b, patient)
                M_next = np.exp(-2*patient.k_el*(b-a))*P + error
                #print(M_next)
                
                omega_next = M_next + 1
                
                P_next = M_next - M_next**2/omega_next
                x_next = x_prev + P_next*(y - x_prev)
                
                self.state[i][j] = (x_next, P_next)
                update = np.random.normal(y - x_prev, 1)#omega_next)
                total += update*weight # duh
                
                self.weights[i][j] = (update*weight, patient)
                
        for i in range(len(self.k_slopes)):
            for j in range(len(self.v_slopes)):
                weight, patient = self.weights[i][j]
                
                self.weights[i][j] = (weight/total, patient)
                
class ErrorTypes:
    ''' Class designed to hold all errors relevent to the simulation '''
    
    def __init__(self, measurement, measurement_timing, dosage, dosage_timing):
        ''' Creates ErrorTypes object
        
            measurement: Measurement error variance as a numeric value
            measurement_timing: Measurement timing error variance as a numeric value
            dosage: Dosage error variance as a numeric value
            dosage_timing: Dosage timing error variance as a numeric value
        '''
        
        self.measurement = measurement
        self.measurement_timing = measurement_timing
        self.dosage = dosage
        self.dosage_timing = dosage_timing
        
class Therapy:
    ''' Class designed to hold details about therapeutic session '''
    
    def __init__(self, duration, dosage_period, dosage_length, measurement_times, peak, trough):
        ''' Creates Therapy object
        
            duration: Length in hours of therapeutic session as a numeric value
            dosage_period: Length in hours between each dose given as a numeric value
            dosage_length: Length of dose in hours as a numeric value
            measurement_times: Times at which measurements will be taken as a list of numeric values
            peak: Peak therapeutic goal in mg/L as a numeric value
            trough: Trough therapeutic goal in mg/L as a numeric value
        '''
        
        self.duration = duration
        self.dosage_period = dosage_period
        self.dosage_length = dosage_length
        self.measurement_times = measurement_times
        self.peak = peak
        self.trough = trough
        
class PKSimulator:
    ''' Class for conducting pharmacokinetic simulations '''
    
    def __init__(self, patient, priors, errors, therapy):
        ''' Creates PKSimulator object 
        '''
        
        self.patient = patient
        self.priors = priors
        self.errors = errors
        self.therapy = therapy
        
        self.time_steps = [0]
        self.amount_steps = [0]
        self.concentration_steps = [0]
        
        self.measurements = []
        
        self.dosage_errors = []
        self.dosage_timing_errors = []
        
        self.dosage_interval = 0
        
        self.dose = self.optimalInitialDose()
        
    def simulate(self, step_size, stop_time, dose, patient=None, precision=1, reset=False):
        
        if patient == None:
            patient = self.patient
            
        while self.time_steps[-1] < stop_time: 
            a = self.time_steps[-1]
            b = a + step_size
            b = round(b, precision)
            #print(self.time_steps[-1], stop_time)
                       
            if a > self.therapy.dosage_period * self.dosage_interval + self.therapy.dosage_length:
                self.dosage_interval += 1
                
            if len(self.dosage_errors) == self.dosage_interval:
                percent_error = np.random.normal(0, self.errors.dosage)
                self.dosage_errors.append(percent_error)
            
            prev = self.amount_steps[-1]
            loss = np.exp(-patient.k_el*(b-a))
            gain = dose * self.administer(a, b, patient)
                
            M_error = np.sqrt((1-np.exp(-2*patient.k_el*(b-a)))/(2*patient.k_el))
            D_error = gain * self.dosage_errors[-1]
            T_error = 1
            #print(M_error, D_error, T_error)
            
            #w1 = np.random.normal(0, self.errors.)
            w2 = np.random.normal(0, self.errors.dosage)
            w3 = np.random.normal(0, self.errors.dosage_timing)
            
            curr = prev*loss + gain + M_error + D_error*w2 + T_error*w3
            
            self.amount_steps.append(curr)
            self.concentration_steps.append(curr/patient.v_d)
            self.time_steps.append(b)  

            if b in self.therapy.measurement_times:
                measurement_error = np.random.normal(0, self.errors.measurement)
                self.measurements.append(self.concentration_steps[-1] + measurement_error)
                self.priors.kalman_filter(a, b, dose, self.administer, M_error+D_error+T_error, self.measurements[-1])
                
        if reset:
            info = (self.time_steps, self.amount_steps, self.concentration_steps)
                
            self.time_steps = [0]
            self.amount_steps = [0]
            self.concentration_steps = [0]
                
            self.measurements = []
        
            self.dosage_errors = []
            self.dosage_timing_errors = []
        
            self.dosage_interval = 0
            self.doses = []
                
            return info
    
    def administer(self, a, b, patient):
        # dose interval from tk to tk_star
        tk = self.dosage_interval * self.therapy.dosage_period
        tk_star = tk + self.therapy.dosage_length
        
        # b is to the left of the dose interval
        if b <= tk:
            val = 0
        
        # a is outside dose interval, b is in dose interval
        elif a < tk and b > tk:
            val = (1-np.exp(-patient.k_el*(b-tk)))/patient.k_el
        
        # a and b are inside of dose interval
        elif a >= tk and b <= tk_star:
            val = (1-np.exp(-patient.k_el*(b-a)))/patient.k_el
        
        # a is in dose interval, b is outside dose interval
        elif a < tk_star and b > tk_star:
            val = (np.exp(-patient.k_el*(b-a))-np.exp(-patient.k_el*(b-tk_star)))/patient.k_el
        
        # a is to the right of the dose interval
        else:
            val = 0

        return val
    
    def optimalInitialDose(self):
        dose = 0
        
        for i in range(len(self.priors.k_slopes)):
            for j in range(len(self.priors.v_slopes)):
                w, patient = self.priors.weights[i][j]
                dose += w * self.optimalDose(patient)
     
        return dose
    
    def optimalDose(self, patient, tolerance=0.01, step=0.1, max_iter=50):
        minimum_dose = 0
        maximum_dose = 3000

        curr = (minimum_dose + maximum_dose) / 2

        idx = 0
        peak = 0
        trough = 0
        last = 0
        error = (peak - self.therapy.peak)**2 + (trough - self.therapy.trough)**2
        
        while idx < max_iter:
            ts, ys, zs = self.simulate(step_size=step, 
                                       stop_time=self.therapy.dosage_period, 
                                       dose=curr,
                                       patient=patient,
                                       reset=True)
            
            peak = zs[ts.index(self.therapy.dosage_length)]
            trough = zs[ts.index(self.therapy.dosage_period-1)]
            
            if peak >= self.therapy.peak and trough >= self.therapy.trough:
                maximum_dose = curr

            elif peak <= self.therapy.peak and trough <= self.therapy.trough:
                minimum_dose = curr
                
            elif peak >= self.therapy.peak and trough <= self.therapy.trough:
                maximum_dose = curr
                
            else:
                minimum_dose = curr
                
            last = error
            error = (peak - self.therapy.peak)**2 + (trough - self.therapy.trough)**2
            
            if abs(error - last) < tolerance:
                break
                
            curr = (minimum_dose + maximum_dose) / 2
            idx += 1

        return curr
    
    def graph(self):
        plt.xlabel('Time (hours)')
        plt.ylabel('Concentration (mg/L)')
        
        plt.axhline(self.therapy.peak, color='r', label='Goal Concentrations')
        plt.axhline(self.therapy.trough, color='r')
        
        plt.plot(self.time_steps, self.concentration_steps, label='True Concentration')
        
        plt.plot(self.therapy.measurement_times, self.measurements, 'ro', label='Noisy Measurements')
        
        plt.legend()
        plt.show()
        
def sample_k_slopes(num, p, mean1, stdev1, mean2, stdev2):
    return np.random.normal(mean1, stdev1, num) if np.random.uniform() >= p else np.random.normal(mean2, stdev2, num)

def sample_v_slopes(num, mean, stdev):
    return np.random.normal(mean, stdev, num)
    
if __name__ == '__main__':
    plt.rcParams['figure.figsize'] = (10, 8)

    # parameters for Patient object
    k_int = 0.01
    k_slope = 0.003125
    cl_cr = 50
    v_slope = 0.2806
    bw = 70

    # parameters for Prior object
    k_slopes = sample_k_slopes(9, 0.2, 0.0041666666666666675, 0.001, 0.0020833333333333333, 0.001)
    v_slopes = sample_v_slopes(9, 0.2806, 0.05)
    
    # parameters for ErrorTypes object
    measurement_error = 0
    measurement_timing_error = 0 
    dosage_error = 0
    dosage_timing_error = 0
    
    # parameters for Therapy object
    duration = 240
    dosage_period = 12
    dosage_length = 1
    measurement_times = [1, 11, 73, 83, 145, 155]
    peak_goal = 7
    peak_trough = 1.5

    # parameters for PKSimulator object
    patient = Patient(k_slope, k_int, cl_cr, v_slope, bw) # also parameter for Prior object
    prior = Prior(k_slopes, v_slopes, patient)
    errors = ErrorTypes(measurement_error, measurement_timing_error, dosage_error, dosage_timing_error)
    therapy = Therapy(duration, dosage_period, dosage_length, measurement_times, peak_goal, peak_trough)
    
    simulator = PKSimulator(patient, prior, errors, therapy)
    simulator.simulate(step_size=0.1, stop_time=240, dose=simulator.dose)
    simulator.graph()
