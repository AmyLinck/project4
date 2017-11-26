import csv
import codecs

"""Takes in a string to tell which dataset csv file to pull from.
Any categorical features are removed from the input vectors.
All labels are stripped from the input vectors.
Sets any missing data features to zero.
Returns a vector of input vectors back to the handler."""

class PreProcess:

    def determine_dataset(self,dataset):
        input = []
        if dataset == "abalone":
            print("Abalone Dataset")
            input = self.process_abalone()
        elif dataset == "cmc":
            print("Contraceptive Method Choice Dataset")
            input = self.process_cmc()
        elif dataset == "epileptic":
            print("Epileptic Seizure Dataset")
            input = self.process_epileptic()
        elif dataset == "census":
            print("US Census 1990 Dataset")
            input = self.process_census()
        elif dataset == "water":
            print("Water Treatment Dataset")
            input = self.process_water()
        else:
            print("Testing Dataset")
            input = self.process_fert()
        return input

    def process_abalone(self):
        input = []
        with codecs.open('Data/original/abalone.csv', 'r', encoding='utf-8') as abl:
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
        with codecs.open('Data/original/contraceptive_method_choice.csv', 'r', encoding='utf-8') as cmc:
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
        with codecs.open('Data/original/epileptic.csv', 'r', encoding='utf-8') as epl:
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
        with codecs.open('Data/original/us_census_1990.csv', 'r', encoding='utf-8') as us:
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
        with codecs.open('Data/original/water_treatment.csv', 'r', encoding='utf-8') as water:
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


    def process_fert(self): #just for quick testing
        input = []
        with codecs.open('Data/original/fertility.csv', 'r', encoding='utf-8') as fertility:
            csv_input = csv.reader(fertility, delimiter=",")
            for row in csv_input:
                example = []
                for element in range(len(row)):
                    if element < len(row) - 1:
                        example.append(float(row[element]))
                input.append(example)
        return input