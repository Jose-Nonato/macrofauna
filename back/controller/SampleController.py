from models.SampleModel import FullSampleSchema
from math import log10
from statistics import mean


COEFFS = {
    "earthworm": 19.2,    # EWM
    "ant": 17.5,          # ANT
    "isoptera": 20.9,     # TER (isoptera -> termite)
    "blattaria": 9.8,     # BLA
    "coleoptera": 20.4,   # COL
    "arachnida": 17.5,    # ARAC
    "diplopoda": 20.1,    # DIPLO
    "chilopoda": 21.8,    # CHILO
    "hemiptera": 13.5,    # HEMI
    "dermapoda": 8.9,     # DERMA (opcional)
    "lepidoptera": 15.5,  # LEPI (opcional)
    "gasteropida": 16.7,  # GAST
    "others": 21.9        # OTR
}


class SampleController:
    @staticmethod
    def calculate_density(sample: dict, area_m2: float = 0.0625):
        """
        Calcula a densidade de organismos por m², a partir dos valores da amostra.
        Por padrão, considera monolito de 25x25cm (0.0625 m²) 
        """
        total_individuos = sum(
            v for k, v in sample.items() if k in COEFFS.keys()
        )
        den = total_individuos / area_m2 if area_m2 > 0 else 0
        return round(den, 2)


    @staticmethod
    def calculate_iqms_for_sample_individual(sample: dict):
        rt = 0
        score_num = 0.0
        for key, coeff in COEFFS.items():
            val = sample.get(key, 0)
            score_num += coeff * val
            if val > 0:
                rt += 1
        
        score_num += 31.8 * sample.get('DEN', 0)
        score_num += 31.8 * rt
        
        iqms_individual = round(log10(score_num + 1), 2)

        return {
            'iqms_sample': iqms_individual,
            'rt': rt
        }


    @staticmethod
    def calculate_iqms_for_sample(samples: FullSampleSchema):
        samples_dict = samples.model_dump()
        iqms_avg = 0.0
        rt_avg = 0
        iqms_list = []
        rt_list = []

        for monolith in samples_dict['sample']:
            den = SampleController.calculate_density(samples_dict['sample'][monolith])
            iqms_individual = SampleController.calculate_iqms_for_sample_individual(samples_dict['sample'][monolith])
            samples_dict['sample'][monolith]['density'] = den
            samples_dict['sample'][monolith]['iqms_sample'] = round(iqms_individual['iqms_sample'], 2)
            samples_dict['sample'][monolith]['rt'] = iqms_individual['rt']

            iqms_list.append(iqms_individual['iqms_sample'])
            rt_list.append(iqms_individual['rt'])

        iqms_avg = mean(iqms_list)
        rt_avg = mean(rt_list)
        samples_dict['iqms'] = round(iqms_avg, 2)
        samples_dict['rt'] = int(rt_avg)

        return FullSampleSchema(**samples_dict)
