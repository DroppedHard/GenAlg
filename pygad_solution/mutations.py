import numpy as np

def gauss_mutation(offspring, ga_instance):

    """
    Mutacja Gaussowska na podstawie mutation_percent_gens
    """

    mutation_probability = ga_instance.mutation_percent_genes / 100

    for chromoseme_idx in range(offspring.shape[0]):
        for gene_idx in range(offspring.shape[1]):
            if np.random.rand() > mutation_probability:
                continue
            mutation_value = np.random.normal(0, 1)
            while mutation_value + offspring[chromoseme_idx, gene_idx] < ga_instance.init_range_low or mutation_value + offspring[chromoseme_idx, gene_idx] > ga_instance.init_range_high:
                mutation_value = np.random.normal(0, 1)
                
            offspring[chromoseme_idx, gene_idx] += mutation_value

    return offspring

