import csv
import codecs

"""Takes in a string to tell which dataset csv file to pull from.
Any categorical features are removed from the input vectors.
All labels are stripped from the input vectors.
Sets any missing data features to zero. The 
Balance dataset has a special function to 
handle a categorical feature.
Returns a vector of input vectors back to the handler."""

class PreProcess:

    def determine_dataset(self,dataset):    #taken in from handler
        if dataset == "balance":
            print("Balance Scale Dataset")
            input = self.process_balance()
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
            elif dataset == 'user':
                print("User Knowledge Modeling Dataset")
                dataFile = 'user_knowledge'
            else:
                print("Test Dataset")     #if there's another dataset you want to test
                dataFile = dataset
            input = self.process_basic(dataFile)

        return input                      #return the processed input vectors back to the handler

    def process_basic(self, dataFile):
        "Remove labels and process all the datasets except for the balance dataset."
        input = []
        with codecs.open('code/Data/original/' + dataFile + '.csv', 'r', encoding='utf-8') as file:
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
        """Remove labels and vectorize categorical features for the balance dataset."""
        input = []
        with codecs.open('code/Data/original/balance.csv', 'r', encoding='utf-8') as file:
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

