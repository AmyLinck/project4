import csv
import codecs

class PreProcess:

    def determine_dataset(self,dataset):
        input = []
        if dataset == "abalone":
            input = self.process_abalone()
        elif dataset == "cmc":
            input = self.process_cmc()
        elif dataset == "epileptic":
            input = self.process_epileptic()
        elif dataset == "census":
            input = self.process_census()
        elif dataset == "water":
            input = self.process_water()
        return input

    def process_abalone(self):
        input = []
        with codecs.open('Data/abalone.csv', 'r', encoding='utf-8') as abl:
            csv_input = csv.reader(abl, delimiter=",")
            for row in csv_input:
                example = []
                for element in range(len(row)):
                    if element < len(row) - 1:
                        if element > 0:
                            example.append(float(row[element]))
                input.append(example)
        return input

    def process_cmc(self):
        input = []
        with codecs.open('Data/contraceptive_method_choice.csv', 'r', encoding='utf-8') as cmc:
            csv_input = csv.reader(cmc, delimiter=",")
            for row in csv_input:
                example = []
                for element in range(len(row)):
                    if element < len(row) - 1:
                        example.append(float(row[element]))
                input.append(example)
        return input

    def process_epileptic(self):
        input = []
        with codecs.open('Data/epileptic.csv', 'r', encoding='utf-8') as epl:
            csv_input = csv.reader(epl, delimiter=",")
            index = 0
            for row in csv_input:
                example = []
                if index > 0:
                    for element in range(len(row)):
                        if element < len(row) - 1:
                            if element > 0:
                                example.append(float(row[element]))
                    input.append(example)
                index = 1
        return input

    def process_census(self):
        input = []
        with codecs.open('Data/us_census_1990.csv', 'r', encoding='utf-8') as us:
            csv_input = csv.reader(us, delimiter=",")
            index = 0
            for row in csv_input:
                example = []
                if index > 0:
                    for element in range(len(row)):
                        if element < len(row) - 1:
                            if element > 0:
                                example.append(float(row[element]))
                    input.append(example)
                index = 1
        return input

    def process_water(self):
        input = []
        with codecs.open('Data/water_treatment.csv', 'r', encoding='utf-8') as water:
            csv_input = csv.reader(water, delimiter=",")
            for row in csv_input:
                example = []
                for element in range(len(row)):
                    if element < len(row) - 1:
                        if element > 0:
                            if row[element] == "?":
                                row[element] = 0.0
                            example.append(float(row[element]))
                input.append(example)
        return input