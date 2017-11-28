import csv
import codecs

"""Takes in a string to tell which dataset csv file to pull from.
Any categorical features are removed from the input vectors.
All labels are stripped from the input vectors.
Sets any missing data features to zero.  Indian liver
and balance datasets have special functions to 
handle categorical features and missing data.
Returns a vector of input vectors back to the handler."""

class PreProcess:

    def determine_dataset(self,dataset):
        if dataset == "balance":
            print("Balance Scale Dataset")
            input = self.process_balance()
        elif dataset == "indian":
            print("Indian Liver Patient Dataset")
            input = self.process_indian_liver()
        else:
            if dataset == 'abalone':
                print("Abalone Dataset")
                dataFile = 'abalone'
            elif dataset == "cmc":
                print("Contraceptive Method Choice Dataset")
                dataFile = 'contraceptive_method_choice'
            elif dataset == "fertility":
                print("Fertility Dataset")
                dataFile = 'fertility'
            else:
                print("Test Dataset")
                dataFile = dataset
            input = self.process_basic(dataFile)

        return input

    def process_basic(self, dataFile):
        input = []
        with codecs.open('Data/original/' + dataFile + '.csv', 'r', encoding='utf-8') as file:
            csv_input = csv.reader(file, delimiter=",")
            for row in csv_input:
                example = []
                for element in range(len(row)):
                    if element < len(row) - 1:
                        if element > 0:
                            example.append(float(row[element]))
                input.append(example)
        return input

    def process_balance(self):
        input = []
        with codecs.open('Data/original/balance.csv', 'r', encoding='utf-8') as file:
            csv_input = csv.reader(file, delimiter=",")
            for row in csv_input:
                example = []
                for element in range(len(row)):
                    if element < len(row) - 1:
                        if element > 0:
                            if row[element] == "L":
                                row[element] = 1
                            elif row[element] == "R":
                                row[element] = 2
                            elif row[element] == "B":
                                row[element] = 3
                            example.append(float(row[element]))
                input.append(example)
        return input

    def process_indian_liver(self):
        input = []
        with codecs.open('Data/original/indian_liver_patient.csv', 'r', encoding='utf-8') as file:
            csv_input = csv.reader(file, delimiter=",")
            for row in csv_input:
                example = []
                for element in range(len(row)):
                    if element < len(row) - 1:
                        if row[element] == "Male" or row[element] == "Female":
                            pass
                        elif row[element] == "":
                            example.append(0)
                        else:
                            example.append(float(row[element]))
                input.append(example)
        return input
